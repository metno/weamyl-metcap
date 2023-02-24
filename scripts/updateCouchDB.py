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
# test{
os.listdir("metcap-api")
# test}

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

try:
    _global_changes = couch.create('_global_changes')
except Exception as e:
    print(e)
    pass 
try:
    _replicator = couch.create('_replicator')
except Exception as e:
    print(e)
    pass 
try:
    _users = couch.create('_users')
except Exception as e:
    print(e)
    pass 
try:
    map = couch.create('map')
except Exception as e:
    print(e)
    pass 
try:
    lrmap = couch.create('lrmap')
except Exception as e:
    print(e)
    pass 
try:
    cmap = couch.create('cmap')
except Exception as e:
    print(e)
    pass 
##
## metfare databases
##
try:
    incidents = couch.create('incidents')
except Exception as e:
    print(e)
    pass 
try:
    warnings = couch.create('warnings')
except Exception as e:
    print(e)
    pass 
try:
    extremenames = couch.create('extremenames')
except Exception as e:
    print(e)
    pass 
try:
    validations = couch.create('validations')
except Exception as e:
    print(e)
    pass 
##
## metfare archived databases
##
try:
    incidents = couch.create('archive_incidents')
except Exception as e:
    print(e)
    pass 
try:
    warnings = couch.create('archive_warnings')
except Exception as e:
    print(e)
    pass 

bbw = {
    "_id": "_design/bbw",
    "views": {
        "bbw": {
            "map": "function(doc) { if(doc.bbox) { emit(doc.bbox[0]); }}"
        }
    }
}
bbs = {
    "_id": "_design/bbs",
        "views": {
        "bbs": {
            "map": "function(doc) { if(doc.bbox) { emit(doc.bbox[1]); }}"
        }
    }
}
bbe = {
    "_id": "_design/bbe",
        "views": {
        "bbe": {
            "map": "function(doc) { if(doc.bbox) { emit(doc.bbox[2]); }}"
        }
    }
}
bbn = {
    "_id": "_design/bbn",
        "views": {
        "bbn": {
            "map": "function(doc) { if(doc.bbox) { emit(doc.bbox[3]); }}"
        }
    }
}

bboxFun = '''
function (doc) {
 if (typeof doc.type !== 'undefined' && doc.features) {
   doc.features.forEach(function(features) {
     emit(features.properties.bbox, {
       //features: features
     });
   });
 }
}
'''
bbox =  {
    "_id": "_design/bbox",
    "views": {
        "bbox": {
            "map":(f"{bboxFun}")
        }
    } 
}

# administrativeName, administrativeId  complex key
nameIdFun = '''
function(doc) { 
    if(doc.administrativeName && doc.administrativeId) { 
        emit(doc._id,[doc.administrativeName[0]['navn'],doc.administrativeId]); 
    }
}
'''
nameId = {
    "_id": "_design/nameId",
        "views": {
        "nameId": {
            "map":(f"{nameIdFun}")
        }
    }
}

nameIdTypeFun = '''
function(doc) { 
    if(doc.administrativeName && doc.administrativeId) { 
        emit(doc._id,[doc.administrativeName[0]['navn'],doc.administrativeId,doc.objtype]); 
    }
}
'''
nameIdType = {
    "_id": "_design/nameIdType",
        "views": {
        "nameIdType": {
            "map":(f"{nameIdTypeFun}")
        }
    }
}

# polygon area
areaFun = '''
function (doc) {
    if (typeof doc.type !== 'undefined' && doc.features) {
      doc.features.forEach(function(features) {
        emit(features.properties.area);
      });
    }
   }
'''
area = {
    "_id": "_design/area",
        "views": {
        "area": {
            "map":(f"{areaFun}")
        }
    }
}

# administrativeId - not usable for numerical comparison since leading zeros are used
admIdFun = '''
function(doc) { 
    if(doc.administrativeId) { 
        emit(doc.administrativeId); 
    }}
'''
admId = {
    "_id": "_design/admid",
        "views": {
        "admid": {
            "map":(f"{admIdFun}")
        }
    }
}

# administrativeName, administrativeId, geometry  complex key
nameIdGeometryFun = '''
function(doc) { 
    if(doc.administrativeName && doc.administrativeId) {
        doc.features.forEach(function(features){
            emit(doc._id,[doc.administrativeName,doc.administrativeId,features.geometry]); 
        })
    }}
'''
nameIdGeometry = {
    "_id": "_design/nameIdGeometry",
        "views": {
        "nameIdGeometry": {
            "map":(f"{nameIdGeometryFun}")        
        }
    }
}


# polygon coordinates
polyFun = '''
function(doc) { 
    if(doc.administrativeName && doc.administrativeId) {
        doc.features.forEach(function(features){
            emit(features.geometry.coordinates); 
        })
    }}
'''
poly = {
    "_id": "_design/poly",
        "views": {
        "poly": {
            "map":(f"{polyFun}")        
        }
    }
}

# list all Fylker
fylkeListFun = '''
function(doc) { 
    if(doc.type !== 'undefined' &&  doc.objtype === "Fylke") { 
        emit(doc.administrativeName,doc.administrativeId); 
    }}
'''
fylkeList = {
    "_id": "_design/fylkeList",
        "views": {
        "fylkeList": {
            "map":(f"{fylkeListFun}")        
        }
    }
}

# list all Kommuner
kommuneListFun = '''
function(doc) { 
    if(doc.type !== 'undefined' &&  doc.objtype === "Kommune") { 
        emit(doc.administrativeName,doc.administrativeId); 
    }}
'''
kommuneList = {
    "_id": "_design/kommuneList",
        "views": {
        "kommuneList": {
            "map":(f"{kommuneListFun}")        
        }
    }
}


# MapViews = [bbox,bbw,bbs,bbe,bbn,area,admid,poly,nameId,nameIdGeometry]
db = couch['map']
MapViews = [bbox, nameId, nameIdType, area, admId, nameIdGeometry, poly]

for view in MapViews:
    try:
        db.save(view)
    except Exception as e:
        print(f'Could not save view : {e}')

# LowResMapViews
db = couch['lrmap']
LowResMapViews = [fylkeList, kommuneList]

for view in LowResMapViews:
    try:
        db.save(view)
    except Exception as e:
        print(f'Could not save view : {e}')




designGroup = 'metcap'

#############################################
# incidents
#############################################
db = couch['incidents']
# incidents by name
getIncidentByName = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.name) { 
        emit(doc.name, null); 
    }}
'''
# incidents by description
getIncidentByDescription = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.description) { 
        emit(doc.description, null); 
    }}
'''
incidentsDesignGroup = {
    "_id": f"_design/{designGroup}",
        "views": {
        "description": {
            "map":(f"{getIncidentByDescription}")        
        },
        "name": {
            "map":(f"{getIncidentByName}")        
        }
    }
}
incidentViews = [incidentsDesignGroup]
for view in incidentViews:
    try:
        db.save(view)
    except Exception as e:
        print(f'Could not save view : {e}')


#############################################
# warnings
#############################################
db = couch['warnings']

# get number of seconds from epoch to onset
getEpochToOnset = '''
function(doc) {
    if (doc) {
        if (doc.onset) {
          const timestamp = doc.onset
          const utc = timestamp.concat("Z")
          const epoch = Math.floor(new Date(utc)/1000);
          emit(epoch, null)
        }
    }
}
'''
# get number of seconds from epoch to expires
# http://127.0.0.1:5984/warnings/_design/metcap/_view/expires?startkey=1653444000&endkey=1653462456
getEpochToExpires = '''
function(doc) {
    if (doc) {
        if (doc.expires) {
          const timestamp = doc.expires
          const utc = timestamp.concat("Z")
          const epoch = Math.floor(new Date(utc)/1000);
          emit(epoch, null)
        }
    }
}
'''
# warning by polygon
# output: features.geometry.coordinates
getWarningsByPolygon = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.features) {
        doc.features.forEach(function(features){
            emit(doc._id,features.geometry.coordinates[0]); 
        })
    }}
'''

# warning by archived
getWarningsByArchived = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.archived) { 
        emit(doc.archived,null); 
    }}
'''

# warning by incident
getWarningsByIncident = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.incident) { 
        emit(doc.incident,null); 
    }}
'''

# warning by author
getWarningsByAuthor = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.author) { 
        emit(doc.author,null); 
    }}
'''

# warning by onset
getWarningsByOnset = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.onset) { 
        emit(doc.onset,null); 
    }}
'''

# warning by expires
getWarningsByExpires = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.expires) { 
        emit(doc.expires,null); 
    }}
'''

# warning by phenomenon
getWarningsByPhenomenon = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.phenomenon) { 
        emit(doc.phenomenon,null); 
    }}
'''

# warning by status
getWarningsByStatus = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.status) { 
        emit(doc.status,null); 
    }}
'''

# warning by colour
getWarningsByColour = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.colour) { 
        emit(doc.colour,null); 
    }}
'''

# warning by certainty
getWarningsByCertainty = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.certainty) { 
        emit(doc.certainty,null); 
    }}
'''

# warning by severity
getWarningsBySeverity = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.severity) { 
        emit(doc.severity,null); 
    }}
'''

# warning by saved_at
getWarningsBySaved_at = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.saved_at) { 
        emit(doc.saved_at,null); 
    }}
'''

# warning by source
getWarningsBySource = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.source) { 
        emit(doc.source,null); 
    }}
'''

# warning by uuid
getWarningsByUuid = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.uuid) { 
        emit(doc.uuid,null); 
    }}
'''

# warning by areaDesc
getWarningsByAreaDesc = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.areaDesc["nb"]) { 
        emit(doc.areaDesc["nb"],null); 
    }}
'''

# warning by altitude
getWarningsByAltitude = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.altitude) { 
        emit(parseFloat(doc.altitude.match(/[a-zA-Z]+|[0-9]+/g)[0]),null); 
    }}
'''

# warning by ceiling
getWarningsByCeiling = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.ceiling) { 
        emit(parseFloat(doc.ceiling.match(/[a-zA-Z]+|[0-9]+/g)[0]),null); 
    }}
'''

# warning by msgType
getWarningsByMsgType = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.msgType) { 
        emit(doc.msgType,null); 
    }}
'''

# warning by references
getWarningsByReferences = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.references) { 
        emit(doc.references,null); 
    }}
'''


# warning by bbox
getWarningsByBBox = '''
function (doc) {
 if (typeof doc.type !== 'undefined' && doc.features) {
   doc.features.forEach(function(features) {
    if (features.geometry.bbox){
     emit(features.geometry.bbox, {
       //features: features
     })};
   });
 }
}
'''

# warning by coordinates
getWarningByCoordinates = '''
function(doc) { 
    if(typeof doc.type !== 'undefined' && doc.features) {
        doc.features.forEach(function(features){
            emit(features.geometry.coordinates); 
        })
    }}
'''

# warning by customArea
getWarningByCustomArea = '''
function(doc) { 
    if(doc.type !== 'undefined' && doc.features) {
        doc.features.forEach(function(features){
          if(features.properties.customArea === true){
            emit(doc.areaDesc.nb,null);
          }
        })
    }}
'''
# warning by capXML
getCapXMLNameByWarning = '''
function (doc) {
 if (typeof doc.type !== 'undefined' && doc.features && doc._attachments) {
    Object.keys(doc._attachments).forEach(function(k){
     if(doc._attachments[k].content_type == "text/xml"){
       emit(doc._id,k);
     }
    }
   )
  }
}
'''
# warning by capJSON
getCapJSONNameByWarning = '''
function (doc) {
 if (typeof doc.type !== 'undefined' && doc.features && doc._attachments) {
    Object.keys(doc._attachments).forEach(function(k){
     if(doc._attachments[k].content_type == "application/json"){
       emit(doc._id,k);
     }
    }
   )
  }
}
'''


waringsDesignGroup = {
    "_id": f"_design/{designGroup}",
      "views": {
        "archived":{"map":(f"{getWarningsByArchived}")},
        "incident":{"map":(f"{getWarningsByIncident}")},
        "author":{"map":(f"{getWarningsByAuthor}")},
        "onset":{"map":(f"{getWarningsByOnset}")},
        "expires":{"map":(f"{getWarningsByExpires}")},
        "phenomenon":{"map":(f"{getWarningsByPhenomenon}")},
        "status":{"map":(f"{getWarningsByStatus}")},
        "colour":{"map":(f"{getWarningsByColour}")},
        "certainty":{"map":(f"{getWarningsByCertainty}")},
        "severity":{"map":(f"{getWarningsBySeverity}")},
        "saved_at":{"map":(f"{getWarningsBySaved_at}")},
        "source":{"map":(f"{getWarningsBySource}")},
        "uuid":{"map":(f"{getWarningsByUuid}")},
        "areaDesc":{"map":(f"{getWarningsByAreaDesc}")},
        "altitude":{"map":(f"{getWarningsByAltitude}")},
        "ceiling":{"map":(f"{getWarningsByCeiling}")},
        "msgType":{"map":(f"{getWarningsByMsgType}")},
        "references":{"map":(f"{getWarningsByReferences}")},
        "epochToOnset":{"map":(f"{getEpochToOnset}")},
        "epochToExpires":{"map":(f"{getEpochToExpires}")},
        "polygon":{"map":(f"{getWarningsByPolygon}")},
        "bbox":{"map":(f"{getWarningsByBBox}")},
        "customArea":{"map":(f"{getWarningByCustomArea}")},
        "capXML":{"map":(f"{getCapXMLNameByWarning}")},
        "capJSON":{"map":(f"{getCapJSONNameByWarning}")},
        "coordinates":{"map":(f"{getWarningByCoordinates}")}
        }
    }

warningViews = [waringsDesignGroup]

for view in warningViews:
    try:
        db.save(view)
    except Exception as e:
        print(f'Could not save view : {e}')


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
                            # souceAttachement = open(f'{dataRootDir}/{c}/{d}/{data["source"]}','rb')
                            couch[d].put_attachment(couch[d][data['_id']], souceAttachement, filename=sf)
                        except Exception as e:
                            print(e)
                            pass
        except:
            pass