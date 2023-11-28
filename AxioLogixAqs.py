# AxioLogixAqs.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import DeviceTypes
import OpenThings
import Common

PRODUCTID_AQS = 0x02

IAQ_UNIT = 1
INDEX_UNIT = 2
TVOC_UNIT = 3
ETOH_UNIT = 4
ECO2_UNIT = 5
TEMP_HUM_UNIT = 6
VBATT_UNIT = 7

AIR_QUALITY_LEVEL_LIMIT = [1.9,2.9,3.9,4.9,5]
AIR_QUALITY_LEVEL_CONDITION = ["Very Good","Good","Medium","Poor","Bad"]

def createAqsSensor(deviceId):
    Domoticz.Log("Creating Aqs Sensor Id: " + deviceId)
    Domoticz.Unit(Name="IAQ", DeviceID=deviceId, Unit=IAQ_UNIT,
                  Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                  Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                  Options={'Custom': '1;IAQ'},
                  Description="RfmAqs Sensor IAQ").Create()
    Domoticz.Unit(Name="Index", DeviceID=deviceId, Unit=INDEX_UNIT,
                  TypeName="Alert",
                  Description="RfmAqs Sensor IAQ").Create()
    Domoticz.Unit(Name="TVOC", DeviceID=deviceId, Unit=TVOC_UNIT,
                  Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                  Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                  Options={'Custom': '1;mg/m^3'},
                  Description="RfmAqs Sensor TVOC").Create()
    Domoticz.Unit(Name="ETOH", DeviceID=deviceId, Unit=ETOH_UNIT,
                  Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                  Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                  Options={'Custom': '1;ppm'},
                  Description="RfmAqs Sensor ETOH").Create()
    Domoticz.Unit(Name="ECO2", DeviceID=deviceId, Unit=ECO2_UNIT,
                  Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                  Subtype=DeviceTypes.DEVICE_SUB_TYPE_CUSTOM,
                  Options={'Custom': '1;ppm'},
                  Description="RfmAqs Sensor ECO2").Create()
    Domoticz.Unit(Name="AQS Temp & Humidity", DeviceID=deviceId, Unit=TEMP_HUM_UNIT,
                  TypeName="Temp+Hum", Type=DeviceTypes.DEVICE_TYPE_TEMP_HUMIDITY,
                  Description="RfmAqs Temp & Humidity").Create()
    Domoticz.Unit(Name="BatteryVoltage", DeviceID=deviceId, Unit=VBATT_UNIT,
                  Type=DeviceTypes.DEVICE_TYPE_GENERAL,
                  Subtype=DeviceTypes.DEVICE_SUB_TYPE_VOLTAGE,
                  Description="RfmAqs Sensor Battery Voltage").Create()

def updateAqsSensor(deviceId, devices, message, rssi):
    Domoticz.Log("Updating AQS Sensor Id: " + str(deviceId))
    batteryVoltageRecord = Common.findRecord(message, OpenThings.PARAM_BATTERY_VOLTAGE)
    humidityRecord = Common.findRecord(message, OpenThings.PARAM_RELATIVE_HUMIDITY)
    batteryLevelRecord = Common.findRecord(message, OpenThings.PARAM_BATTERY_LEVEL)
    temperatureRecord = Common.findRecord(message, OpenThings.PARAM_TEMPERATURE)
    tvocRecord = Common.findRecord(message, OpenThings.PARAM_TVOC)
    etohRecord = Common.findRecord(message, OpenThings.PARAM_ETOH)
    eco2Record = Common.findRecord(message, OpenThings.PARAM_ECO2)
    iaqRecord = Common.findRecord(message, OpenThings.PARAM_IAQ)

    batteryVoltage = round(batteryVoltageRecord["value"], 2)
    temperature = round(temperatureRecord["value"], 2)
    humidity = round(humidityRecord["value"], 2)
    batteryLevel = batteryLevelRecord["value"]
    iaq = round(iaqRecord["value"], 2)
    tvoc = round(tvocRecord["value"], 2)
    etoh = round(etohRecord["value"], 2)
    eco2 = round(eco2Record["value"], 2)

    iaqLevel = calculateIAQLevel(iaq)
    iaqtext = AIR_QUALITY_LEVEL_CONDITION[iaqLevel]

    Domoticz.Debug("Updating AQS Sensor Id: [" + str(deviceId) + "] "
                   "IAQ: [" + str(iaq) + "] " +
                   "TVOC: [" + str(tvoc) + "] " +
                   "ETOH: [" + str(etoh) + "] " +
                   "ECO2: [" + str(eco2) + "] " +
                   "IAQText: [" + iaqtext + "]" +
                   "IAQLevel: [" + str(iaqLevel) + "] " +
                   "Humidity: [" + str(humidity) + "] " +
                   "Temperature: [" + str(temperature) + "] " +
                   "Battery Level: [" + str(batteryLevel) + "]" +
                   "Battery Voltage: [" + str(batteryVoltage) + "]")
    
    devices[deviceId].Units[IAQ_UNIT].nValue = iaq
    devices[deviceId].Units[IAQ_UNIT].sValue = str(iaq)
    devices[deviceId].Units[IAQ_UNIT].BatteryLevel = batteryLevel
    devices[deviceId].Units[IAQ_UNIT].SignalLevel = rssi
    devices[deviceId].Units[IAQ_UNIT].Update(Log=True)

    devices[deviceId].Units[INDEX_UNIT].nValue = iaqLevel
    devices[deviceId].Units[INDEX_UNIT].sValue = iaqtext
    devices[deviceId].Units[INDEX_UNIT].BatteryLevel = batteryLevel
    devices[deviceId].Units[INDEX_UNIT].SignalLevel = rssi
    devices[deviceId].Units[INDEX_UNIT].Update(Log=True)

    devices[deviceId].Units[TVOC_UNIT].nValue = tvoc
    devices[deviceId].Units[TVOC_UNIT].sValue = str(tvoc)
    devices[deviceId].Units[TVOC_UNIT].BatteryLevel = batteryLevel
    devices[deviceId].Units[TVOC_UNIT].SignalLevel = rssi
    devices[deviceId].Units[TVOC_UNIT].Update(Log=True)

    devices[deviceId].Units[ETOH_UNIT].nValue = etoh
    devices[deviceId].Units[ETOH_UNIT].sValue = str(etoh)
    devices[deviceId].Units[ETOH_UNIT].BatteryLevel = batteryLevel
    devices[deviceId].Units[ETOH_UNIT].SignalLevel = rssi
    devices[deviceId].Units[ETOH_UNIT].Update(Log=True)

    devices[deviceId].Units[ECO2_UNIT].nValue = eco2
    devices[deviceId].Units[ECO2_UNIT].sValue = str(eco2)
    devices[deviceId].Units[ECO2_UNIT].BatteryLevel = batteryLevel
    devices[deviceId].Units[ECO2_UNIT].SignalLevel = rssi
    devices[deviceId].Units[ECO2_UNIT].Update(Log=True)

    devices[deviceId].Units[TEMP_HUM_UNIT].nValue = temperature
    devices[deviceId].Units[TEMP_HUM_UNIT].sValue = str(temperature) + ";" + str(humidity)
    devices[deviceId].Units[TEMP_HUM_UNIT].BatteryLevel = batteryLevel
    devices[deviceId].Units[TEMP_HUM_UNIT].SignalLevel = rssi
    devices[deviceId].Units[TEMP_HUM_UNIT].Update(Log=True)

    devices[deviceId].Units[VBATT_UNIT].nValue = batteryVoltage
    devices[deviceId].Units[VBATT_UNIT].sValue = str(batteryVoltage)
    devices[deviceId].Units[VBATT_UNIT].BatteryLevel = batteryLevel
    devices[deviceId].Units[VBATT_UNIT].SignalLevel = rssi
    devices[deviceId].Units[VBATT_UNIT].Update(Log=True)

def calculateIAQLevel(iaq):
    level = 0

    if iaq <= AIR_QUALITY_LEVEL_LIMIT[0]:
        level = 0

    if iaq > AIR_QUALITY_LEVEL_LIMIT[0] and iaq <= AIR_QUALITY_LEVEL_LIMIT[1]:
        level = 1

    if iaq > AIR_QUALITY_LEVEL_LIMIT[1] and iaq <= AIR_QUALITY_LEVEL_LIMIT[2]:
        level = 2

    if iaq > AIR_QUALITY_LEVEL_LIMIT[2] and iaq <= AIR_QUALITY_LEVEL_LIMIT[3]:
        level = 3
    
    if iaq > AIR_QUALITY_LEVEL_LIMIT[4]:
        level = 4
    
    return level