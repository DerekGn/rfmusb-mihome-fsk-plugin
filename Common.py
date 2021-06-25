# Common.py
#
# Author: DerekGn
#

def findRecord(message, idToFind):
    for record in message["recs"]:
        parameterId = record["paramid"]
        if(parameterId == idToFind):
            return record

def createDeviceId(productId, sensorId):
    return str(productId) + ":" + str(sensorId)