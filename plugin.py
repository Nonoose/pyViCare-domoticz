"""
<plugin key="pyViCare-domoticz" name="pyViCare-domoticz Viessmann API Plugin" author="Nonoose" version="1.0.0" wikilink="https://www.domoticz.com/wiki/Developing_a_Python_plugin" externallink="https://github.com/Nonoose/pyViCare-domoticz">
    <description>
        Domoticz plugin to access the Viessmann API using pyViCare library.
        All credits to "somm15": creator of pyViCare and "wimmme": creator of the domoticz plugin, this plugin is just a fork to add sensors for my equipment
    </description>
    <params>
        <param field="Username" label="Viessmann Email" width="300px" required="true"/>
        <param field="Password" label="Viessmann Password" width="300px" required="true" password="true"/>
        <param field="Mode1" label="Viessmann API client ID" width="300px" required="true"/>
        <param field="Mode2" label="Viessmann update interval" width="300px" required="true" default="60"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import os
import sys
import logging
from PyViCare.PyViCare import PyViCare

class VSensor:
    def __init__(self, position, name, type):
        self.position = position
        self.name = name
        self.type = type

class BasePlugin:
    enabled = False


    def __init__(self):
        self.vicare = None
        self.client_id = ""
        self.Username = ""
        self.Password = ""
        self.update_interval = ""
        self.DEBUG = ""


    def onStart(self):
        Domoticz.Log("onStart called")
        self.debugging = Parameters["Mode6"]
        self.update_interval = int(Parameters["Mode2"])

        self.client_id = Parameters["Mode1"].strip()
        self.Username = Parameters["Username"].strip()
        self.Password = Parameters["Password"].strip()
        self.DEBUG = Parameters["Mode6"]

        if self.DEBUG == "Debug":
            Domoticz.Debugging(1)

        if len(self.Username) == 0 or len(self.Password) == 0 or len(self.client_id) == 0:
            Domoticz.Log("Please provide Viessmann Email, Password and client_ID in the plugin settings.")
            return 

        try:
            # Define all sensors :
            sensor = [VSensor(1,"ExternalTemperature","Temperature")]
            sensor.append(VSensor(2,"InternalTemperature","Temperature"))
            sensor.append(VSensor(3,"HotWaterTemperature","Temperature"))
            sensor.append(VSensor(4,"HotWaterSetTemperature","Temperature"))
            sensor.append(VSensor(5,"HeaterTemperature","Temperature"))
            sensor.append(VSensor(6,"HeaterSetTemperature","Temperature"))
            sensor.append(VSensor(7,"BoilerTemperature","Temperature"))
            sensor.append(VSensor(8,"Burner","Text"))
            sensor.append(VSensor(9,"HeaterProgram","Text"))

            self.vicare = PyViCare()
            self.vicare.initWithCredentials(self.Username, self.Password, self.client_id, os.path.join(os.path.expanduser('~'),"token.save"))

            device = self.vicare.devices[0]

            Domoticz.Log("Model: " + device.getModel())
            Domoticz.Log("Status: " + "Online" if device.isOnline() else "Offline") 

            self.enabled = True

            # Create sensors if they don't exist
            devs = Devices
            for sens in sensor:
                SensorExist = 0
                for dev in devs:
                  if (dev == sens.position):
                    SensorExist = 1
                if (SensorExist == 0):
                  Domoticz.Device(Name=sens.name, Unit=sens.position, TypeName=sens.type, Used=1).Create()
                  Domoticz.Log("Sensor ''" + sens.name + "'' created")

            Domoticz.Heartbeat(self.update_interval)

        except Exception as e:
            Domoticz.Log("Failed to initialize pyViCare: {}".format(str(e)))
            self = None


    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called")

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("onNotification called")

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        if self.vicare is not None:
            try:
              # Fetch the data from Viessmann API using pyViCare
              device = self.vicare.devices[0]
              vitovalor = device.asOilBoiler()
              circuit = vitovalor.circuits[0]
              burner = vitovalor.burners[0]
              
              # Store values from defined sensors
              outside_temp = vitovalor.getOutsideTemperature()
              inside_temp = circuit.getRoomTemperature()
              hotwater_temp = vitovalor.getDomesticHotWaterStorageTemperature()
              hotwater_desired_temp = vitovalor.getDomesticHotWaterConfiguredTemperature()
              heater_temp = circuit.getSupplyTemperature()
              heater_desired_temp = circuit.getCurrentDesiredTemperature()
              boiler_temp = vitovalor.getBoilerTemperature()
              burner_active = burner.getActive()
              active_mode = circuit.getActiveProgram()

              if outside_temp is not None:
                Devices[1].Update(nValue=0,sValue=str(outside_temp))
              if inside_temp is not None:
                Devices[2].Update(nValue=0,sValue=str(inside_temp))
              if hotwater_temp is not None:
                Devices[3].Update(nValue=0,sValue=str(hotwater_temp))
              if hotwater_desired_temp is not None:
                Devices[4].Update(nValue=0,sValue=str(hotwater_desired_temp))
              if heater_temp is not None:
                Devices[5].Update(nValue=0,sValue=str(heater_temp))
              if heater_desired_temp is not None:
                Devices[6].Update(nValue=0,sValue=str(heater_desired_temp))
              if boiler_temp is not None:
                Devices[7].Update(nValue=0,sValue=str(boiler_temp))
              if burner_active is True:
                Devices[8].Update(nValue=0,sValue="On")
              if burner_active is False:
                Devices[8].Update(nValue=0,sValue="Off")
              if active_mode is not None:
                Devices[9].Update(nValue=0,sValue=str(active_mode))

            except Exception as e:
                Domoticz.Log("Error fetching data from Viessmann API: {}".format(str(e)))
                return
        else:
            Domoticz.Log("pyViCare not initialized. Please check your Viessmann Username and Password in plugin settings.")
            return

# Define Domoticz log function
def LogMessage(message):
    Domoticz.Log(message)

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def LogMessage(message):
    Domoticz.Log(message)
