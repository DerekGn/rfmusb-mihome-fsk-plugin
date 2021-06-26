# AxioLogix.py
#
# Author: DerekGn
#
import Common
import Domoticz
import Energine
import OpenThings

MFRID_AXIOLOGIX = 0x55

PRODUCTID_TEMPHUMIDITY = 0x01
PRODUCTID_AQS = 0x02
PRODUCTID_EM = 0x03

def createDevice(deviceId, productId, unitIndex):
    if(productId == PRODUCTID_TEMPHUMIDITY):
        unitIndex += 1
        Domoticz.Log("Creating Temp Humidity Sensor Id: " + deviceId + " Unit Id: " + str(unitIndex))
        Domoticz.Device(Name="Temp Humidity Sensor", DeviceID=deviceId, Unit=unitIndex,
                        TypeName="Temp+Hum", Type=82,
                        Description="RfmTemp Sensor").Create()
    elif(productId == PRODUCTID_AQS):
        unitIndex += 1
        Domoticz.Log("Creating Aqs Sensor Id: " + deviceId + " Unit Id: " + str(unitIndex))
        Domoticz.Device(Name="AQS", DeviceID=deviceId, Unit=unitIndex,
                        Type=243, Subtype=31,
                        Options={'Custom': '1;VOC Index'},
                        Description="RfmAqs Sensor").Create()
        unitIndex += 1
        Domoticz.Device(Name="AQS Temp & Humidity", DeviceId=deviceId, Unit=unitIndex,
                        TypeName="Temp+Hum", Type=82,
                        Description="RfmAqs Temp & Humidity").Create()
    elif(productId == PRODUCTID_EM):
        unitIndex += 1
        Domoticz.Log("Creating Energy Meter Sensor Id: " + deviceId + " Unit Id: " + str(unitIndex))
        Domoticz.Device(Name="Energy Meter Voltage", DeviceID=deviceId, Unit=unitIndex,
                        Type=243, Subtype=31,
                        Options={'Custom': '1;VAC'},
                        Description="Rms Voltage").Create()
        unitIndex += 1
        Domoticz.Device(Name="Energy Meter Frequency", DeviceID=deviceId, Unit=unitIndex,
                        Type=243, Subtype=31,
                        Options={'Custom': '1;Hz'},
                        Description="Line Voltage Frequency").Create()
        
        unitIndex = createLineMeasurements('L', deviceId, unitIndex)
        unitIndex = createLineMeasurements('n', deviceId, unitIndex)
        unitIndex = createEnergyMeasurements(deviceId, unitIndex)

        return unitIndex


def createLineMeasurements(line, deviceId, unitIndex):
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter " + line + " Current", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;Irms'},
                    Description=line + " Line Rms Current").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter " + line + " Phase", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;°'},
                    Description="Phase Angle between Voltage and " + line + " Line Current").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter " + line + " PMean", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;kW'},
                    Description=line + " Line Mean Active Power").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter " + line + " QMean", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;kvar'},
                    Description=line + " Line Mean Reactive Power").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter " + line + "Power Factor", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=31,
                    Description=line + " Line Power Factor").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter " + line + " SMean", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;kVA'},
                    Description=line + " Line Mean Apparent Power").Create()

    return unitIndex

def createEnergyMeasurements(deviceId, unitIndex):
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter Absolute Active Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=28,
                    Description="Energy Meter Absolute Active Energy").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter Absolute Reactive Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=28,
                    Description="Energy Meter Absolute Reactive Energy").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter Forward Active Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=28,
                    Description="Energy Meter Forward Active Energy").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter Forward Reactive Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=28,
                    Description="Energy Meter Forward Reactive Energy").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter Reverse Active Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=28,
                    Description="Energy Meter Reverse Active Energy").Create()
    unitIndex += 1
    Domoticz.Device(Name="Energy Meter Reverse Reactive Energy", DeviceID=deviceId, Unit=unitIndex,
                    Type=243, Subtype=28,
                    Description="Energy Meter Reverse Reactive Energy").Create()

    return unitIndex

def updateDevice(device, productId, message):
    if(productId == PRODUCTID_TEMPHUMIDITY):
        Domoticz.Log("Updating TempHumidity Sensor Id: " + str(device.ID))
        temperatureRecord = Common.findRecord(
            message, OpenThings.PARAM_TEMPERATURE)
        batteryRecord = Common.findRecord(
            message, OpenThings.PARAM_BATTERY_LEVEL)
        humidityRecord = Common.findRecord(
            message, OpenThings.PARAM_RELATIVE_HUMIDITY)

        humidity = ((125.0 * humidityRecord["value"]) / 65536.0) - 6

        temperature = ((175.72 * temperatureRecord["value"]) / 65536.0) - 46.85

        device[1].Update(nValue=0, sValue=temperature + ";" +
                         humidity, BatteryLevel=batteryRecord["value"])
    elif(productId == PRODUCTID_AQS):
        Domoticz.Log("Updating AQS Sensor Id: " + str(device.ID))
        temperatureRecord = Common.findRecord(
            message, OpenThings.PARAM_TEMPERATURE)
        batteryRecord = Common.findRecord(
            message, OpenThings.PARAM_BATTERY_LEVEL)
        humidityRecord = Common.findRecord(
            message, OpenThings.PARAM_RELATIVE_HUMIDITY)
        vocRecord = Common.findRecord(
            message, OpenThings.PARAM_VOC_INDEX)

        humidity = humidityRecord["value"] * 0.001

        temperature = temperatureRecord["value"] * 0.001

        batteryLevel = batteryRecord["value"]

        device[1].Update(nValue=0, sValue=vocRecord["value"],
                         BatteryLevel=batteryLevel)
        device[2].Update(nValue=0, sValue=temperature + ";" +
                         humidity, BatteryLevel=batteryRecord["value"])
    elif(productId == PRODUCTID_EM):
        Domoticz.Log("Updating Energy Meter Id: " + str(device.ID))
        voltageRecord = Common.findRecord(message, OpenThings.PARAM_VOLTAGE)
        freqRecord = Common.findRecord(message, OpenThings.PARAM_FREQUENCY)

        device[1].Update(sValue=voltageRecord["value"] / 100.0)
        device[2].Update(nValue=freqRecord["value"] / 100.0)

        iRecord_L = Common.findRecord(message, OpenThings.PARAM_CURRENT_L)
        phaseRecord_L = Common.findRecord(
            message, OpenThings.PARAM_PHASE_ANGLE_L)
        activePowerRecord_L = Common.findRecord(
            message, OpenThings.PARAM_ACTIVE_POWER_L)
        powerFactorRecord_L = Common.findRecord(
            message, OpenThings.PARAM_POWER_FACTOR_L)
        reactivePowerRecord_L = Common.findRecord(
            message, OpenThings.PARAM_REACTIVE_POWER_L)
        apparentPowerRecord_L = Common.findRecord(
            message, OpenThings.PARAM_APPARENT_POWER_L)

        updateLineMeasurements(device, iRecord_L, phaseRecord_L, activePowerRecord_L,
                               powerFactorRecord_L, reactivePowerRecord_L, apparentPowerRecord_L, 3)

        iRecord_N = Common.findRecord(message, OpenThings.PARAM_CURRENT_N)
        phaseRecord_N = Common.findRecord(
            message, OpenThings.PARAM_PHASE_ANGLE_N)
        activePowerRecord_N = Common.findRecord(
            message, OpenThings.PARAM_ACTIVE_POWER_N)
        powerFactorRecord_N = Common.findRecord(
            message, OpenThings.PARAM_POWER_FACTOR_N)
        reactivePowerRecord_N = Common.findRecord(
            message, OpenThings.PARAM_REACTIVE_POWER_N)
        apparentPowerRecord_N = Common.findRecord(
            message, OpenThings.PARAM_APPARENT_POWER_N)

        updateLineMeasurements(device, iRecord_N, phaseRecord_N, activePowerRecord_N,
                               powerFactorRecord_N, reactivePowerRecord_N, apparentPowerRecord_N, 9)

        updateEnergyMeasurements(device, message)


def updateLineMeasurements(device, currentRecord, phaseRecord, activePowerRecord,
                           powerFactorRecord, reactivePowerRecord, apparentPowerRecord, unit):
    # Current
    device[unit].Update(nValue=currentRecord["value"] / 1000.0)
    # Phase
    device[unitIndex].Update(nValue=phaseRecord["value"] / 10.0)
    # Mean Active Power
    device[unitIndex].Update(nValue=activePowerRecord["value"] / 1000.0)
    # Mean Reactive Power
    device[unitIndex].Update(nValue=reactivePowerRecord["value"] / 1000.0)
    # Power Factor
    device[unitIndex].Update(nValue=powerFactorRecord["value"] / 1000.0)
    # Apparent Power
    device[unitIndex].Update(nValue=apparentPowerRecord["value"] / 1000.0)

def updateEnergyMeasurements(device, message):
    # Absolute Active Energy
    activeEnergy = Common.findRecord(message, OpenThings.PARAM_ABS_ACTIVE_ENERGY)
    device[15].Update(nValue=activeEnergy["Value"])
    # Absolute Reactive Energy
    reactiveEnergy = Common.findRecord(message, OpenThings.PARAM_ABS_REACTIVE_ENERGY)
    device[16].Update(nValue=reactiveEnergy["Value"])
    # Forward Active Energy
    fwdActiveEnergy = Common.findRecord(message, OpenThings.PARAM_FWD_ACTIVE_ENERGY)
    device[17].Update(nValue=fwdActiveEnergy["Value"])
    # Forward Reactive Energy
    fwdReactiveEnergy = Common.findRecord(message, OpenThings.PARAM_FWD_REACTIVE_ENERGY)
    device[18].Update(nValue=fwdReactiveEnergy["Value"])
    # Reverse Active Energy
    revActiveEnergy = Common.findRecord(message, OpenThings.PARAM_REV_ACTIVE_ENERGY)
    device[19].Update(nValue=revActiveEnergy["Value"])
    # Reverse Reactive Energy
    revReactiveEnergy = Common.findRecord(message, OpenThings.PARAM_REV_REACTIVE_ENERGY)
    device[20].Update(nValue=revReactiveEnergy["Value"])