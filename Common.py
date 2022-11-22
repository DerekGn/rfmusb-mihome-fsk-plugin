# Common.py
#
# Author: DerekGn
#

import DomoticzEx as Domoticz

def findDevice(deviceId):
        for x in Devices:
            if(Devices[x].DeviceID == deviceId):
                return Devices[x]

def findRecord(message, idToFind):
    for record in message["recs"]:
        parameterId = record["paramid"]
        if(parameterId == idToFind):
            return record

def createDeviceId(productId, manufacturerId, sensorId):
    return str(productId) + ":" + str(manufacturerId) + ":" + str(sensorId)