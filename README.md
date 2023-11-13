# Domoticz plugin for pyViCare, a python interface to the Viessmann API
A Python plugin for Domoticz to communicate with the Viessmann API.
Just a fork from the great job of "wimmme" :
https://github.com/wimmme/pyViCare-domoticz

I've just changed the way sensors are added and programmed 9 of them :
- ExternalTemperature
- InternalTemperature
- HotWaterTemperature
- HotWaterSetTemperature
- HeaterTemperature
- HeaterSetTemperature
- BoilerTemperature
- Burner
- HeaterProgram
Programmed for my "Vitorondens 200-T" but should work for others

# Getting started
If you don't have git:
```
sudo apt-get update
sudo apt-get install git
```
Goto to the plugins directory of your domoticz installation folder and clone this repository:
```
cd domoticz/plugins
git clone https://github.com/Nonoose/pyViCare-domoticz.git pyViCare-domoticz
```
So in this case the directory structure should now be: domoticz/plugins/pyViCare-domoticz/plugin.py

Next, you need to restart Domoticz so that it will find the plugin:
```
 sudo systemctl restart domoticz.service
```
or
```
sudo service domoticz.sh restart
```
From here the plugin should be able to be set-up from the Domoticz interface. Go to the hardware page and look in the dropdown, you should find "pyViCare-domoticz Viessmann API Plugin"

If you run Linux and the plugin does not show up in the hardware list, you may have to make the plugin.py file executable. Go to the directory and execute the command:
```
 chmod +x pyViCare-domoticz/plugin.py
```

https://www.domoticz.com/wiki/Using_Python_plugins

# Requirements
This plugin requires python v3.9 (or greater), and the python modules pyViCare and requests installed
```
pip install pyViCare requests
```

To use PyViCare, every user has to register and create their private API key. Follow these steps to create your API key:

1. Login to the [Viessmann Developer Portal](https://developer.viessmann.com/start.html) with your existing ViCare username from the ViCare app.
2. Go to My Dashboard, which should open https://app.developer.viessmann.com/
3. Navigate to API Keys.
4. Create a new OAuth client using following data:
   * Name: PyViCare
   * Google reCAPTCHA: Disabled
   * Redirect URIs: vicare://oauth-callback/everest
   * Copy the Client ID to use in your code. Pass it as constructor parameter to the device.

(instructions copied from somm15: https://github.com/somm15/PyViCare)

# Create a Hardware in Domoticz
In Domoticz web UI, navigate to the Hardware page.
Give a name to your Hardware and select "pyViCare-domoticz Viessmann API Plugin" type
Enter following informations from the Viessman Developer Portal account you created above :
- Viessmann Email:	
- Viessmann Password:	
- Viessmann API client ID:

Click "Add", and all sensors should be created and filled with informations

# Compatibility
This script was tested with:
* Domoticz Version: 2023.2
* Python Version: 3.9
* Ubuntu: 22.04.1 
