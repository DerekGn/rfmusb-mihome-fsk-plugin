# Python plugin for controlling energenie Fsk devices
#
# Author: DerekGn
#
"""
<plugin key="RfmEnergFsk" name="RfmUsb Energenie FSK" author="DerekGn" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://github.com/DerekGn/rfmusb-mihome-fsk-plugin">
    <description>
        <h2>RfmUsb Energenie Fsk Devices Plugin</h2>
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
    CMD_GET_FIFO = "g-fifo"
    CMD_SET_RX = "s-om 4"
    
    RESPONSE_IRQ_RSSI = "DIO PIN IRQ [0x08]"
    RESPONSE_IRQ_RX = "DIO PIN IRQ [0x01]"
    RESPONSE_OK = "OK"
    
    InitCommands = [
        "e-r",
        "s-mt 0",
        "s-fd 0x01EC",
        "s-f 434300000",
        "s-rxbw 14",
        "s-br 4800",
        "s-ss 1",
        "s-se 1",
        "s-sbe 0",
        "s-sync 2DD4",
        "s-pf 0",
        "s-dfe 1",
        "s-crc 0",
        "s-caco 0",
        "s-af 0",
        "s-pl 66",
        "s-dio 0 1",
        "s-dio 3 1",
        "s-dim 0x9",
        "s-rt",
        "s-op"
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
                                         Protocol="None", Address=Parameters["SerialPort"], Baud=115200)
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

        if(self.IsInitalised == False):
            
            Domoticz.Debug("Command Executed: ["+self.LastCommand+"] Response: ["+strData+"] ")
            
            if(self.CommandIndex < len(self.InitCommands)):
                if(self.InitCommands[self.CommandIndex].startswith(self.CMD_SET_RSSI_THRESHOLD)):
                    self.sendCommand(self.CMD_SET_RSSI_THRESHOLD + " " + str(Parameters["Mode3"]))
                elif(self.InitCommands[self.CommandIndex].startswith(self.CMD_SET_OUTPUT_POWER)):
                    self.sendCommand(self.CMD_SET_OUTPUT_POWER + " " + str(Parameters["Mode4"]))
                else:
                    self.sendCommand(self.InitCommands[self.CommandIndex])

                self.CommandIndex = self.CommandIndex + 1
            else:
                Domoticz.Debug("Initalised Rfm")
                self.LastCommand = ""
                self.IsInitalised = True
                self.sendCommand(self.CMD_SET_RX)
        else:
            if(self.RESPONSE_IRQ_RSSI in strData):
                Domoticz.Debug("Serial Data: ["+strData+"]")
                self.sendCommand(self.CMD_GET_LAST_RSSI)
            elif(self.RESPONSE_IRQ_RX in strData):
                Domoticz.Debug("Serial Data: ["+strData+"]")
                self.sendCommand(self.CMD_GET_FIFO)
            elif(self.LastCommand == self.CMD_GET_LAST_RSSI):
                Domoticz.Debug("Command Executed: ["+self.LastCommand+"] Response: ["+strData+"] ")
                self.LastRssi = int(strData, 16)
            elif(self.LastCommand == self.CMD_GET_FIFO):
                Domoticz.Debug("Command Executed: ["+self.LastCommand+"] Response: ["+strData+"] ")
                # Decode the fifo data
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
            if(length > 10 and length+1 < 64):
                message = fifo[0:length+1]
                Domoticz.Debug("Message: " + "".join("%02x" %
                                                     b for b in message))
                openthingsMessage = OpenThings.decode(message)
                self.handleMessage(openthingsMessage)
            else:
                Domoticz.Debug(
                    "Received Message Length out of range: " + str(length))
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

        Domoticz.Debug("DeviceId: " + deviceId)

        if(not self.deviceExists(deviceId)):
            join = Common.findRecord(message, OpenThings.PARAM_JOIN)
            Domoticz.Debug("Join: " + str(join))
            if(join is not None):
                Domoticz.Log("Join Message From SensorId: "+str(sensorId))
                self.addDevice(manufacturerId, deviceId, productId)
            else:
                Domoticz.Log("SensorId: "+str(sensorId) + "not joined")
        else:
            Domoticz.Debug("Updating Device DeviceId: "+str(deviceId))
            self.updateDevice(deviceId, manufacturerId, productId, message)

    def addDevice(self, manufacturerId, deviceId, productId):
        if(manufacturerId == Energine.MFRID_ENERGENIE):
            Energine.createDevice(deviceId, productId)
        elif(manufacturerId == AxioLogix.MFRID_AXIOLOGIX):
            AxioLogix.createDevice(deviceId, productId)
        else:
            Domoticz.Error("Unknown Product Id: " + str(productId))

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
