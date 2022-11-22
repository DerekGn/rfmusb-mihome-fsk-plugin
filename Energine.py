# Energine.py
#
# Author: DerekGn
#
import DomoticzEx as Domoticz
import OpenThings
import Common

MFRID_ENERGENIE = 0x04

# PRODUCTID_MIHO001                      # Home Hub
# PRODUCTID_MIHO002                      # OOK: Control only
# PRODUCTID_MIHO003                      # OOK: Hand Controller
PRODUCTID_MIHO004 = 0x01  # FSK: Monitor only
PRODUCTID_MIHO005 = 0x02  # FSK: Adaptor Plus
PRODUCTID_MIHO006 = 0x05  # FSK: House Monitor
# PRODUCTID_MIHO007                      # OOK: Double Wall Socket white
# PRODUCTID_MIHO008                      # OOK: Single light switch white
# PRODUCTID_MIHO009                      # OOK: Double Light Switch white
# PRODUCTID_MIHO010                      # OOK: Single light dimmer switch white
# PRODUCTID_MIHO011
# PRODUCTID_MIHO012
PRODUCTID_MIHO013 = 0x03  # FSK: eTRV
# PRODUCTID_MIHO014                      # OOK: In-line Relay
# PRODUCTID_MIHO015
# PRODUCTID_MIHO016
# PRODUCTID_MIHO017
# PRODUCTID_MIHO018
# PRODUCTID_MIHO019
# PRODUCTID_MIHO020
# PRODUCTID_MIHO021                      # OOK: Double Wall Socket nickel
# PRODUCTID_MIHO022                      # OOK: Double Wall Socket chrome
# PRODUCTID_MIHO023                      # OOK: Double Wall Socket brushed steel
# PRODUCTID_MIHO024                      # OOK: Style Light nickel
# PRODUCTID_MIHO025                      # OOK: Style Light chrome
# PRODUCTID_MIHO026                      # OOK: Style Light steel
# PRODUCTID_MIHO027                      # Starter pack bundle
# PRODUCTID_MIHO028                      # Eco starter pack
# PRODUCTID_MIHO029                      # Heating bundle
# PRODUCTID_MIHO030
# PRODUCTID_MIHO031
PRODUCTID_MIHO032 = 0x0C  # FSK: Motion sensor
PRODUCTID_MIHO033 = 0x0D  # FSK: Open sensor
# PRODUCTID_MIHO034
# PRODUCTID_MIHO035
# PRODUCTID_MIHO036
# PRODUCTID_MIHO037                      # Adaptor Plus Bundle
# PRODUCTID_MIHO038                      # OOK: 2-gang socket Bundle
# PRODUCTID_MIHO039                      # OOK: 2-gang socket Bundle black nickel
# PRODUCTID_MIHO040                      # OOK: 2-gang socket Bundle chrome
# PRODUCTID_MIHO041                      # OOK: 2-gang socket Bundle stainless steel
# PRODUCTID_MIHO069                      # Wall thermostat
# PRODUCTID MIHO075                      # OOK: Single Gang Light Dimmer in brushed nikel
# PRODUCTID MIHO076                      # OOK: Single Gang Light Dimmer in polished chrome
# PRODUCTID MIHO077                      # OOK: Single Gang Light Dimmer in brushed steel
# PRODUCTID MIHO087                      # OOK: Single Gang Light Dimmer in brushed graphite

# Default keys for OpenThings encryption and decryption
CRYPT_PID = 242
CRYPT_PIP = 0x0100

def createDevice(deviceId, productId):
    if(productId == PRODUCTID_MIHO032):
        Domoticz.Log("Creating Motion Sensor Id: " + deviceId)
        Domoticz.Unit(Name="Motion Sensor", DeviceID=deviceId, Unit=1,
                        TypeName="Switch", Type=244, Subtype=73, Switchtype=8,
                        Description="MIHO032 Infra red Motion Sensor", Used=1).Create()
    elif(productId == PRODUCTID_MIHO033):
        Domoticz.Log("Creating Door Sensor Id: " + deviceId)
        Domoticz.Unit(Name="Door Sensor", DeviceID=deviceId, Unit=1,
                        TypeName="Switch", Type=244, Subtype=73, Switchtype=11,
                        Description="MIHO033 Door Sensor", Used=1).Create()

def updateDevice(deviceId, device, productId, message):
    if(device is not None):
        if(productId == PRODUCTID_MIHO032):
            motionRecord = Common.findRecord(
                message, OpenThings.PARAM_MOTION_DETECTOR)
            # TODO map 0 value
            Domoticz.Debug("Updating Motion Sensor Id: " +
                        str(deviceId) + str(motionRecord["value"]))
            
            device[1].nValue = int(motionRecord["value"])
            device[1].sValue = str(motionRecord["value"])
            device[1].Update(Log=True)
        elif(productId == PRODUCTID_MIHO033):
            Domoticz.Debug("Updating Door Sensor Id: " + str(deviceId))
            doorRecord = Common.findRecord(message, OpenThings.PARAM_DOOR_SENSOR)

            device[1].nValue = int(doorRecord["value"])
            device[1].sValue = str(doorRecord["value"])
            device[1].Update(Log=True)

            device.Update(nValue=int(
                doorRecord["value"]), sValue=str(doorRecord["value"]))