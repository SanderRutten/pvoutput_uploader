## Installation
Copy this addon to your Home Assistant /addons/pvoutput_uploader/  
Go to Supervisor > Add-On Store and reload your add-ons. This add-on is now shown at Local add-ons.  

## Configuration Options

| Config option   | Explaination   |
|:---|:---|
|ha_host   | Cannot be localhost because add-on's are Docker containers  |
|ha_token   | Go to http://IP_ADDRESS:8123/profile and generate a token.   |
|pvoutput_apikey   | Your PVoutput API key  |
|pvoutput_systemid   | Your plant ID  |
|v1_entity   | Entity which reports the Energy Generated (Today's generated solar power in watt hours)  |
|v2_entity   | Entity which reports the Power Generated (Current generated solar power in watts)  |
|v3_entity   | Entity which reports the Energy Consumption (Today's (total) usage in watt hours)  |
|v4_entity   | Entity which reports the Power Consumption (Current power usage in watts)  |
  
For v4 you can upload your smartmeter energy data, or use a sensor template which calculates the total energy usage for that day.  
To calculate the total energy per day you can take a look to the example below.  
Please make sure that your output is in the format expected by [PVOutput](https://pvoutput.org/help.html#api-addstatus).  
  
## No smartmeter?
If you don't have a device for your (smart) power meter, you can 'disable' it by editing this add-on and rebuilding it.  
In config.sh remove the 4 lines with entity_v3 and entity_v4.  
In pvoutput_uploader.py remove everything which points to v3 and v4 (e.g. api_v3, entity_v3, and don't forget to remove the two values in the cURL command).  

## Example sensor configuration
The configuration below works in my situation. Adjust to fit your situation  
My situation: Dutch smartmeter via DSMR integration and Growatt integration  
  
My Growatt Inverter for example reports it's data in kW while PVoutput expects watt hours. Which means the sensor reports a value of 5.4 kW but PVoutput wants to have 5400 as value.  
To fix the kW / watt hour 'problem' additional sensors needed to be added to configuration.yaml.  
Last but not least to calculate my energy_per_day two sensors from my smartmeter needed to be combined and an utility_meter to finish.  
  
### v1 and v3 convert to watt hour
```yml
  - platform: template
    sensors:
      pvoutput_v1:
        value_template: "{{ states('sensor.growatt_total_energy_today') | float * 1000 | round(2) }}"
        friendly_name: 'PVoutput formatted V1'
        unit_of_measurement: 'Watt'

      pvoutput_v3:
        value_template: "{{ states('sensor.energy_per_day') | float * 1000 | round(2) }}"
        friendly_name: 'PVoutput formatted v3'
        unit_of_measurement: 'Watt'

      energy_consumption_total_kwh:
        value_template: "{{ states('sensor.energy_consumption_tarif_1') | float + states('sensor.energy_consumption_tarif_2') | float | round(2) }}"
        friendly_name: 'kWh (Total)'
        unit_of_measurement: 'kWh'

utility_meter:
  energy_per_day:
    source: sensor.energy_consumption_total_kwh
    cycle: daily
```
### v4 real power usage
To calculate the real total power usage (Generated Solar - Return + Consumption) an additional sensor was created.  
Once again it was necessary to get the values in watt hour.  
```yml
  - platform: template
    sensors:
      power_consumption_watts:
        value_template: "{{ states('sensor.power_consumption') | float * 1000 | round(1) }}"
        friendly_name: 'P1 Usage'
        unit_of_measurement: 'Watt'

      power_production_watts:
        value_template: "{{ states('sensor.power_production') | float * 1000 | round(1) }}"
        friendly_name: 'P1 Return'
        unit_of_measurement: 'Watt'

      power_total_usage:
        value_template: "{{ states('sensor.growatt_total_output_power') | float - states('sensor.power_production_watts') | float + states('sensor.power_consumption_watts') | float }}"
        friendly_name: 'Real usage'
        unit_of_measurement: 'Watt'
```
