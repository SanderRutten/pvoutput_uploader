#!/usr/bin/with-contenv bashio
CONFIG_PATH=/data/options.json
pvoutput_apikey=$(jq --raw-output ".pvoutput_apikey" $CONFIG_PATH)
pvoutput_systemid=$(jq --raw-output ".pvoutput_systemid" $CONFIG_PATH)
ha_host=$(jq --raw-output ".ha_host" $CONFIG_PATH)
ha_token=$(jq --raw-output ".ha_token" $CONFIG_PATH)
entity_v1=$(jq --raw-output ".entity_v1" $CONFIG_PATH)
entity_v2=$(jq --raw-output ".entity_v2" $CONFIG_PATH)
entity_v3=$(jq --raw-output ".entity_v3" $CONFIG_PATH)
entity_v4=$(jq --raw-output ".entity_v4" $CONFIG_PATH)

python3 ./pvoutput_uploader.py $pvoutput_apikey $pvoutput_systemid $ha_host $ha_token $entity_v1 $entity_v2 $entity_v3 $entity_v4
