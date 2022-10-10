#! /bin/bash

metcap_container_id=$(docker ps -aqf "name=metcap-api")

echo "docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-dev-kartverketToCouchdb.py"
kvoutput=$(docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-dev-kartverketToCouchdb.py)

echo "docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-dev-metno-custom-couchdb.py"
customoutput=$(docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-dev-metno-custom-couchdb.py)
