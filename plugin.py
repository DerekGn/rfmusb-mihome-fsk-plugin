# Python plugin for controlling energenie Fsk devices
#
# Author: DerekGn
#
"""
<plugin key="RfmEnergFsk" name="RfmUsb Energenie FSK" author="DerekGn" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://github.com/DerekGn/rfmusb-mihome-fsk-plugin">
    <description>
        <h2>RfmUsb Energenie Fsk Devices Plugin Version: 1.0.0</h2>
        <br/>
        The RfmUsb Energenie Fsk Devices Plugin allows controlling various Energenie Fsk devices.
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Supports </li>
        </ul>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>Switch - On off control</li>
        </ul>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>Serial port is the name of the serial port that the Rfm69 is enumerated</li>
            <li>Tx Power Level is the Tx power level. Defaults to -2 dbm</li>
            <li>Tx Count is the number of times the switching message is transmitted.Defaults to 5</li>
        </ul>
    </description>
    <params>
        <param field="SerialPort" label="Serial Port" width="150px" required="true" default="/dev/serial1"/>
        <param field="Mode3" label="RSSI Threshold" width="100px" required="true" default="-114"/>
        <param field="Mode4" label="Tx Power Level" width="100px" required="true" default="0">
            <options>
                <option label="-2 dbm" value="-2"/>
                <option label="-1 dbm" value="-1"/>
                <option label="0 dbm" value="0"/>
                <option label="1 dbm" value="1"/>
                <option label="2 dbm" value="2"/>
                <option label="3 dbm" value="3"/>
                <option label="4 dbm" value="4"/>
                <option label="5 dbm" value="5"/>
                <option label="6 dbm" value="6"/>
                <option label="7 dbm" value="7"/>
                <option label="8 dbm" value="8"/>
                <option label="9 dbm" value="9"/>
                <option label="10 dbm" value="10"/>
                <option label="11 dbm" value="11"/>
                <option label="12 dbm" value="12"/>
                <option label="13 dbm" value="13"/>
                <option label="14 dbm" value="14"/>
                <option label="15 dbm" value="15"/>
                <option label="16 dbm" value="16"/>
                <option label="17 dbm" value="17"/>
                <option label="18 dbm" value="18"/>
                <option label="19 dbm" value="19"/>
                <option label="20 dbm" value="20"/>
            </options>
        </param>
        <param field="Mode6" label="Debug" width="150px">
            <options>
                <option label="None" value="0"  default="true" />
                <option label="Python Only" value="2"/>
                <option label="Basic Debugging" value="62"/>
                <option label="Basic+Messages" value="126"/>
                <option label="Queue" value="128"/>
                <option label="Connections Only" value="16"/>
                <option label="Connections+Queue" value="144"/>
                <option label="All" value="-1"/>
            </options>
        </param>
    </params>
</plugin>
"""
import DomoticzEx as Domoticz
import OpenThings
import AxioLogix
import Energine
import Common

class BasePlugin:

    CMD_GET_FIRMWARE_VERSION = "g-fv"
    CMD_SET_RSSI_THRESHOLD = "s-rt"
    CMD_SET_OUTPUT_POWER = "s-op"
    CMD_GET_LAST_RSSI = "g-lrssi"
    CMD_SET_STANDBY = "e-om 1"
    CMD_READ_BUFFER = "r-b"
    CMD_SET_RX = "s-om 4"

    RESPONSE_MODE_RX = "OK-[0x0004]-Rx"
    RESPONSE_IRQ = "DIO PIN IRQ"
    RESPONSE_OK = "OK"
    
    InitCommands = [
        "e-r",              # Reset the radio device
        "s-mt 0",           # Set modulation to FSK
        "s-fd 0x01EC",      # Set frequency deviation to ± 30kHz
        "s-f 434300000",    # Set frequency 434.300 MHz
        "s-rxbw 14",        # Set the rx bandwidth to 62 khz
        "s-br 4800",        # Baud rate 4800
        "s-ss 1",           # Set sync size to 1
        "s-se 1",           # Set sync enable
        "s-sbe 0",          # Set single bit error
        "s-sync 2DD4",      # Set the sync to 0x2D 0xD4
        "s-pf 1",           # Set packet format to variable
        "s-dfe 1",          # Set DC free encoding to manchester
        "s-crc 0",          # Set crc off
        "s-caco 0",         # Set crc auto clear off
        "s-af 0",           # Set address filter off
        "s-pl 0xFF",        # Set max packet length to 0xFF
        "s-dio 0 1",        # Set DIO 0 mapping to 1 for payload ready IRQ
        "s-dio 1 2",        # Set DIO 3 mapping to 1 for fifo not empty
        "s-dim 0x3",        # Set Irq mask to 3 
        "s-be 1",           # Enable buffered IO
        #"s-rt",             # Set the receive threshold
        "s-op"              # Set the output power
    ]

    LastCommand = ""
    CommandIndex = 0
    SerialConn = None
    IsInitalised = False
    LastRssi = 0
    LastIrq = 0

    def __init__(self):
        return

    def onStart(self):
        if Parameters["Mode6"] != "0":
            Domoticz.Debugging(int(Parameters["Mode6"]))
            DumpConfigToLog()

        OpenThings.init(242)
        SerialConn = Domoticz.Connection(Name="Serial Connection", Transport="Serial",
                                         Protocol="None", Address=Parameters["SerialPort"], Baud=230400)
        SerialConn.Connect()

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        if (Status == 0):
            Domoticz.Log("Connected successfully to: " +
                         Parameters["SerialPort"])

            self.SerialConn = Connection
            self.sendCommand(self.CMD_GET_FIRMWARE_VERSION)
        else:
            Domoticz.Log("Failed to connect ("+str(Status) +
                         ") to: "+Parameters["SerialPort"])

            Domoticz.Debug("Failed to connect ("+str(Status)+") to: " +
                           Parameters["SerialPort"]+" with error: "+Description)
        return True

    def onMessage(self, Connection, Data):
        strData = Data.decode("ascii")
        strData = strData.replace("\n", "")

        if(self.LastCommand != ""):
            Domoticz.Debug("Command Executed: ["+self.LastCommand+"] Response: ["+strData+"]")
        else:
            Domoticz.Debug("Serial Data: ["+strData+"]")
            
        if(self.IsInitalised == False):
            if(self.LastCommand.startswith(self.CMD_GET_FIRMWARE_VERSION)):
                Domoticz.Log("Rfm Firmware Version: " + strData)

            if(self.CommandIndex < len(self.InitCommands)):
                if(self.InitCommands[self.CommandIndex].startswith(self.CMD_SET_RSSI_THRESHOLD)):
                    self.sendCommand(self.CMD_SET_RSSI_THRESHOLD + " " + str(Parameters["Mode3"]))
                elif(self.InitCommands[self.CommandIndex].startswith(self.CMD_SET_OUTPUT_POWER)):
                    self.sendCommand(self.CMD_SET_OUTPUT_POWER + " " + str(Parameters["Mode4"]))
                else:
                    self.sendCommand(self.InitCommands[self.CommandIndex])

                self.CommandIndex = self.CommandIndex + 1
            else:
                Domoticz.Debug("Initalised Rfm FSK")
                self.LastCommand = ""
                self.IsInitalised = True
                self.sendCommand(self.CMD_SET_RX)
        else:
            if(self.RESPONSE_MODE_RX in strData):
                self.LastCommand = ""
            elif(self.RESPONSE_IRQ in strData) and ((strData[16:17] == "3") or (strData[16:17] == "1")):
                self.sendCommand(self.CMD_GET_LAST_RSSI)
            elif(self.LastCommand == self.CMD_GET_LAST_RSSI):
                self.LastRssi = int(strData, 16)
                self.sendCommand(self.CMD_READ_BUFFER)
            elif(self.LastCommand == self.CMD_READ_BUFFER):
                Domoticz.Debug("Command Executed: ["+self.LastCommand+"] Response: ["+strData+"] Rssi: ["+ str(self.LastRssi) +"]")
                # Decode the buffer data
                self.LastCommand = ""
                self.decodeProcessFifoData(strData)

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) +
                     ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text +
                     "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("Connection '"+Connection.Name+"' disconnected.")
        return

    def onHeartbeat(self):
        pass

    # Support functions
    def sendCommand(self, Command):
        self.LastCommand = Command
        self.SerialConn.Send(Command + "\n")

    def decodeProcessFifoData(self, data):
        try:
            fifo = bytearray.fromhex(data)
            length = fifo[0]
            message = fifo[0:length + 1]
            Domoticz.Debug("Message: " + "".join("%02x" % b for b in message) + " Length: " + str(length))
            openthingsMessage = OpenThings.decode(message)
            self.handleMessage(openthingsMessage)
        except OpenThings.OpenThingsException as error:
            errorMessage = str(error)
            Domoticz.Error("Unable to decode payload: " + errorMessage)

    def handleMessage(self, message):
        Domoticz.Debug(str(message))
        header = message["header"]
        sensorId = header["sensorid"]
        productId = header["productid"]
        manufacturerId = header["mfrid"]

        deviceId = Common.createDeviceId(productId, manufacturerId, sensorId)
        join = Common.findRecord(message, OpenThings.PARAM_JOIN)
        deviceExists = self.deviceExists(deviceId)

        if(join is not None):
            Domoticz.Debug("Join: " + str(join))
            if(not deviceExists):
                Domoticz.Log("Join Message From DeviceId: [" + str(deviceId) + "]")
                self.addDevice(manufacturerId, deviceId, productId)
            else:
                Domoticz.Log("DeviceId: [" + str(deviceId) + "] Already Joined")
        else:
            if(deviceExists):
                Domoticz.Debug("Updating DeviceId: [" + str(deviceId) + "]")
                self.updateDevice(deviceId, manufacturerId, productId, message)
            else:
                Domoticz.Log("DeviceId: [" + str(deviceId) + "] Not Found")

    def addDevice(self, manufacturerId, deviceId, productId):
        if(manufacturerId == Energine.MFRID_ENERGENIE):
            Energine.createDevice(deviceId, productId)
        elif(manufacturerId == AxioLogix.MFRID_AXIOLOGIX):
            AxioLogix.createDevice(deviceId, productId)
        else:
            Domoticz.Error("Unknown Product Id: [" + str(productId) + "]")

    def updateDevice(self, deviceId, manufacturerId, productId, message):
        if(manufacturerId == Energine.MFRID_ENERGENIE):
            Energine.updateDevice(deviceId, Devices, productId, message, self.LastRssi)
        elif(manufacturerId == AxioLogix.MFRID_AXIOLOGIX):
            AxioLogix.updateDevice(deviceId, Devices, productId, message, self.LastRssi)
    
    def deviceExists(self, deviceId):
        for x in Devices:
            if(Devices[x].DeviceID == deviceId):
                return True

        return False

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)


def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)


def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status,
                           Priority, Sound, ImageFile)


def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for DeviceName in Devices:
        Device = Devices[DeviceName]
        Domoticz.Debug("Device ID:       '" + str(Device.DeviceID) + "'")
        Domoticz.Debug("--->Unit Count:      '" + str(len(Device.Units)) + "'")
        for UnitNo in Device.Units:
            Unit = Device.Units[UnitNo]
            Domoticz.Debug("--->Unit:           " + str(UnitNo))
            Domoticz.Debug("--->Unit Name:     '" + Unit.Name + "'")
            Domoticz.Debug("--->Unit nValue:    " + str(Unit.nValue))
            Domoticz.Debug("--->Unit sValue:   '" + Unit.sValue + "'")
            Domoticz.Debug("--->Unit LastLevel: " + str(Unit.LastLevel))
    return
