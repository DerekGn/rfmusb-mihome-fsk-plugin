# AxioLogix.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import AxioLogixTempHumidity
import AxioLogixEnergyMeter
import AxioLogixAqs

MFRID_AXIOLOGIX = 0x55

def create_device(deviceId, productId):
    if(productId == AxioLogixTempHumidity.PRODUCTID_TEMPHUMIDITY):
        AxioLogixTempHumidity.create_temperature_humidity_sensor(deviceId)
    elif(productId == AxioLogixAqs.PRODUCTID_AQS):
        AxioLogixAqs.create_aqs_sensor(deviceId)
    elif(productId == AxioLogixEnergyMeter.PRODUCTID_EM):
        AxioLogixEnergyMeter.create_energy_meter_sensor(deviceId)

def update_device(deviceId, devices, productId, message, rssi):
    if(productId == AxioLogixTempHumidity.PRODUCTID_TEMPHUMIDITY):
        AxioLogixTempHumidity.update_temperature_humidity_sensor(deviceId, devices, message, rssi)
    elif(productId == AxioLogixAqs.PRODUCTID_AQS):
        AxioLogixAqs.update_aqs_sensor(deviceId, devices, message, rssi)
    elif(productId == AxioLogixEnergyMeter.PRODUCTID_EM):
        AxioLogixEnergyMeter.update_energy_meter_sensor(deviceId, devices, message, rssi)

def find_device_by_type(devices, deviceType):
    for x in devices:
        if(x.Type == deviceType):
            return x
