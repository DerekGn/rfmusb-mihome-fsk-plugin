# axiologix_temp_humidity.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import DeviceTypes
import OpenThings
import Common

PRODUCTID_TEMPHUMIDITY = 0x01

def createTempHumiditySensor(deviceId):
    Domoticz.Log("Creating Temp Humidity Sensor Id: " + str(deviceId))
    Domoticz.Unit(Name="Temp Humidity Sensor", DeviceID=deviceId, Unit=1,
                  TypeName="Temp+Hum", Type=DeviceTypes.DEVICE_TYPE_TEMP_HUMIDITY,
                  Description="RfmTemp Sensor").Create()

def updateTemperatureHumiditySensor(deviceId, devices, message, rssi):
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
    
    devices[deviceId].Units[1].sValue = str(temperature) + ";" + str(humidity)
    devices[deviceId].Units[1].BatteryLevel = batteryLevel
    devices[deviceId].Units[1].SignalLevel = rssi
    devices[deviceId].Units[1].Update(Log=True)