# Common.py
#
# Author: DerekGn
#

import DomoticzEx as Domoticz

def device_and_unit_exists(devices, deviceId, unitId):
    return (devices[deviceId] is not None) \
        and (devices[deviceId].Units[unitId] is not None)

def find_record(message, id):
    found = None
    for record in message["recs"]:
        if(record["paramid"] == id):
            Domoticz.Debug("Found record Id: " + str(id))
            found = record
            break
    return found

def create_device_id(productId, manufacturerId, sensorId):
    return str(productId) + ":" + str(manufacturerId) + ":" + str(sensorId)

def round_record_value(record, rounding):
    result = 0
    if("value" in record):
        result = round(record["value"], rounding)
    return result