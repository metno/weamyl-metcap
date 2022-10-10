
## API documentation

* http://localhost:7532/api/docs

## Examples

### GET

* get list of counties
```
curl -X 'GET' 'http://localhost:7532/api/v1/map/lowres/fylke/list/' -H 'accept: application/json'
```

* get list of municipalities

```
curl -X 'GET' 'http://localhost:7532/api/v1/map/lowres/kommune/list/' -H 'accept: application/json'
```

### POST

* get list of regions that overlap (name and number only). Note type of unit returned

```
curl -X 'POST'   'http://localhost:7532/api/v1/map/short/'   -H 'accept: application/json'   -d @svalbard.geojson
```

* get list of regions that overlap (GeoJSON)

```
curl -X 'POST'   'http://localhost:7532/api/v1/map/'   -H 'accept: application/json'   -d @svalbard.geojson
```

## Ways to validate/view GeoJSON 

* Use public service such as https://geojson.io/

* Use a JavaScript library such as https://openlayers.org to display GeoJSON features on a map layer of your choice. See https://openlayers.org/en/latest/examples/geojson.html

* Use an application such as https://wiki.gnome.org/Apps/Maps 
This option is quick and easy and allows you to view your GeoJSON files 
on your desktop. Once installed you can access the application either through 
the context menu or from the command line with 

```
gnome-maps svalbard.geojson res-svalbard.geojson
```