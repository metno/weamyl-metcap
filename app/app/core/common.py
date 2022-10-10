from shapely.geometry import Polygon
from app.db.database import couch
import json
import requests
import uuid


class Common():

    def __init__(self) -> None:
        pass

    def getBbox(self, bounds):
        self.bbox = Polygon([
                [bounds[0], bounds[1]],
                [bounds[2], bounds[1]],
                [bounds[2], bounds[3]],
                [bounds[0], bounds[3]]
            ])
    
        return self.bbox
    
    def getNameNor(self, nameList):
        for elem in nameList:
            if elem['sprak'] == 'nor':
                return elem['navn']
        return "No name found"

    def getQueryPoly(self, query):
        if(query['type'] == 'FeatureCollection'):
            self.poly = Polygon(query['features'][0]['geometry']['coordinates'][0])
        if(query['type'] == 'Feature'):
            self.poly = Polygon(query['geometry']['coordinates'][0])
        return self.poly

    def getBounds(self, query):
        self.poly = self.getQueryPoly(query)
        return self.poly.bounds   
          
    def boundsIntersect(self, sourceBounds, searchBounds):
        if(searchBounds[0] > sourceBounds[2] or searchBounds[1] > sourceBounds[3] or searchBounds[2] < sourceBounds[0] or searchBounds[3] < sourceBounds[1]):
            return False
        else:
            return True

    def getDoc(self, db, id):
        """
        input: mapDb|capDb|customMapDb database document id
        outpu: mapDb|capDb|customMapDb ddatabae document
        """
        response, status = couch.get(f'/{db}/{id}')
        return json.loads(response.content)

    def findMatchingTags(self, db, query):
        """filter on all tags present in query first"""
        pass

    def findMatchingBounds(self, db, searchBounds):
        self.matched = []
        response, status = couch.get(f'/{db}/_design/bbox/_view/bbox')
        jresponse = json.loads(response.content)
        for row in jresponse['rows']:
            if (self.boundsIntersect(row['key'], searchBounds)):
                self.matched.append(row['id'])
        return self.matched

    def findMatchingPolys(self, db, query, iDList):
        self.matchedDocIdList = []
        self.searchPoly = self.getQueryPoly(query)
        self.iDList = self.getViewListString(iDList)
        response, status = couch.get(f'/{db}/_design/nameIdGeometry/_view/nameIdGeometry?keys={self.iDList}')
        rows = response.json()['rows']
        for row in rows:
            sourcePoly = Polygon(row['value'][2]['coordinates'][0])
            if "cutoff" in query:
                if(self.polyOverlaps(sourcePoly, self.searchPoly, cutoff=query['cutoff'])):
                    self.matchedDocIdList.append(row['id'])
            else:
                if(self.polyOverlaps(sourcePoly, self.searchPoly) or self.searchPoly.contains(sourcePoly)):
                    self.matchedDocIdList.append(row['id'])
        return(self.matchedDocIdList)   

    def polyOverlaps(self, sourcePoly, searchPoly, cutoff=0.2):
        self.sourcePoly = sourcePoly
        self.searchPoly = searchPoly
        self.cutoff = cutoff
        if(self.searchPoly.intersects(self.sourcePoly)):
            if((self.searchPoly.intersection(self.sourcePoly)).area/self.sourcePoly.area >= cutoff):
                return True
        return False

    def readQuery(self, query):
        self.keys = query.keys()
        return query


    def getViewListString(self, iDList):
        self.iDList = '","'.join(iDList)
        self.iDList = '["'+self.iDList+'"]'
        return self.iDList


    def getUUID(self,nameSpace, datasetId, humanString=""):
        '''
        Creates Universally Unique IDentifier (UUID) objects according to RFC 4122
        based on data owner name space and dataset identifier.

        dependency: uuid

        input: 
            nameSpace - namespace for data owner
            datasetId - unique dataset identifier issued by data owner
            humanString - optional string for human readability. UUID output will be humanString:uuid
        output:
            UUID string
        '''
        self.uuid = (f'{humanString}:{str(uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_URL, nameSpace), datasetId))}')
        return self.uuid

###############################################################################


cf = Common()
