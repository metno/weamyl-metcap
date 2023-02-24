#! /bin/bash

metcap_container_id=$(docker ps -aqf "name=metcap-api")

# echo "docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-dev-kartverketToCouchdb.py"
# kvoutput=$(docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-dev-kartverketToCouchdb.py)



echo "docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-db-initialize.py"
customoutput=$(docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-db-initialize.py)

echo "docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-data-import.py"
customoutput=$(docker exec ${metcap_container_id} python3 /app/metcap-api/scripts/local-data-import.py)
