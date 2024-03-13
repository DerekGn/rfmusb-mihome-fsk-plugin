# axiologix_temp_humidity.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import Types
import OpenThings
import Common

PRODUCTID_TEMPHUMIDITY = 0x01

def create_temperature_humidity_sensor(deviceId):
    Domoticz.Status("Creating Temp Humidity Sensor Id: [{}]"
                    .format(deviceId))
    Domoticz.Unit(Name="Temp Humidity Sensor",
                  DeviceID=deviceId, Unit=1,
                  TypeName="Temp+Hum",
                  Type=Types.TYPE_TEMP_HUMIDITY,
                  Description="RfmTemp Sensor").Create()

def update_temperature_humidity_sensor(deviceId, devices, message, rssi):
    Domoticz.Status("Updating Temperature Humidity Sensor Id: [{}]"
                    .format(deviceId))
    batteryRecord = Common.find_record(message, OpenThings.PARAM_BATTERY_LEVEL)
    temperatureRecord = Common.find_record(message, OpenThings.PARAM_TEMPERATURE)
    humidityRecord = Common.find_record(message, OpenThings.PARAM_RELATIVE_HUMIDITY)

    temperature = round(temperatureRecord["value"], 2)
    humidity = round(humidityRecord["value"], 2)
    batteryLevel = batteryRecord["value"]

    Domoticz.Debug("Updating TempHumidity Sensor Id: [{0}] Temperature: [{1}] Humidity: [{2}] Battery Level: [{3}]"
                   .format(deviceId, str(temperature), str(humidity), str(batteryLevel)))
    
    devices[deviceId].Units[1].sValue = str(temperature) + ";" + str(humidity) + ";0"
    devices[deviceId].Units[1].BatteryLevel = batteryLevel
    devices[deviceId].Units[1].SignalLevel = rssi
    devices[deviceId].Units[1].Update(Log=True)