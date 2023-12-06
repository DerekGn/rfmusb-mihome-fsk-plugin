# axiologix_energy_meter.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import DeviceTypes
import OpenThings
import Common

PRODUCTID_EM = 0x03

def createEnergyMeterSensor(deviceId):
    Domoticz.Log("Creating Energy Meter Sensor Id: " + deviceId)
    Domoticz.Unit(Name="Energy Meter Voltage", DeviceID=deviceId, Unit=1,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;VAC'},
                    Description="Rms Voltage").Create()
    Domoticz.Unit(Name="Energy Meter Frequency", DeviceID=deviceId, Unit=2,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;Hz'},
                    Description="Line Voltage Frequency").Create()

    unitIndex = createLineMeasurements(deviceId, 3,  'L')
    unitIndex = createLineMeasurements(deviceId, unitIndex, 'N')
    createEnergyMeasurements(deviceId, unitIndex)

def createLineMeasurements(deviceId, unitIndex, line):
    Domoticz.Log("Creating Energy Meter Sensor Id: " + str(deviceId) + " Line Measurements " + line)
    Domoticz.Unit(Name="Energy Meter " + line + " Current", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;Irms'},
                    Description=line + " Line Rms Current").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter " + line + " Phase", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;°'},
                    Description="Phase Angle between Voltage and " + line + " Line Current").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter " + line + " PMean", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;kW'},
                    Description=line + " Line Mean Active Power").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter " + line + " QMean", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;kvar'},
                    Description=line + " Line Mean Reactive Power").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter " + line + "Power Factor", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                    Description=line + " Line Power Factor").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter " + line + " SMean", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                    Options={'Custom': '1;kVA'},
                    Description=line + " Line Mean Apparent Power").Create()
    return unitIndex

def createEnergyMeasurements(deviceId, unitIndex):
    Domoticz.Log("Creating Energy Meter Sensor Id: " + str(deviceId) + " Energy Measurements")
    Domoticz.Unit(Name="Energy Meter Absolute Active Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_COUNTER_INC,
                    Description="Energy Meter Absolute Active Energy").Create()
    unitIndex += 1                    
    Domoticz.Unit(Name="Energy Meter Absolute Reactive Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_COUNTER_INC,
                    Description="Energy Meter Absolute Reactive Energy").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter Forward Active Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_COUNTER_INC,
                    Description="Energy Meter Forward Active Energy").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter Forward Reactive Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_COUNTER_INC,
                    Description="Energy Meter Forward Reactive Energy").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter Reverse Active Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_COUNTER_INC,
                    Description="Energy Meter Reverse Active Energy").Create()
    unitIndex += 1
    Domoticz.Unit(Name="Energy Meter Reverse Reactive Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                    Subtype=DeviceTypes.DEVICE_SUB_TYPE_COUNTER_INC,
                    Description="Energy Meter Reverse Reactive Energy").Create()
    
    return unitIndex

def updateEnergyMeterSensor(deviceId, devices, message, rssi):
    Domoticz.Log("Updating Energy Meter Sensor Id: " + str(deviceId))
    voltageRecord = Common.findRecord(message, OpenThings.PARAM_VOLTAGE)
    freqRecord = Common.findRecord(message, OpenThings.PARAM_FREQUENCY)

    voltage = round(voltageRecord["value"], 2)
    frequency = round(freqRecord["value"], 2)

    Domoticz.Debug("Updating Energy Meter Sensor Id: [" + str(deviceId)
                       + "] Voltage: [" + str(voltage)
                       + "] frequency: [" + str(frequency)
                       + "]")

    devices[deviceId].Units[1].nValue = voltage
    devices[deviceId].Units[1].sValue = str(voltage)
    devices[deviceId].Units[1].Update(Log=True)

    devices[deviceId].Units[2].nValue = frequency
    devices[deviceId].Units[2].sValue = str(frequency)
    devices[deviceId].Units[2].Update(Log=True)

    iRecord_L = Common.findRecord(message, OpenThings.PARAM_CURRENT_L)
    phaseRecord_L = Common.findRecord(message, OpenThings.PARAM_PHASE_ANGLE_L)
    activePowerRecord_L = Common.findRecord(message, OpenThings.PARAM_ACTIVE_POWER_L)
    powerFactorRecord_L = Common.findRecord(message, OpenThings.PARAM_POWER_FACTOR_L)
    reactivePowerRecord_L = Common.findRecord(message, OpenThings.PARAM_REACTIVE_POWER_L)
    apparentPowerRecord_L = Common.findRecord(message, OpenThings.PARAM_APPARENT_POWER_L)

    unitIndex = updateLineMeasurements(devices, iRecord_L, phaseRecord_L, activePowerRecord_L,
                           powerFactorRecord_L, reactivePowerRecord_L, apparentPowerRecord_L, 3)

    iRecord_N = Common.findRecord(message, OpenThings.PARAM_CURRENT_N)
    phaseRecord_N = Common.findRecord(message, OpenThings.PARAM_PHASE_ANGLE_N)
    activePowerRecord_N = Common.findRecord(message, OpenThings.PARAM_ACTIVE_POWER_N)
    powerFactorRecord_N = Common.findRecord(message, OpenThings.PARAM_POWER_FACTOR_N)
    reactivePowerRecord_N = Common.findRecord(message, OpenThings.PARAM_REACTIVE_POWER_N)
    apparentPowerRecord_N = Common.findRecord(message, OpenThings.PARAM_APPARENT_POWER_N)

    unitIndex = updateLineMeasurements(devices, iRecord_N, phaseRecord_N, activePowerRecord_N,
                            powerFactorRecord_N, reactivePowerRecord_N, apparentPowerRecord_N, unitIndex)

    updateEnergyMeasurements(devices, message, unitIndex)

def updateLineMeasurements(devices, currentRecord, phaseRecord, activePowerRecord,
                           powerFactorRecord, reactivePowerRecord, apparentPowerRecord, unitIndex):
    # Current
    devices[deviceId].Units[unitIndex].nValue=round(currentRecord["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Phase
    devices[deviceId].Units[unitIndex].nValue=round(phaseRecord["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Mean Active Power
    devices[deviceId].Units[unitIndex].nValue=round(activePowerRecord["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Mean Reactive Power
    devices[deviceId].Units[unitIndex].nValue=round(reactivePowerRecord["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Power Factor
    devices[deviceId].Units[unitIndex].nValue=round(powerFactorRecord["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Apparent Power
    devices[deviceId].Units[unitIndex].nValue=round(apparentPowerRecord["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1

    return unitIndex

def updateEnergyMeasurements(device, message, unitIndex):
    # Absolute Active Energy
    record = Common.findRecord(
        message, OpenThings.PARAM_ABS_ACTIVE_ENERGY)
    devices[deviceId].Units[unitIndex].nValue=round(record["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Absolute Reactive Energy
    record = Common.findRecord(
        message, OpenThings.PARAM_ABS_REACTIVE_ENERGY)
    devices[deviceId].Units[unitIndex].nValue=round(record["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Forward Active Energy
    record = Common.findRecord(
        message, OpenThings.PARAM_FWD_ACTIVE_ENERGY)
    devices[deviceId].Units[unitIndex].nValue=round(record["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Forward Reactive Energy
    record = Common.findRecord(
        message, OpenThings.PARAM_FWD_REACTIVE_ENERGY)
    devices[deviceId].Units[unitIndex].nValue=round(record["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Reverse Active Energy
    record = Common.findRecord(
        message, OpenThings.PARAM_REV_ACTIVE_ENERGY)
    devices[deviceId].Units[unitIndex].nValue=round(record["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1
    # Reverse Reactive Energy
    record = Common.findRecord(
        message, OpenThings.PARAM_REV_REACTIVE_ENERGY)
    devices[deviceId].Units[unitIndex].nValue=round(record["value"],2)
    devices[deviceId].Units[unitIndex].Update()
    unitIndex += 1