# AxioLogix.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import Common
import Energine
import OpenThings
import DeviceTypes

MFRID_AXIOLOGIX = 0x55

PRODUCTID_TEMPHUMIDITY = 0x01
PRODUCTID_AQS = 0x02
PRODUCTID_EM = 0x03


def createDevice(deviceId, productId):
    if(productId == PRODUCTID_TEMPHUMIDITY):
        Domoticz.Log("Creating Temp Humidity Sensor Id: " + str(deviceId))
        Domoticz.Unit(Name="Temp Humidity Sensor", DeviceID=deviceId, Unit=1,
                        TypeName="Temp+Hum", Type=DeviceTypes.DEVICE_TYPE_TEMP_HUMIDITY,
                        Description="RfmTemp Sensor", Used=1).Create()
    elif(productId == PRODUCTID_AQS):
        Domoticz.Log("Creating Aqs Sensor Id: " + deviceId)
        Domoticz.Unit(Name="AQS", DeviceID=deviceId, Unit=1,
                        Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                        Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                        Options={'Custom': '1;VOC Index'},
                        Description="RfmAqs Sensor", Used=1).Create()
        Domoticz.Unit(Name="AQS Temp & Humidity", DeviceID=deviceId, Unit=2,
                        TypeName="Temp+Hum", Type=DeviceTypes.DEVICE_TYPE_TEMP_HUMIDITY,
                        Description="RfmAqs Temp & Humidity", Used=1).Create()
    elif(productId == PRODUCTID_EM):
        Domoticz.Log("Creating Energy Meter Sensor Id: " + deviceId)
        Domoticz.Unit(Name="Energy Meter Voltage", DeviceID=deviceId, Unit=1,
                        Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                        Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                        Options={'Custom': '1;VAC'},
                        Description="Rms Voltage", Used=1).Create()
        Domoticz.Unit(Name="Energy Meter Frequency", DeviceID=deviceId, Unit=2,
                        Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                        Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                        Options={'Custom': '1;Hz'},
                        Description="Line Voltage Frequency", Used=1).Create()

        unitIndex = createLineMeasurements(deviceId, 3,  'L')
        unitIndex = createLineMeasurements(deviceId, unitIndex, 'n')
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

def updateDevice(deviceId, devices, productId, message):
    if(productId == PRODUCTID_TEMPHUMIDITY):
        updateTemperatureHumiditySensor(deviceId, devices, message)
    elif(productId == PRODUCTID_AQS):
        updateAqsSensor(deviceId, devices, message)
    elif(productId == PRODUCTID_EM):
        updateEnergyMeterSensor(deviceId, devices, message)

def updateTemperatureHumiditySensor(deviceId, devices, message):
    Domoticz.Log("Updating Temperature Humidity Sensor Id: " + str(deviceId))
    batteryRecord = Common.findRecord(message, OpenThings.PARAM_BATTERY_LEVEL)
    temperatureRecord = Common.findRecord(message, OpenThings.PARAM_TEMPERATURE)
    humidityRecord = Common.findRecord(message, OpenThings.PARAM_RELATIVE_HUMIDITY)

    temperature = round(temperatureRecord["value"], 2)
    humidity = round(humidityRecord["value"], 2)
    batteryLevel = batteryRecord["value"]

    Domoticz.Debug("Updating TempHumidity Sensor Id: [" + str(deviceId)
                       + "] Temperature: [" + str(temperature)
                       + "] Humidity: [" + str(humidity)
                       + "] Battery Level: [" + str(batteryLevel) + "]")
    
    devices[deviceId].Units[1].nValue = temperature
    devices[deviceId].Units[1].sValue = str(temperature) + ";" + str(humidity)
    devices[deviceId].Units[1].BatteryLevel = batteryLevel
    devices[deviceId].Units[1].Update(Log=True)

def updateAqsSensor(deviceId, devices, message):
    Domoticz.Log("Updating AQS Sensor Id: " + str(deviceId))
    batteryRecord = Common.findRecord(message, OpenThings.PARAM_BATTERY_LEVEL)
    temperatureRecord = Common.findRecord(message, OpenThings.PARAM_TEMPERATURE)
    humidityRecord = Common.findRecord(message, OpenThings.PARAM_RELATIVE_HUMIDITY)
    vocRecord = Common.findRecord(message, OpenThings.PARAM_VOC_INDEX)

    temperature = round(temperatureRecord["value"], 2)
    humidity = round(humidityRecord["value"], 2)
    vocIndex = round(vocRecord["value"], 2)
    batteryLevel = batteryRecord["value"]
    
    Domoticz.Debug("Updating AQS Sensor Id: [" + str(deviceId)
                       + "] AQS Index: [" + str(vocIndex)
                       + "] Temperature: [" + str(temperature)
                       + "] Humidity: [" + str(humidity)
                       + "] Battery Level: [" + str(batteryLevel) + "]")

    devices[deviceId].Units[1].nValue = vocIndex
    devices[deviceId].Units[1].sValue = str(vocIndex)
    devices[deviceId].Units[1].BatteryLevel = batteryLevel
    devices[deviceId].Units[1].Update(Log=True)

    devices[deviceId].Units[2].nValue = temperature
    devices[deviceId].Units[2].sValue = str(temperature) + ";" + str(humidity)
    devices[deviceId].Units[2].Update(Log=True)
    
def updateEnergyMeterSensor(deviceId, devices, message):
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

def findDeviceByType(devices, deviceType):
    for x in devices:
        if(x.Type == deviceType):
            return x
