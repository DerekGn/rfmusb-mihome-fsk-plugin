# Common.py
#
# Author: DerekGn
#

def FindRecord(message, idToFind):
    for record in message["recs"]:
        parameterId = record["paramid"]
        if(parameterId == idToFind):
            return record