


var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }),
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([5.2375931841654655, 60.51416117978438]),
    zoom: 6.5
  })
});

function getVectorLayer(filePath,layerName){
    const str = new ol.layer.VectorImage({
        source: new ol.source.Vector({
            url: filePath,
            format: new ol.format.GeoJSON()
        }),
        visible: true,
        title: layerName
    })
    return str;
}

const counties ={
  hq00: "./data/query-map-03.geojson",
  mp: "./data/res-query-map-03.geojson",
}

for (key in counties){
    map.addLayer(getVectorLayer(counties[key],key));
}
