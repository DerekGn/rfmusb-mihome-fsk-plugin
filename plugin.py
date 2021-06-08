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


class BasePlugin:

    CMD_GET_FIRMWARE_VERSION = "g-fv"
    CMD_EXECUTE_TX = "e-tx "
    COMMAND_RESULT_OK = "OK"

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
        "s-di 1"
    ]

    LastCommand = ""
    CommandIndex = 0
    SerialConn = None
    IsInitalised = False
    FifoRead = False

    def __init__(self):
        return

    def onStart(self):
        OpenThings.init(0)
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
            self.SendCommand(self.CMD_GET_FIRMWARE_VERSION)
        else:
            Domoticz.Log("Failed to connect ("+str(Status) +
                         ") to: "+Parameters["SerialPort"])

            Domoticz.Debug("Failed to connect ("+str(Status)+") to: " +
                           Parameters["SerialPort"]+" with error: "+Description)
        return True

    def onMessage(self, Connection, Data):
        strData = Data.decode("ascii")
        strData = strData.replace("\n", "")

        Domoticz.Log(
            "Command Executed: ["+self.LastCommand+"] Respose: ["+strData+"] ")

        if(self.IsInitalised == False and self.LastCommand.startswith("s-op")):
            self.IsInitalised = True

        if(self.IsInitalised == False):
            if(self.CommandIndex < len(self.InitCommands)):
                self.SendCommand(self.InitCommands[self.CommandIndex])
                self.CommandIndex = self.CommandIndex + 1
            else:
                # Append setting of power command to initalisation
                self.SendCommand("s-op " + str(Parameters["Mode4"]))

        if(strData.startswith("DIO PIN IRQ")):
            # Read the FIFO
            self.SendCommand("g-fifo")
            self.FifoRead = True

        if(self.FifoRead == True):
            # Decode the fifo data
            self.DecodeAndProcessFifoData(strData)

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
    def SendCommand(self, Command):
        self.LastCommand = Command
        self.SerialConn.Send(Command + "\n")

    def DecodeAndProcessFifoData(self, data):
        payload = bytearray(data.decode('hex'))
        try:
            message = OpenThings.decode(payload)
            self.handle_message(message)
        except OpenThings.OpenThingsException:
            Domoticz.Error("Unable to decode payload:%s" % payload)

    def HandleMessage(self, message):
        for rec in message["recs"]:
            paramid = rec["paramid"]
            if paramid == OpenThings.PARAM_JOIN:
                self.HandleSensorJoin(message)

    def HandleSensorJoin(self, message):
        header = message["header"]
        sensorId = header["sensorid"]
        Domoticz.Log("Join Message From SensorId '"+str(sensorId)+"'.")
        device = self.FindDevice(sensorId)
        if(device is None):
            self.AddDevice(message)

    def FindDevice(self, sensorId):
        for x in Devices:
            if(Devices[x].ID == sensorId):
                return Devices[x]

    def AddDevice(self, message):
        header = message["header"]
        sensorId = header["sensorid"]
        productId = header["productid"]
        manufacturerId = header["mfrid"]
        address = (manufacturerId, productId, sensorId)
        if(manufacturerId == Energine.MFRID_ENERGENIE):
            self.AddEnergineDevice(address, sensorId, productId)
        elif(manufacturerId == AxioLogix.MFRID_AXIOLOGIX):
            self.AddAxioLogixDevice(address, sensorId, productId)
        else:
            Domoticz.Error("Unknown Sensor Id: " +
                           str(sensorId) + " Product Id: " + str(productId))

    def AddEnergineDevice(self, address, sensorId, productId):
        if(productId == Energine.PRODUCTID_MIHO032):
            Domoticz.Log("Creating Motion Sensor Id: " + str(sensorId))
            Domoticz.Device(Name="Motion Sensor", Unit=address,
                            TypeName="Switch", Type=244, Subtype=62, Switchtype=8).Create()
        elif(productId == Energine.PRODUCTID_MIHO033):
            Domoticz.Log("Creating Door Sensor Id: " + str(sensorId))
            Domoticz.Device(Name="Door Sensor", Unit=address,
                            TypeName="Switch", Type=244, Subtype=73, Switchtype=11).Create()

    def AddAxioLogixDevice(self, address, sensorId, productId):
        if(productId == AxioLogix.PRODUCTID_TEMPHUMIDITY):
            Domoticz.Log("Creating Temp Humidity Sensor Id: " + str(sensorId))
            Domoticz.Device(Name="Temp Humidity Sensor", Unit=address,
                            TypeName="Temp+Hum", Type=82).Create()
        elif(productId == Energine.PRODUCTID_AQS):
            Domoticz.Log("Creating Aqs Sensor Id: " + str(sensorId))
            Domoticz.Device(Name="Air Quality Sensor", Unit=address,
                            TypeName="Air Quality", Type=249).Create()
        # elif(productId == Energine.PRODUCTID_EM):
        #     Domoticz.Log("Creating Energy Meter Id: " + str(sensorId))
        #     


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
