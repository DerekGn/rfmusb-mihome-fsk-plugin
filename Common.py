# Common.py
#
# Author: DerekGn
#

def deviceAndUnitExists(devices, deviceId, unitId):
    return (devices[deviceId] is not None) \
        and (devices[deviceId].Units[unitId] is not None)

def findRecord(message, idToFind):
    for record in message["recs"]:
        parameterId = record["paramid"]
        if(parameterId == idToFind):
            return record

def createDeviceId(productId, manufacturerId, sensorId):
    return str(productId) + ":" + str(manufacturerId) + ":" + str(sensorId)
