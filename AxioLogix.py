# AxioLogix.py
#
# Author: DerekGn
#
import Common
import Domoticz
import Energine
import OpenThings

MFRID_AXIOLOGIX                  = 0x55

PRODUCTID_TEMPHUMIDITY           = 0x01
PRODUCTID_AQS                    = 0x02
PRODUCTID_EM                     = 0x03

def CreateAxioLogixDevice(sensorId, productId):
    if(productId == PRODUCTID_TEMPHUMIDITY):
        Domoticz.Log("Creating Temp Humidity Sensor Id: " + str(sensorId))
        Domoticz.Device(Name="Temp Humidity Sensor", DeviceID=sensorId, Unit=1,
                        TypeName="Temp+Hum", Type=82,
                        Description="RfmTemp Sensor").Create()
    elif(productId == PRODUCTID_AQS):
        Domoticz.Log("Creating Aqs Sensor Id: " + str(sensorId))
        Domoticz.Device(Name="AQS", DeviceID=sensorId, Unit=1,
                        Type=243, Subtype=31,
                        Options={'Custom': '1;VOC Index'},
                        Description="RfmAqs Sensor").Create()
        Domoticz.Device(Name="AQS Temp & Humidity", DeviceId=sensorId, Unit=2,
                        TypeName="Temp+Hum", Type=82,
                        Description="RfmAqs Temp & Humidity").Create()
    elif(productId == PRODUCTID_EM):
        Domoticz.Log("Creating Energy Meter Id: " + str(sensorId))
        Domoticz.Device(Name="Energy Meter Voltage", DeviceID=sensorId, Unit=1,
                        Type=243, Subtype=31,
                        Options={'Custom': '1;VAC'},
                        Description="Rms Voltage").Create()
        Domoticz.Device(Name="Energy Meter Frequency", DeviceID=sensorId, Unit=2,
                        Type=243, Subtype=31,
                        Options={'Custom': '1;Hz'},
                        Description="Line Voltage Frequency").Create()

        CreateRfmEmLineMeasurements('L', sensorId, 3)

        CreateRfmEmLineMeasurements('n', sensorId, 9)

        CreateRfmEmEnergyMeasurements(sensorId, 15)

def CreateRfmEmLineMeasurements(self, line, sensorId, unit):
    Domoticz.Device(Name="Energy Meter " + line + " Current", DeviceID=sensorId, Unit=unit,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;Irms'},
                    Description=line + " Line Rms Current").Create()
    Domoticz.Device(Name="Energy Meter " + line + " Phase", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;°'},
                    Description="Phase Angle between Voltage and " + line + " Line Current").Create()
    Domoticz.Device(Name="Energy Meter " + line + " PMean", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;kW'},
                    Description=line + " Line Mean Active Power").Create()
    Domoticz.Device(Name="Energy Meter " + line + " QMean", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;kvar'},
                    Description=line + " Line Mean Reactive Power").Create()
    Domoticz.Device(Name="Energy Meter " + line + "Power Factor", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=31,
                    Description=line + " Line Power Factor").Create()
    Domoticz.Device(Name="Energy Meter " + line + " SMean", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=31,
                    Options={'Custom': '1;kVA'},
                    Description=line + " Line Mean Apparent Power").Create()

def CreateRfmEmEnergyMeasurements(self, sensorId, unit):
    Domoticz.Device(Name="Energy Meter Absolute Active Energy", DeviceID=sensorId, Unit=unit,
                    Type=243, Subtype=28,
                    Description="Energy Meter Absolute Active Energy").Create()
    Domoticz.Device(Name="Energy Meter Absolute Reactive Energy", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=28,
                    Description="Energy Meter Absolute Reactive Energy").Create()
    Domoticz.Device(Name="Energy Meter Forward Active Energy", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=28,
                    Description="Energy Meter Forward Active Energy").Create()
    Domoticz.Device(Name="Energy Meter Forward Reactive Energy", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=28,
                    Description="Energy Meter Forward Reactive Energy").Create()
    Domoticz.Device(Name="Energy Meter Reverse Active Energy", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=28,
                    Description="Energy Meter Reverse Active Energy").Create()
    Domoticz.Device(Name="Energy Meter Reverse Reactive Energy", DeviceID=sensorId, Unit=++unit,
                    Type=243, Subtype=28,
                    Description="Energy Meter Reverse Reactive Energy").Create()

def UpdateDevice(device, productId, message):
    parameterId = record["paramid"]

    if(productId == PRODUCTID_TEMPHUMIDITY):
        temperatureRecord = Common.FindRecord(message, OpenThings.PARAM_TEMPERATURE)
        batteryRecord = Common.FindRecord(message, OpenThings.PARAM_BATTERY_LEVEL)
        humidityRecord = Common.FindRecord(message, OpenThings.PARAM_TEMPERATURE)