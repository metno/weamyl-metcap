curl -X 'POST'   'http://localhost:7532/api/v1/cap/'   -H 'accept: application/json'   -d @query-cap-00.geojson | jq > res-query-cap-00-list.txt
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220710121539 | jq > res-query-cap-00a-2.49.0.1.578.0.20220710121539.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220615070509 | jq > res-query-cap-00b-2.49.0.1.578.0.20220615070509.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220710094104 | jq > res-query-cap-00c-2.49.0.1.578.0.20220710094104.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220614095614 | jq > res-query-cap-00d-2.49.0.1.578.0.20220614095614.geojson


curl -X 'POST'   'http://localhost:7532/api/v1/cap/'   -H 'accept: application/json'   -d @query-cap-polygon.geojson | jq > res-query-cap-polygon-list.txt
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220627103815 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220627103815.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220803114347 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220803114347.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220625104102 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220625104102.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220723142521 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220723142521.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802101753 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220802101753.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220624101914 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220624101914.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802103450 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220802103450.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220624093218 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220624093218.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220625094437 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220625094437.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802074644 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220802074644.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220527101842 | jq > res-query-cap-polygon-2.49.0.1.578.0.20220527101842.geojson

curl -X 'POST'   'http://localhost:7532/api/v1/cap/'   -H 'accept: application/json'   -d @query-cap-polygon-august.geojson | jq > res-query-cap-polygon-august-list.txt
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802101753 | jq > res-query-cap-polygon-august-2.49.0.1.578.0.20220802101753.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220803114347 | jq > res-query-cap-polygon-august-2.49.0.1.578.0.20220803114347.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802103450 | jq > res-query-cap-polygon-august-2.49.0.1.578.0.20220802103450.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802074644 | jq > res-query-cap-polygon-august-2.49.0.1.578.0.20220802074644.geojson

curl -X 'POST'   'http://localhost:7532/api/v1/cap/'   -H 'accept: application/json'   -d @query-cap-polygon-august-Yellow.geojson | jq > res-query-cap-polygon-august-Yellow-list.txt
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802074644 | jq > res-query-cap-polygon-august-Yellow-2.49.0.1.578.0.20220802074644.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802103450 | jq > res-query-cap-polygon-august-Yellow-2.49.0.1.578.0.20220802103450.geojson
curl http://admin:d0gf00d@127.0.0.1:5984/warnings/2.49.0.1.578.0.20220802101753 | jq > res-query-cap-polygon-august-Yellow-2.49.0.1.578.0.20220802101753.geojson