# AxioLogixAqs.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import Types
import SubTypes
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

PARAM_BATTERY_VOLTAGE   = 0x01
PARAM_IAQ			    = 0x02
PARAM_TVOC				= 0x03
PARAM_ETOH				= 0x04
PARAM_ECO2				= 0x05

AIR_QUALITY_LEVEL_LIMIT = [1.9,2.9,3.9,4.9,5]
AIR_QUALITY_LEVEL_CONDITION = ["None","Very Good","Good","Medium","Poor","Bad"]

def create_aqs_sensor(deviceId):
    Domoticz.Log("Creating Aqs Sensor Id: " + deviceId)
    Domoticz.Unit(Name="IAQ", DeviceID=deviceId, Unit=IAQ_UNIT,
                  Type=Types.TYPE_GENERAL,
                  Subtype=SubTypes.SUB_TYPE_CUSTOM,
                  Options={'Custom': '1;IAQ'},
                  Description="RfmAqs Sensor IAQ").Create()
    Domoticz.Unit(Name="Index", DeviceID=deviceId, Unit=INDEX_UNIT,
                  TypeName="Alert",
                  Description="RfmAqs Sensor IAQ").Create()
    Domoticz.Unit(Name="TVOC", DeviceID=deviceId, Unit=TVOC_UNIT,
                  Type=Types.TYPE_GENERAL,
                  Subtype=SubTypes.SUB_TYPE_CUSTOM,
                  Options={'Custom': '1;mg/m^3'},
                  Description="RfmAqs Sensor TVOC").Create()
    Domoticz.Unit(Name="ETOH", DeviceID=deviceId, Unit=ETOH_UNIT,
                  Type=Types.TYPE_GENERAL,
                  Subtype=SubTypes.SUB_TYPE_CUSTOM,
                  Options={'Custom': '1;ppm'},
                  Description="RfmAqs Sensor ETOH").Create()
    Domoticz.Unit(Name="ECO2", DeviceID=deviceId, Unit=ECO2_UNIT,
                  Type=Types.TYPE_GENERAL,
                  Subtype=SubTypes.SUB_TYPE_CUSTOM,
                  Options={'Custom': '1;ppm'},
                  Description="RfmAqs Sensor ECO2").Create()
    Domoticz.Unit(Name="AQS Temp & Humidity", DeviceID=deviceId, Unit=TEMP_HUM_UNIT,
                  TypeName="Temp+Hum", Type=Types.DEVICE_TYPE_TEMP_HUMIDITY,
                  Description="RfmAqs Temp & Humidity").Create()
    Domoticz.Unit(Name="BatteryVoltage", DeviceID=deviceId, Unit=VBATT_UNIT,
                  Type=Types.TYPE_GENERAL,
                  Subtype=Types.DEVICE_SUB_TYPE_VOLTAGE,
                  Description="RfmAqs Sensor Battery Voltage").Create()

def update_aqs_sensor(deviceId, devices, message, rssi):
    Domoticz.Log("Updating AQS Sensor Id: [{0}]"
                 .format(deviceId))
    batteryVoltageRecord = Common.find_record(message, PARAM_BATTERY_VOLTAGE)
    humidityRecord = Common.find_record(message, OpenThings.PARAM_RELATIVE_HUMIDITY)
    batteryLevelRecord = Common.find_record(message, OpenThings.PARAM_BATTERY_LEVEL)
    temperatureRecord = Common.find_record(message, OpenThings.PARAM_TEMPERATURE)
    tvocRecord = Common.find_record(message, PARAM_TVOC)
    etohRecord = Common.find_record(message, PARAM_ETOH)
    eco2Record = Common.find_record(message, PARAM_ECO2)
    iaqRecord = Common.find_record(message, PARAM_IAQ)

    batteryVoltage = Common.round_record_value(batteryVoltageRecord, 2)
    temperature = Common.round_record_value(temperatureRecord, 1)
    humidity = Common.round_record_value(humidityRecord, 2)
    batteryLevel = Common.round_record_value(batteryLevelRecord, 2)
    iaq = Common.round_record_value(iaqRecord, 2)
    tvoc = Common.round_record_value(tvocRecord, 2)
    etoh = Common.round_record_value(etohRecord, 2)
    eco2 = Common.round_record_value(eco2Record, 2)

    iaqLevel = calculate_IAQ_level(iaq)
    iaqtext = AIR_QUALITY_LEVEL_CONDITION[iaqLevel]

    Domoticz.Debug("Updating AQS Sensor Id: [{0}] "
                   "RSSI: [{1}] IAQ: [{2}] " +
                   "TVOC: [{3}] ETOH: [{4}] " +
                   "ECO2: [{5}] IAQText: [{6}] " +
                   "IAQLevel: [{7}] Humidity: [{8}] " +
                   "Temperature: [{9}] Battery Level: [{10}] " +
                   "Battery Voltage: [{11}]"
                   .format(deviceId, str(rssi), str(iaq), str(tvoc), 
                           str(etoh), str(eco2), iaqtext, str(iaqLevel), 
                           str(humidity), str(temperature), str(batteryLevel),
                           str(batteryVoltage)))
    
    device = device
    device.Units[IAQ_UNIT].nValue = iaq
    device.Units[IAQ_UNIT].sValue = str(iaq)
    device.Units[IAQ_UNIT].BatteryLevel = batteryLevel
    device.Units[IAQ_UNIT].SignalLevel = rssi
    device.Units[IAQ_UNIT].Update(Log=True)

    device.Units[INDEX_UNIT].nValue = iaqLevel
    device.Units[INDEX_UNIT].sValue = iaqtext
    device.Units[INDEX_UNIT].BatteryLevel = batteryLevel
    device.Units[INDEX_UNIT].SignalLevel = rssi
    device.Units[INDEX_UNIT].Update(Log=True)

    device.Units[TVOC_UNIT].nValue = tvoc
    device.Units[TVOC_UNIT].sValue = str(tvoc)
    device.Units[TVOC_UNIT].BatteryLevel = batteryLevel
    device.Units[TVOC_UNIT].SignalLevel = rssi
    device.Units[TVOC_UNIT].Update(Log=True)

    device.Units[ETOH_UNIT].nValue = etoh
    device.Units[ETOH_UNIT].sValue = str(etoh)
    device.Units[ETOH_UNIT].BatteryLevel = batteryLevel
    device.Units[ETOH_UNIT].SignalLevel = rssi
    device.Units[ETOH_UNIT].Update(Log=True)

    device.Units[ECO2_UNIT].nValue = eco2
    device.Units[ECO2_UNIT].sValue = str(eco2)
    device.Units[ECO2_UNIT].BatteryLevel = batteryLevel
    device.Units[ECO2_UNIT].SignalLevel = rssi
    device.Units[ECO2_UNIT].Update(Log=True)

    device.Units[TEMP_HUM_UNIT].nValue = temperature
    device.Units[TEMP_HUM_UNIT].sValue = str(temperature) + ";" + str(humidity) + ";0"
    device.Units[TEMP_HUM_UNIT].BatteryLevel = batteryLevel
    device.Units[TEMP_HUM_UNIT].SignalLevel = rssi
    device.Units[TEMP_HUM_UNIT].Update(Log=True)

    device.Units[VBATT_UNIT].nValue = batteryVoltage
    device.Units[VBATT_UNIT].sValue = str(batteryVoltage)
    device.Units[VBATT_UNIT].BatteryLevel = batteryLevel
    device.Units[VBATT_UNIT].SignalLevel = rssi
    device.Units[VBATT_UNIT].Update(Log=True)

def calculate_IAQ_level(iaq):
    level = 0

    if iaq > 0 and iaq <= AIR_QUALITY_LEVEL_LIMIT[0]:
        level = 1

    if iaq > AIR_QUALITY_LEVEL_LIMIT[0] and iaq <= AIR_QUALITY_LEVEL_LIMIT[1]:
        level = 2

    if iaq > AIR_QUALITY_LEVEL_LIMIT[1] and iaq <= AIR_QUALITY_LEVEL_LIMIT[2]:
        level = 3

    if iaq > AIR_QUALITY_LEVEL_LIMIT[2] and iaq <= AIR_QUALITY_LEVEL_LIMIT[3]:
        level = 4
    
    if iaq > AIR_QUALITY_LEVEL_LIMIT[4]:
        level = 5
    
    return level