import yaml
import json
import os
from os.path import isfile, join
import sys
import couchdb
import pyproj
from pyproj import Proj, transform
from shapely.geometry import Polygon
from shapely.geometry import shape, GeometryCollection


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

# Kartverket
inDir = (f'{METCAPROOT}/data/sources/kartverket/in')
outDir = (f'{METCAPROOT}/data/sources/kartverket/out')
kvKommuner = f'{inDir}/Basisdata_0000_Norge_25833_Kommuner_GeoJSON.geojson'
kvFylker = f'{inDir}/Basisdata_0000_Norge_25833_Fylker_GeoJSON.geojson'
nameSpace = 'no.geonorge'

nameSpaceLowRes = 'no.met'
thisProductDataProvider = 'https://www.met.no/'


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


def kvToMetCoords(crsIn, crsOut, coordinates):
    # input:
    #          String - CRS of input coordinates e.g. epsg:25833 
    #          String - CRS of output coordinates e.g. epsg:4326
    #          List - coordinates list of lists of [[x0,y0],[x1,y1],...]
    # output:  
    #          List - transformed coordinates as list of lists
    #        
    # comments:
    #          this function is not generic
    transformedCoords = []
    transformer = pyproj.Transformer.from_crs(crsIn, crsOut)
    for i in range(len(coordinates)):
        lat, lon = transformer.transform(coordinates[i][0], coordinates[i][1])
        transformedCoords.append([lon, lat])

    return transformedCoords


def countX(list, x):
    return list.count(x) 


def getFeatures(df, administrativeId):
    features = []
    if('administrative_enheter.fylke' in df):
        for feature in df['administrative_enheter.fylke']['features']:
            if (feature['properties']['fylkesnummer'] == administrativeId):
                features.append(feature)
    if('administrative_enheter.kommune' in df):
        for feature in df['administrative_enheter.kommune']['features']:
            if (feature['properties']['kommunenummer'] == administrativeId):
                features.append(feature)
    return features


def getlowResGeojson(inGeojson, tolerance, preserve_topology=True):
    df = dict(inGeojson)
    lrdf = dict(inGeojson)
    removeFromPeoperties = ['lokalid', 'navnerom', 'versjonid',
                            'datafangstdato', 'oppdateringsdato',
                            'datauttaksdato', 'opphav']
    # need this if input GeoJSON source is
    # CouchDB since "_rev" element is universal in CouchDB
    try:
        lrdf.pop("_rev")
    except Exception as e:
        print((f'key exception: {e}'))
        pass
    lrdf['_id'] = (f"lr_{df['_id']}")
    lrdf['uuid'] = cf.getUUID(
        thisProductDataProvider, lrdf['_id'], humanString=nameSpaceLowRes)
    lrdf['comment'] = (f"Resampled from {df['_id']} with UUID: {df['uuid']}")
    for i in range(len(df['features'])):
        for j in range(len(df['features'][i]['geometry']['coordinates'])):
            poly = Polygon(df['features'][i]['geometry']['coordinates'][j])
            lrpoly = poly.simplify(tolerance, preserve_topology=True)
            lrx, lry = lrpoly.exterior.xy
            coords = []
            for k in range(len(lrx)):
                coords.append([lrx[k], lry[k]])
            lrdf['features'][i]['geometry']['coordinates'][j] = coords
            try:
                for k in removeFromPeoperties:
                    lrdf['features'][i]['properties'].pop(k)
            except Exception as e:
                print(e)
                pass
    return lrdf


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


# set up replication
source = configObj['metfare_couchDb']
target = configObj['couchDb']

replication = {
    "_id": (f"{source.get('FQDN')}_to_{source.get('FQDN')}"),
    "source":  {
        "url": (f"{source.get('protocol')}://{source.get('FQDN')}/{source.get('capDb')}"),
        "auth": {
            "basic": {
                "username": (f"{source.get('username')}"),
                "password": (f"{source.get('password')}")
            }
        }
    },
    "target": {
        "url": (f"{target.get('protocol')}://{target.get('FQDN')}:{target.get('port')}/{target.get('capDb')}"),
        "auth": {
            "basic": {
                "username": (f"{target.get('username')}"),
                "password": (f"{target.get('password')}")
            }
        }
    },
    "create_target":  True,
    "continuous": True
}
db = couch['_replicator']
try:
    db.save(replication)
except Exception as e:
    print(f'Could not save document : {e}')
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
MapViews = [bbox,nameId,nameIdType,area,admId,nameIdGeometry,poly]

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

def getUnitCounts(kvFylker,kvKommuner):
  # first pass to extract all unit ids and counts


  # keep track of all units
  administrativeIdKList = []
  administrativeIdFList = []
  administrativeIdKDict = {}
  administrativeIdFDict = {}

  # define and initialize variables
  kvInFile = [kvFylker,kvKommuner]
  for kvif in kvInFile:
    if kvif == kvKommuner:
      topKey = "administrative_enheter.kommune"
      adminUnitIdKey = "kommunenummer"
      print(f"Reading kommune data. 'topKey' set to {topKey}, 'adminUnitIdKey set to {adminUnitIdKey}.")
    elif kvif == kvFylker:
      topKey = "administrative_enheter.fylke"
      adminUnitIdKey = "fylkesnummer"
      print(f"Reading kommune data. 'topKey' set to {topKey}, 'adminUnitIdKey set to {adminUnitIdKey}.")
    else:
      print("No input file found.")

    with open(kvif) as f:
      df = json.load(f)

    crsIn = df[topKey]['crs']['properties']['name'].lower()
    crsOut = "EPSG:4326".lower()

    for ff in range(len(df[topKey]['features'])):
      if(df[topKey]['features'][ff]['properties']['objtype'].lower() == 'kommune'):
          administrativeIdKList.append(df[topKey]['features'][ff]['properties']['kommunenummer'])
      if(df[topKey]['features'][ff]['properties']['objtype'].lower() == 'fylke'):
          administrativeIdFList.append(df[topKey]['features'][ff]['properties']['fylkesnummer'])

  for elem in administrativeIdFList:
      administrativeIdFDict[elem] = countX(administrativeIdFList,elem)  
  for elem in administrativeIdKList:
      administrativeIdKDict[elem] = countX(administrativeIdKList,elem)
  return (administrativeIdFDict,administrativeIdKDict)    

fDict,kDict = getUnitCounts(kvFylker,kvKommuner)

def exportGeojson(inFile,adminUnit):
    # create the GeoJSON files
    '''
    inFile: one of Basisdata_0000_Norge_25833_Kommuner_GeoJSON.geojson 
            or 
            Basisdata_0000_Norge_25833_Fylker_GeoJSON.geojson
    
    adminUnit: string - one of "fylke" or "kommune" 
    '''
    db = couch['map']

    topKey = (f'administrative_enheter.{adminUnit}')
    if(adminUnit == 'fylke'):
        adminUnitId = 'fylkesnummer'
        iDDict = fDict 
    if(adminUnit == 'kommune'):
        adminUnitId = 'kommunenummer'
        iDDict = kDict 

    with open(inFile) as f:
        df = json.load(f)


    for k,v in iDDict.items():
        features = getFeatures(df,k)

        crsIn = df[topKey]['crs']['properties']['name'].lower()
        crsOut = "EPSG:4326".lower()


        for i in range(len(features)):
            subPolyBounds = []
            subPolyAreas = []
            for j in range(len(features[i]['geometry']['coordinates'])):
                lonlatCoords = kvToMetCoords(crsIn,crsOut,features[i]['geometry']['coordinates'][j])
                poly=Polygon(lonlatCoords)
                features[i]['geometry']['coordinates'][j]=lonlatCoords
                subPolyBounds.append(poly.bounds) 
                subPolyAreas.append(poly.area)
            features[i]['properties']['bbox'] = subPolyBounds[subPolyBounds.index(max(subPolyBounds))]
            features[i]['properties']['area'] = subPolyAreas[subPolyAreas.index(max(subPolyAreas))]
            features[i]['properties']['crs'] = crsOut

        geographicUnit = {}
        geographicUnit['_id'] = (f'{adminUnit}_{k}')
        geographicUnit['objtype'] = adminUnit.capitalize()
        geographicUnit['source'] = 'https://kartverket.no/'
        geographicUnit['uuid'] = cf.getUUID(features[0]['properties']['navnerom'],k,humanString=nameSpace)
        geographicUnit['administrativeName'] = features[0]['properties']['navn']
        geographicUnit['administrativeId'] = features[0]['properties'][adminUnitId]
        geographicUnit['type'] = 'FeatureCollection'

        geographicUnit['features']=features
    
        # save to CouchDB
        try:
            db.save(geographicUnit)
        except Exception as e:
            print(e)

        fileName = (f"{outDir}/{geographicUnit['_id']}.geojson")
        

        
        with open(fileName, 'w', encoding='utf-8') as f:
           json.dump(geographicUnit, f, ensure_ascii=False, indent=4)
           os.chmod(fileName,0o664)
    
        # with open(fileName, 'w', encoding='utf-8') as f:
        #     if os.path.isfile(fileName):
        #         raise FileExistsError(fileName)
        #     else:
        #         json.dump(geographicUnit, f, ensure_ascii=False, indent=4)

exportGeojson(kvKommuner,'kommune')

exportGeojson(kvFylker,'fylke')

db = couch['lrmap']
base_path = outDir
file_ls = [f for f in os.listdir(base_path) if isfile(join(base_path, f))]

for f in file_ls:

    inGeojson=(f"{base_path}/{f}")

    with open(inGeojson) as f:
        inGeojson = json.load(f)
    tolerance = 0.02 if inGeojson['objtype'].lower() == 'fylke' else 0.003
    lrdf = getlowResGeojson(inGeojson,tolerance,preserve_topology=False)
    # save to CouchDB
    try:
        db.save(lrdf)
    except Exception as e:
        print(e)
    f.close()

    fileName = (f"{outDir}/lowres/{lrdf['_id']}.geojson")
    
    with open(fileName, 'w', encoding='utf-8') as f:
       json.dump(lrdf, f, ensure_ascii=False, indent=4)
       os.chmod(fileName,0o664)
    f.close()
