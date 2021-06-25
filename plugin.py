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
        <param field="Mode5" label="Tx Count" width="100px" default="5">
            <options>
                <option label="Five" value="5"/>
                <option label="Eight" value="8"/>
                <option label="Thirteen" value="13"/>
            </options>
        </param>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import OpenThings
import AxioLogix
import Energine
import Common


class BasePlugin:

    CMD_GET_FIRMWARE_VERSION = "g-fv"
    CMD_SET_STANDBY = "e-om 1"
    CMD_GET_FIFO = "g-fifo"
    CMD_SET_RX = "s-om 4"
    CMD_RESULT_OK = "OK"

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
        "s-cc 0",
        "s-caco 0",
        "s-af 0",
        "s-pl 66",
        "s-dio 0 1",
        "s-di 1",
        "s-op"
    ]

    UnitIndex = 0
    LastCommand = ""
    CommandIndex = 0
    SerialConn = None
    IsInitalised = False

    def __init__(self):
        return

    def onStart(self):
        # if Parameters["Mode6"] == "Debug":
        Domoticz.Debugging(3)

        DumpConfigToLog()

        UnitIndex = self.getUnitIndex()

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

        Domoticz.Debug(
            "Command Executed: ["+self.LastCommand+"] Respose: ["+strData+"] ")

        if(self.IsInitalised == False):
            if(self.CommandIndex < len(self.InitCommands)):
                if(self.InitCommands[self.CommandIndex].startswith("s-op")):
                    self.sendCommand("s-op " + str(Parameters["Mode4"]))
                else:
                    self.sendCommand(self.InitCommands[self.CommandIndex])

                self.CommandIndex = self.CommandIndex + 1
            else:
                self.LastCommand = ""
                self.IsInitalised = True
                self.sendCommand(self.CMD_SET_RX)
        else:
            if("DIO PIN IRQ" in strData):
                self.sendCommand(self.CMD_GET_FIFO)
            elif(self.LastCommand == self.CMD_GET_FIFO):
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
    def getUnitIndex(self):
        unitCount = 0
        for x in Devices:
            deviceId = str(Devices[x].DeviceID)
            if(deviceId.startswith(str(Energine.PRODUCTID_MIHO032))):
                unitCount += 1
            elif(deviceId.startswith(str(Energine.PRODUCTID_MIHO033))):
                unitCount += 1
            elif(deviceId.startswith(str(AxioLogix.PRODUCTID_TEMPHUMIDITY))):
                unitCount += 1
            elif(deviceId.startswith(str(AxioLogix.PRODUCTID_AQS))):
                unitCount += 1
            elif(deviceId.startswith(str(AxioLogix.PRODUCTID_EM))):
                unitCount += 20

        Domoticz.Debug("UnitCount: " + str(unitCount))
        
        return unitCount

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
        except OpenThings.OpenThingsException as error:
            errorMessage = str(error)
            if("bad CRC" not in errorMessage):
                Domoticz.Error("Unable to decode payload: " + errorMessage)

    def handleMessage(self, message):
        Domoticz.Log(str(message))
        header = message["header"]
        sensorId = header["sensorid"]
        productId = header["productid"]
        manufacturerId = header["mfrid"]

        device = self.findDevice(Common.createDeviceId(productId, sensorId))

        Domoticz.Log("Device: " + str(device))
        
        if(device is None):
            join = Common.findRecord(message, OpenThings.PARAM_JOIN)
            Domoticz.Log("Join: " + str(join))
            if(join is not None):
                Domoticz.Log("Join Message From SensorId: "+str(sensorId))
                self.addDevice(manufacturerId, sensorId, productId)
        else:
            Domoticz.Log("Updating Device SensorId: "+str(sensorId))
            self.updateDevice(manufacturerId, productId, device, message)

    def findDevice(self, deviceId):
        for x in Devices:
            if(Devices[x].DeviceID == deviceId):
                return Devices[x]

    def addDevice(self, manufacturerId, sensorId, productId):
        if(manufacturerId == Energine.MFRID_ENERGENIE):
            self.UnitIndex = Energine.createDevice(sensorId, productId, self.UnitIndex)
        elif(manufacturerId == AxioLogix.MFRID_AXIOLOGIX):
            self.UnitIndex = AxioLogix.createDevice(sensorId, productId, self.UnitIndex)
        else:
            Domoticz.Error("Unknown Sensor Id: " +
                           str(sensorId) + " Product Id: " + str(productId))

    def updateDevice(self, manufacturerId, productId, device, message):
        if(manufacturerId == Energine.MFRID_ENERGENIE):
            Energine.updateDevice(device, productId, message)
        elif(manufacturerId == AxioLogix.MFRID_AXIOLOGIX):
            AxioLogix.updateDevice(device, productId, message)


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

def onDeviceRemoved(Unit):
    Domoticz.Debug("Device Removed: " + str(Unit))
    # Generic helper functions


def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
