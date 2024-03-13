# axiologix_energy_meter.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import Types
import SubTypes
import OpenThings
import Common

PRODUCTID_EM = 0x03

PARAM_CURRENT_L = 0x06
PARAM_PHASE_ANGLE_L = 0x07
PARAM_ACTIVE_POWER_L = 0x08
PARAM_POWER_FACTOR_L = 0x09
PARAM_REACTIVE_POWER_L = 0x0A
PARAM_APPARENT_POWER_L = 0x0B
PARAM_CURRENT_N = 0x0C
PARAM_PHASE_ANGLE_N = 0x0D
PARAM_ACTIVE_POWER_N = 0x0E
PARAM_POWER_FACTOR_N = 0x0F
PARAM_REACTIVE_POWER_N = 0x10
PARAM_APPARENT_POWER_N = 0x11
PARAM_ABS_ACTIVE_ENERGY = 0x12
PARAM_ABS_REACTIVE_ENERGY = 0x13
PARAM_FWD_ACTIVE_ENERGY = 0x14
PARAM_FWD_REACTIVE_ENERGY = 0x15
PARAM_REV_ACTIVE_ENERGY = 0x16
PARAM_REV_REACTIVE_ENERGY = 0x17

def createEnergyMeterSensor(deviceId):
    Domoticz.Log("Creating Energy Meter Sensor Id: " + deviceId)
    Domoticz.Unit(Name="Energy Meter Voltage", DeviceID=deviceId, Unit=1,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;VAC'},
                    Description="Rms Voltage").Create()
    Domoticz.Unit(Name="Energy Meter Frequency", DeviceID=deviceId, Unit=2,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;Hz'},
                    Description="Line Voltage Frequency").Create()

    createLineMeasurements(deviceId, 3,  'L')
    createLineMeasurements(deviceId, 9, 'N')
    createEnergyMeasurements(deviceId, 15)

def createLineMeasurements(deviceId, unitId, line):
    Domoticz.Log("Creating Energy Meter Sensor Id: " + str(deviceId) + " Line Measurements " + line)
    Domoticz.Unit(Name="Energy Meter " + line + " Current", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;Irms'},
                    Description=line + " Line Rms Current").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter " + line + " Phase", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;°'},
                    Description="Phase Angle between Voltage and " + line + " Line Current").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter " + line + " Power Factor", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Description=line + " Line Power Factor").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter " + line + " P Mean", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;kW'},
                    Description=line + " Line Mean Active Power").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter " + line + " Q Mean", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;kvar'},
                    Description=line + " Line Mean Reactive Power").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter " + line + " S Mean", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;kVA'},
                    Description=line + " Line Mean Apparent Power").Create()

def createEnergyMeasurements(deviceId, unitId):
    Domoticz.Log("Creating Energy Meter Sensor Id: " + str(deviceId) + " Energy Measurements")
    Domoticz.Unit(Name="Energy Meter Absolute Active Energy", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;KWh'},
                    Description="Energy Meter Absolute Active Energy").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter Absolute Reactive Energy", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;KWh'},
                    Description="Energy Meter Absolute Reactive Energy").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter Forward Active Energy", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;KWh'},
                    Description="Energy Meter Forward Active Energy").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter Forward Reactive Energy", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;KWh'},
                    Description="Energy Meter Forward Reactive Energy").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter Reverse Active Energy", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;KWh'},
                    Description="Energy Meter Reverse Active Energy").Create()
    unitId += 1
    Domoticz.Unit(Name="Energy Meter Reverse Reactive Energy", DeviceID=deviceId, Unit=unitId,
                    Type=Types.TYPE_GENERAL,
                    Subtype=SubTypes.SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;KWh'},
                    Description="Energy Meter Reverse Reactive Energy").Create()

def updateEnergyMeterSensor(deviceId, devices, message, rssi):
    Domoticz.Log("Updating Energy Meter Sensor Id: " + str(deviceId))
    
    device = devices[deviceId]

    voltageRecord = Common.findRecord(message, OpenThings.PARAM_VOLTAGE)
    freqRecord = Common.findRecord(message, OpenThings.PARAM_FREQUENCY)

    voltageRaw = voltageRecord["value"]
    frequencyRaw = freqRecord["value"]

    voltage = round(voltageRaw / 100.0, 2)
    frequency = round(frequencyRaw / 100.0, 2)

    Domoticz.Debug("Updating Energy Meter Sensor Id: [" + str(deviceId)
                       + "] Voltage: [" + str(voltage)
                       + "] frequency: [" + str(frequency)
                       + "]")

    device.Units[1].nValue = voltage
    device.Units[1].sValue = str(voltage)
    device.Units[1].SignalLevel = rssi
    device.Units[1].Update(Log=True)

    device.Units[2].nValue = frequency
    device.Units[2].sValue = str(frequency)
    device.Units[2].SignalLevel = rssi
    device.Units[2].Update(Log=True)

    iRecord_L = Common.findRecord(message, PARAM_CURRENT_L)
    phaseRecord_L = Common.findRecord(message, PARAM_PHASE_ANGLE_L)
    powerFactorRecord_L = Common.findRecord(message, PARAM_POWER_FACTOR_L)
    activePowerRecord_L = Common.findRecord(message, PARAM_ACTIVE_POWER_L)
    reactivePowerRecord_L = Common.findRecord(message, PARAM_REACTIVE_POWER_L)
    apparentPowerRecord_L = Common.findRecord(message, PARAM_APPARENT_POWER_L)

    updateLineMeasurements(device, iRecord_L, phaseRecord_L, activePowerRecord_L,
                           powerFactorRecord_L, reactivePowerRecord_L, apparentPowerRecord_L, 3, rssi)

    iRecord_N = Common.findRecord(message, PARAM_CURRENT_N)
    phaseRecord_N = Common.findRecord(message, PARAM_PHASE_ANGLE_N)
    powerFactorRecord_N = Common.findRecord(message, PARAM_POWER_FACTOR_N)
    activePowerRecord_N = Common.findRecord(message, PARAM_ACTIVE_POWER_N)
    reactivePowerRecord_N = Common.findRecord(message, PARAM_REACTIVE_POWER_N)
    apparentPowerRecord_N = Common.findRecord(message, PARAM_APPARENT_POWER_N)

    updateLineMeasurements(device, iRecord_N, phaseRecord_N, activePowerRecord_N,
                          powerFactorRecord_N, reactivePowerRecord_N, apparentPowerRecord_N, 6, rssi)

    updateEnergyMeasurements(device, message, 15, rssi)

def updateLineMeasurements(device, currentRecord, phaseRecord, activePowerRecord,
                           powerFactorRecord, reactivePowerRecord, apparentPowerRecord, unitId, rssi):
    # Current
    if(currentRecord["length"] != 0):
        Domoticz.Log("Current Updating")
        device.Units[unitId].sValue=str(round(currentRecord["value"] / 1000.0, 3))
    else:
        device.Units[unitId].sValue="0"
    device.Units[unitId].SignalLevel = rssi
    device.Units[unitId].Update()
    unitId += 1
    # Phase
    if(phaseRecord["length"] != 0):
        device.Units[unitId].sValue=str(round(phaseRecord["value"] / 10.0, 1))
    else:
        device.Units[unitId].sValue="0"    
    device.Units[unitId].SignalLevel = rssi
    device.Units[unitId].Update()
    unitId += 1
    # Power Factor
    if(powerFactorRecord["length"] != 0):
        device.Units[unitId].sValue=str(round(powerFactorRecord["value"] / 1000.0, 3))
    else:
        device.Units[unitId].sValue="0"
    device.Units[unitId].SignalLevel = rssi
    device.Units[unitId].Update()
    unitId += 1
    # Mean Active Power
    if(activePowerRecord["length"] != 0):
        device.Units[unitId].sValue=str(round(activePowerRecord["value"] / 1000.0, 3))
    else:
        device.Units[unitId].sValue="0"
    device.Units[unitId].SignalLevel = rssi
    device.Units[unitId].Update()
    unitId += 1
    # Mean Reactive Power
    if(reactivePowerRecord["length"] != 0):
        device.Units[unitId].sValue=str(round(reactivePowerRecord["value"] / 1000.0, 3))
    else:
        device.Units[unitId].sValue="0"

    device.Units[unitId].SignalLevel = rssi
    device.Units[unitId].Update()
    unitId += 1
    # Apparent Power
    if(apparentPowerRecord["length"] != 0):
        device.Units[unitId].sValue=str(round(apparentPowerRecord["value"], 3))
    else:
        device.Units[unitId].sValue="0"
    device.Units[unitId].SignalLevel = rssi
    device.Units[unitId].Update()

def updateEnergyMeasurements(device, message, unitId, rssi):
    # Absolute Active Energy
    record = Common.findRecord(message, PARAM_ABS_ACTIVE_ENERGY)
    if(record["length"] != 0):
        device.Units[unitId].sValue=str(round(record["value"] * 0.1, 1))
        device.Units[unitId].SignalLevel = rssi
        device.Units[unitId].nValue=0
        device.Units[unitId].Update()
    unitId += 1
    # Absolute Reactive Energy
    record = Common.findRecord(message, PARAM_ABS_REACTIVE_ENERGY)
    if(record["length"] != 0):
        device.Units[unitId].sValue=str(round(record["value"] * 0.1, 1))
        device.Units[unitId].SignalLevel = rssi
        device.Units[unitId].nValue=0
        device.Units[unitId].Update()
    unitId += 1
    # Forward Active Energy
    record = Common.findRecord(message, PARAM_FWD_ACTIVE_ENERGY)
    if(record["length"] != 0):
        device.Units[unitId].sValue=str(round(record["value"] * 0.1, 1))
        device.Units[unitId].SignalLevel = rssi
        device.Units[unitId].nValue=0
        device.Units[unitId].Update()
    unitId += 1
    # Forward Reactive Energy
    record = Common.findRecord(message, PARAM_FWD_REACTIVE_ENERGY)
    if(record["length"] != 0):
        device.Units[unitId].sValue=str(round(record["value"] * 0.1, 1))
        device.Units[unitId].SignalLevel = rssi
        device.Units[unitId].nValue=0
        device.Units[unitId].Update()
    unitId += 1
    # Reverse Active Energy
    record = Common.findRecord(message, PARAM_REV_ACTIVE_ENERGY)
    if(record["length"] != 0):
        device.Units[unitId].sValue=str(round(record["value"] * 0.1, 1))
        device.Units[unitId].SignalLevel = rssi
        device.Units[unitId].nValue=0
        device.Units[unitId].Update()
    unitId += 1
    # Reverse Reactive Energy
    record = Common.findRecord(message, PARAM_REV_REACTIVE_ENERGY)
    if(record["length"] != 0):
        device.Units[unitId].sValue=str(round(record["value"] * 0.1, 1))
        device.Units[unitId].SignalLevel = rssi
        device.Units[unitId].nValue=0
        device.Units[unitId].Update()
