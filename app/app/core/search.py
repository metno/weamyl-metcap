import requests
# import json

from app.core.common import cf
from app.db.database import couch


class Search():
    def __init__(self) -> None:
        pass

    def mapSearchLowres(self, query, unit):
        self.query = query
        response, status = couch.get(
            f'/{couch.lrmapDb}/lr_{unit}_{self.query}'
            )
        return response.json()

    def buildKvMapSearchResult(self, response):
        if not isinstance(response, requests.models.Response):
            raise Exception(
                'Input is not an instance of requests.models.Response'
                )
        else:
            self.response = response
            self.searchResult = {}
            self.searchResult["type"] = "FeatureCollection"
            self.searchResult["features"] = []
            for doc in self.response.json()['rows']:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "administrativeName": cf.getNameNor(doc['value'][0]),
                        "administrativeId": doc['value'][1]
                        },
                    "geometry": doc['value'][2]   
                    }
                self.searchResult["features"].append(feature)
        return self.searchResult

    def mapSearch(self, query):
        self.query = query
        iDList = cf.findMatchingBounds(couch.mapDb, cf.getBounds(self.query))        
        self.resultIdList = cf.getViewListString(cf.findMatchingPolys(
            couch.mapDb, self.query, list(dict.fromkeys(iDList))))
        response, status = couch.get(
            f'/{couch.mapDb}/_design/nameIdGeometry/_view/nameIdGeometry?keys={self.resultIdList}'
            )
        return self.buildKvMapSearchResult(response)

    def getSearchShortResults(self, response):
        if not isinstance(response, requests.models.Response):
            raise Exception(
                'Input is not an instance of requests.models.Response'
                )
        else:
            self.response = response
            self.searchShortResultsCounty = []
            self.searchShortResultsMunicipality = []
            self.searchShortResultsDict = {}
            for doc in self.response.json()['rows']:
                if(doc['value'][2].lower() == 'fylke'):
                    self.searchShortResultsCounty.append([doc['value'][0],
                                                         doc['value'][1]])
                if(doc['value'][2].lower() == 'kommune'):
                    self.searchShortResultsMunicipality.append(
                        [doc['value'][0],
                         doc['value'][1]])
            if(len(self.searchShortResultsCounty) > 0):
                self.searchShortResultsDict['county'] = self.searchShortResultsCounty
            if(len(self.searchShortResultsMunicipality) > 0):
                self.searchShortResultsDict['municipality'] = self.searchShortResultsMunicipality

            return self.searchShortResultsDict

    def mapSearchShort(self, query):
        self.query = query
        iDList = cf.findMatchingBounds(couch.mapDb, cf.getBounds(self.query))
        self.resultIdList = cf.getViewListString(
            list(dict.fromkeys(
                cf.findMatchingPolys(
                    couch.mapDb, self.query, list(dict.fromkeys(iDList)))
                    )))
        response, status = couch.get(
            f'/{couch.mapDb}/_design/nameIdType/_view/nameIdType?keys={self.resultIdList}'
            )
        return self.getSearchShortResults(response)

    def mapGetLowresList(self, query):
        self.query = query
        unitList = []
        response, status = couch.get(
            f'/{couch.lrmapDb}/_design/{query}/_view/{query}')
        for doc in response.json()['rows']:
            unitList.append([cf.getNameNor(doc['key']), doc['value']])
        return unitList
        
###############################################################################


ms = Search()