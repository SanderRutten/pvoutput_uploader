# Upload HomeAssistant data to PVOutput
import json, subprocess, argparse
import requests, sched, time
from datetime import datetime

s = sched.scheduler(time.time, time.sleep)
def loop_pvoutput(sc):
  date = datetime.today().strftime('%Y%m%d')
  time = datetime.today().strftime('%H:%M:%S')

# Idee voor 0.3:
# HACS support

  # PVOutput API
  PVoutputURL = 'https://pvoutput.org/service/r2/addstatus.jsp'
  # For testing you can use https://webhook.site and replace URL below with your temporary unique link
  # PVoutputURL = 'https://webhook.site/f682a4c0-fee7-4ca3-bdfa-a28db48be493'

  # Read variabless from options.json
  parser = argparse.ArgumentParser()
  parser.add_argument("pvoutput_apikey")
  parser.add_argument("pvoutput_systemid")
  parser.add_argument("ha_host")
  parser.add_argument("ha_token")
  parser.add_argument("entity_v1")
  parser.add_argument("entity_v2")
  parser.add_argument("entity_v3")
  parser.add_argument("entity_v4")
  parser.add_argument("entity_v5")
  parser.add_argument("entity_v6")

  args = parser.parse_args()
  pvoutput_apikey = args.pvoutput_apikey
  pvoutput_systemid = args.pvoutput_systemid
  ha_host = args.ha_host
  ha_token = args.ha_token
  entity_v1 = args.entity_v1
  entity_v2 = args.entity_v2
  entity_v3 = args.entity_v3
  entity_v4 = args.entity_v4
  entity_v5 = args.entity_v5
  entity_v6 = args.entity_v6

  # Authenticate to Home Assistant with correct token
  headers = {
    'Authorization': 'Bearer ' + ha_token,
    'Content-Type': 'application/json',
  }

  # Get JSON from devices
  v1_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v1, headers=headers)
  v2_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v2, headers=headers)

  # JSON response to text
  v1_parse = json.loads(v1_json.text)
  v2_parse = json.loads(v2_json.text)

  # Read the value 'state'
  api_v1 = (v1_parse["state"])
  api_v2 = (v2_parse["state"])

  # Optional sensors
  if entity_v3 == 'sensor.none':
    api_v3 = '0'
  else:
    v3_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v3, headers=headers)
    v3_parse = json.loads(v3_json.text)
    api_v3 = (v3_parse["state"])

  if entity_v4 == 'sensor.none':
    api_v4 = '0'
  else:
    v4_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v4, headers=headers)
    v4_parse = json.loads(v4_json.text)
    api_v4 = (v4_parse["state"])

  if entity_v5 == 'sensor.none':
    api_v5 = '0'
  else:
    v5_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v5, headers=headers)
    v5_parse = json.loads(v5_json.text)
    api_v5 = (v5_parse["state"])

  if entity_v6 == 'sensor.none':
    api_v6 = '0'
  else:
    v6_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v6, headers=headers)
    v6_parse = json.loads(v6_json.text)
    api_v6 = (v6_parse["state"])

# Run curl to upload data
  cmd=('curl -s -d "d=%s" -d "t=%s" -d "v1=%s" -d "v2=%s" -d "v3=%s" -d "v4=%s" -d "v5=%s" -d "v6=%s" \
  -H "X-Pvoutput-Apikey: %s" -H "X-Pvoutput-SystemId: %s" "%s"' \
  %(date, time, api_v1, api_v2, api_v3, api_v4, api_v5, api_v6, pvoutput_apikey, pvoutput_systemid, PVoutputURL))
  print('PVoutput uploading @ ' + date +  ' : ' + time)
  print('V1 ' + api_v1)
  print('V2 ' + api_v2)
  print('V3 ' + api_v3)
  print('V4 ' + api_v4)
  print('V5 ' + api_v5)
  print('V6 ' + api_v6)

  subprocess.call(cmd, shell=True)

  s.enter(300, 1, loop_pvoutput, (sc,))
s.enter(300, 1, loop_pvoutput, (s,))
s.run()
