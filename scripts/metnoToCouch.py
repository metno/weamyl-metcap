
import numpy as np
# import geopandas
# import matplotlib.pyplot as plt
from shapely.geometry.polygon import Polygon
import json
from shapely.geometry import shape, GeometryCollection
import yaml
import couchdb
import os
from os.path import isfile, join
import sys

new_path = r'../app'
if not new_path in (sys.path):
    sys.path.append(new_path)
print(">"*17 +" system path is:")
print(sys.path)
print(">"*17)

from app.core.common import cf

# The config is not distributed. File must be kept safe. 
configFileDefault = "/opt/metcap/etc/config.yml"
configFile = os.environ.get('METCAP_CONFIG_FILE', configFileDefault)


def getConfig(filePath):
    with open(filePath) as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e)

def getCouchConnection(configObj):
    c = configObj['couchDb']
    couchConnectionString = f"{c.get('protocol')}://{c.get('username')}:{c.get('password')}@{c.get('FQDN')}:{c.get('port')}"
    try:
        return couchdb.Server(couchConnectionString)
    except Exception as e:
        print(e)

couch = getCouchConnection(getConfig(configFile))




inDir = "../data/sources/metno/out/lowres"
inFile = f'{inDir}/lr_fylke_21.geojson'
with open(inFile) as f:
    df= json.load(f)

db = couch['lrmap']
# save to CouchDB
try:
    db.save(df)
except Exception as e:
    print(e)





inDir = "../data/sources/metno/out/lowres"
inFile = f'{inDir}/lr_kommune_2111.geojson'
with open(inFile) as f:
    df= json.load(f)

db = couch['lrmap']
# save to CouchDB
try:
    db.save(df)
except Exception as e:
    print(e)





inDir = "../data/sources/metno/out"
inFile = f'{inDir}/fylke_21.geojson'
with open(inFile) as f:
    df= json.load(f)

db = couch['map']
# save to CouchDB
try:
    db.save(df)
except Exception as e:
    print(e)




inDir = "../data/sources/metno/out"
inFile = f'{inDir}/kommune_2111.geojson'
with open(inFile) as f:
    df= json.load(f)

db = couch['map']
# save to CouchDB
try:
    db.save(df)
except Exception as e:
    print(e)

