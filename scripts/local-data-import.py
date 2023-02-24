import yaml
import os
import sys
import couchdb
import json
from tqdm import tqdm
from pathlib import Path
import logging
log = logging.getLogger(__name__)
from getpass import getpass
import re
from tqdm import tqdm

# recommended value is /opt/metcap
METCAPROOT = '..'

new_path = (f'{METCAPROOT}/app')
if new_path not in (sys.path):
    sys.path.append(new_path)
print(">"*17 + " system path is:")
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


configObj = getConfig(configFile)
couch = getCouchConnection(configObj)
# couch = getCouchConnection(getConfig(configFile))


######################################################################
#                                                                    #
# import local (test) data                                           #
#                                                                    #
######################################################################

# dataRootDir = 'metcap-api/data/couchdb'
dataRootDir = '/opt/metcap/data_sources'
countries = ['norway', 'romania']
dataDirs = ['cmap', 'extremenames', 'incidents', 'lrmap', 'map', 'validations', 'warnings']
gre = re.compile('(.*\.geojson$)',flags=re.IGNORECASE)
xre = re.compile('(.*\.xml$)',flags=re.IGNORECASE)

def readGeoJSON (filePath):
    f = open( filePath , "rb" )
    data = json.load(f)
    f.close()
    return data

def saveToDB(data, database):
    try:
        log.debug(f"\n\nSaving {data['_id']} to {database}")

        if data['_id'] in database:
            print(f"**** {data['_id']} **** already exists, skipping item")
            database.delete(database['_id'])
        else:
            database.save(data)

    except couchdb.http.ResourceConflict:
        log.exception(f"Could not update for filename. See log.")
        pass

for c in tqdm(countries):
    for d in tqdm(dataDirs):
        try:
            for fn in tqdm(os.listdir(f'{dataRootDir}/{c}/{d}')):
                if gre.match(f'{dataRootDir}/{c}/{d}/{fn}'):
                    # is GeoJSON. save to db
                    data = readGeoJSON(f'{dataRootDir}/{c}/{d}/{fn}')
                    try:
                        saveToDB(data,couch[d])
                    except:
                        pass
                    if xre.match(data['source']):
                        try:
                            # source is *.xml CAP. Attach it to document
                            sources = data["source"].replace(" ", "").split(',')
                            sf = list(filter(xre.match, sources))[0]
                            souceAttachement = open(f'{dataRootDir}/{c}/{d}/{sf}','rb')
                            couch[d].put_attachment(couch[d][data['_id']], souceAttachement, filename=sf)
                        except Exception as e:
                            print(e)
                            pass
        except:
            pass