# Upload HomeAssistant data to PVOutput
import json, subprocess, argparse
#import subprocess
#import requests
import requests, sched, time
from datetime import datetime

s = sched.scheduler(time.time, time.sleep)
def loop_pvoutput(sc):
  date = datetime.today().strftime('%Y%m%d')
  time = datetime.today().strftime('%H:%M:%S')

  # PVOutput API
  PVoutputURL = 'https://pvoutput.org/service/r2/addstatus.jsp'
  #PVoutputURL = 'https://webhook.site/f682a4c0-fee7-4ca3-bdfa-a28db48be493'

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

  args = parser.parse_args()
  pvoutput_apikey = args.pvoutput_apikey
  pvoutput_systemid = args.pvoutput_systemid
  ha_host = args.ha_host
  ha_token = args.ha_token
  entity_v1 = args.entity_v1
  entity_v2 = args.entity_v2
  entity_v3 = args.entity_v3
  entity_v4 = args.entity_v4

  # Authenticate to Home Assistant with correct token
  headers = {
    'Authorization': 'Bearer ' + ha_token,
    'Content-Type': 'application/json',
  }
  # Get JSON from devices
  v1_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v1, headers=headers)
  v2_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v2, headers=headers)
  v3_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v3, headers=headers)
  v4_json = requests.get('http://' + ha_host + ':8123/api/states/' + entity_v4, headers=headers)

  # JSON response to text
  v1_parse = json.loads(v1_json.text)
  v2_parse = json.loads(v2_json.text)
  v3_parse = json.loads(v3_json.text)
  v4_parse = json.loads(v4_json.text)

  # Read the value 'state'
  api_v1 = (v1_parse["state"])
  api_v2 = (v2_parse["state"])
  api_v3 = (v3_parse["state"])
  api_v4 = (v4_parse["state"])

  cmd=('curl -s -d "d=%s" -d "t=%s" -d "v1=%s" -d "v2=%s" -d "v3=%s" -d "v4=%s" \
  -H "X-Pvoutput-Apikey: %s" -H "X-Pvoutput-SystemId: %s" "%s"' \
  %(date, time, api_v1, api_v2, api_v3, api_v4, pvoutput_apikey, pvoutput_systemid, PVoutputURL))
  print('PVoutput uploading @ ' + date +  ' : ' + time)
  print('V1 ' + api_v1)
  print('V2 ' + api_v2)
  print('V3 ' + api_v3)
  print('V4 ' + api_v4)

  subprocess.call(cmd, shell=True)

  s.enter(300, 1, loop_pvoutput, (sc,))
s.enter(300, 1, loop_pvoutput, (s,))
s.run()
