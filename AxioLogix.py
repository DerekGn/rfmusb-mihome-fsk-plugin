# AxioLogix.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import AxioLogixTempHumidity
import AxioLogixEnergyMeter
import AxioLogixAqs

MFRID_AXIOLOGIX = 0x55

def createDevice(deviceId, productId):
    if(productId == AxioLogixTempHumidity.PRODUCTID_TEMPHUMIDITY):
        AxioLogixTempHumidity.createTempHumiditySensor(deviceId)
    elif(productId == AxioLogixAqs.PRODUCTID_AQS):
        AxioLogixAqs.createAqsSensor(deviceId)
    elif(productId == AxioLogixEnergyMeter.PRODUCTID_EM):
        AxioLogixEnergyMeter.createEnergyMeterSensor(deviceId)

def updateDevice(deviceId, devices, productId, message, rssi):
    if(productId == AxioLogixTempHumidity.PRODUCTID_TEMPHUMIDITY):
        AxioLogixTempHumidity.updateTemperatureHumiditySensor(deviceId, devices, message, rssi)
    elif(productId == AxioLogixAqs.PRODUCTID_AQS):
        AxioLogixAqs.updateAqsSensor(deviceId, devices, message, rssi)
    elif(productId == AxioLogixEnergyMeter.PRODUCTID_EM):
        AxioLogixEnergyMeter.updateEnergyMeterSensor(deviceId, devices, message, rssi)

def findDeviceByType(devices, deviceType):
    for x in devices:
        if(x.Type == deviceType):
            return x
