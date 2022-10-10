from shapely.geometry import Polygon
# from app.db.database import couch
# import json
# import requests
# import uuid
from datetime import datetime
from logging import exception
from math import floor
from app.core.common import cf
from app.db.database import couch



class WCommon():

    def __init__(self) -> None:
        pass

    def getCapEpoch(self, capTimestamp):
        self.dateTimeObj = datetime.strptime(capTimestamp, "%Y-%m-%dT%H:%M")    
        return floor((self.dateTimeObj - datetime(1970, 1, 1)).total_seconds())

    def getQueryString(self, query):
        self.query = query
        self.qs = ''
        if all(key in self.query for key in ('db', 'design', 'view', 'startkey', 'endkey')):
            self.qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?startkey={self.query["startkey"]}&endkey={self.query["endkey"]}'
        elif all(key in self.query for key in ('db', 'design', 'view', 'key')):
            self.qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"'
        elif all(key in self.query for key in ('db', 'design', 'view', 'keys')):
            self.keyList = cf.getViewListString(self.query["keys"])
            self.qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?keys={self.keyList}'
        elif all(key in self.query for key in ('db', 'design', 'view')):
            self.qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}'
        elif all(key in self.query for key in ('db', 'id')):
            self.qs = f'/{self.query["db"]}/{self.query["id"]}'
        else:
            raise Exception("Malformed query")
        return self.qs

    def findMatchingBounds(self, searchBounds):
        self.q = {'db': 'warnings',
                  'design': 'metcap',
                  'view': 'bbox'
                  }
        self.qs = wcf.getQueryString(self.q)
        self.result = []
        response, status = couch.get(self.qs)
        for doc in response.json()['rows']:
            if cf.boundsIntersect(searchBounds, doc['key']):
                self.result.append(doc['id'])
        return self.result

    def getPolygon(self, coordinates):
        return Polygon(coordinates)

    def getPolygonArea(self, coordinates):
        return Polygon(coordinates).area
###############################################################################


wcf = WCommon()
