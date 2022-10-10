from array import array
import datetime
from datetime import datetime, timezone
import requests
import math
from app.core.common import cf

# import json

from app.core.wcommon import wcf
from app.db.database import couch


class WSearch():
    def __init__(self) -> None:
        self.SEARCH_TAGS = [
                            "archived",
                            "author",
                            "certainty",
                            "colour",
                            "incident",
                            "msgType",
                            "phenomenon",                            
                            "severity",
                            "source",
                            "status",
                            # "uuid"
                            ]
        pass

    
    def getCList(self, query):
        # input: query dict
        # output: list
        # query example 
        #   query = {'db':'warnings',
        #            'design': 'metcap',
        #            'view':'phenomenon',
        #            'key': 'lightning'
        #            }
        self.query = query
        self.qs = wcf.getQueryString(self.query)
        self.result = []
        response, status = couch.get(self.qs)
        if len(response.json().keys()) >= 0:
            if('rows' in response.json().keys()):
                for doc in response.json()['rows']:
                    self.result.append(doc['id'])
                return self.result
            else:
                return response.json()

    def getWarningsArchivedList(self):
        # input:
        # output: list of CAP warning archive statuses in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'archived'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))

    def getWarningsAreaDescList(self):
        # input:
        # output: list of CAP warning area descriptions in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'areaDesc'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))


    def getWarningsAuthorList(self):
        # input:
        # output list of CAP warning authors in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'author'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result)) 

    def getWarningsCertaintyList(self):
        # input:
        # output list of CAP warning certainties in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'certainty'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))        
 
    def getWarningsColourList(self):
        # input:
        # output: list of CAP warning colours in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'colour'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))

    def getWarningsCustomAreaList(self):
        # input:
        # output: list of CAP warning custom areas in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'customArea'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))


    def getWarningsMsgTypeList(self):
        # input:
        # output: list of CAP warning message types in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'msgType'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))


    def getIncidentsNameList(self):
        # input:
        # output: list of CAP incident names in database
        self.query = {'db': 'incidents',
                      'design': 'metcap',
                      'view': 'name'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))

    def getIncidentsDescriptionList(self):
        # input:
        # output: list of CAP incident descriptions in database
        self.query = {'db': 'incidents',
                      'design': 'metcap',
                      'view': 'description'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))


    def getWarningsPhenomenonList(self):
        # input:
        # output: list of CAP warning phenomena in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'phenomenon'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))

    def getWarningsSeverityList(self):
        # input:
        # output list of CAP warning severities in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'severity'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))  

    def getWarningsStatusList(self):
        # input:
        # output list of CAP warning statuses in database
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'status'
                      }
        qs = wcf.getQueryString(self.query)
        result = []
        response, status = couch.get(qs)
        for doc in response.json()['rows']:
            result.append(doc['key'])
        return sorted(set(result))

    def getWarningsByIncidentId(self, id):
        # input: string id
        # output: cap id
        # query example 
        # '0000000008'
        # Incident IDs and names must be unique
        # 

        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'incident',
                      'key': id
                      }
        qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"'
        # qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"&include_docs=true'
        response, status = couch.get(qs)
        result = []
        if(not response.json()['rows']):
            return
        else:
            for doc in response.json()['rows']:
                result.append(doc['id'])
                # result.append(doc['doc'])
            return result

    # def getWarningsByIncidentDescription(self, description):
    #     # input: string description
    #     # output: cap
    #     # query example 
    #     # 'description'
    #     # Incident IDs and names must be unique
    #     # 

    #     incidentId = self.getIncidentByDescription(description)
    #     # test{
    #     print(incidentId)
    #     # test}
    #     self.query = {'db': 'warnings',
    #                   'design': 'metcap',
    #                   'view': 'incident',
    #                   'key': incidentId
    #                   }
    #     qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"'
    #     # qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"&include_docs=true'
    #     response, status = couch.get(qs)
    #     result = []
    #     if(not response.json()['rows']):
    #         return result
    #     else:
    #         for doc in response.json()['rows']:
    #             result.append(doc['id'])
    #             # result.append(doc['doc'])
    #         return result

    # def getIncidentByDescription(self, description):
    #     # input: description string 
    #     # output: incident id
    #     self.query = {'db': 'incidents',
    #                   'design': 'metcap',
    #                   'view': 'description',
    #                   'key': description
    #                   }
    #     qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"'
    #     # qs = wcf.getQueryString(self.query)
    #     response, status = couch.get(qs)
    #     result = []
    #     if(not response.json()['rows']):
    #         return
    #     else:
    #         for doc in response.json()['rows']:
    #             result.append(doc['id'])
    #         return str(result[0])


    def getWarningsByIncidentName(self, name):
        # input: string name
        # output: cap
        # query example 
        # 'Muninn'
        # Incident IDs and names must be unique
        # 

        incidentId = self.getIncidentByName(name)
        self.query = {'db': 'warnings',
                      'design': 'metcap',
                      'view': 'incident',
                      'key': incidentId
                      }
        qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"'
        # qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"&include_docs=true'
        response, status = couch.get(qs)
        result = []
        if(not response.json()['rows']):
            return result
        else:
            for doc in response.json()['rows']:
                result.append(doc['id'])
                # result.append(doc['doc'])
            return result

    def getIncidentByName(self, name):
        # input: name string 
        # output: incident id
        self.query = {'db': 'incidents',
                      'design': 'metcap',
                      'view': 'name',
                      'key': name
                      }
        qs = f'/{self.query["db"]}/_design/{self.query["design"]}/_view/{self.query["view"]}?key="{self.query["key"]}"'
        # qs = wcf.getQueryString(self.query)
        response, status = couch.get(qs)
        result = []
        if(not response.json()['rows']):
            return
        else:
            for doc in response.json()['rows']:
                result.append(doc['id'])
            return str(result[0])


    def getWarningsInPeriod(self, onset, expires):
        # input: time stamps from warning database ("onset", "expires")
        # output: list of valid CAP messages in the time interval
        # self.result = []
        self.dt = datetime.now(timezone.utc)
        self.utc_time = self.dt.replace(tzinfo=timezone.utc)
        self.utc_timestamp = math.floor(self.utc_time.timestamp())
        self.lq = {'db': 'warnings',
                   'design': 'metcap',
                   'view': 'epochToOnset',
                   'startkey': wcf.getCapEpoch(onset),
                   'endkey': self.utc_timestamp
                   }
        self.rq = {'db': 'warnings',
                   'design': 'metcap',
                   'view': 'epochToExpires',
                   'startkey': 0,
                   'endkey': wcf.getCapEpoch(expires)
                   }
        la = ws.getCList(self.lq)
        ra = ws.getCList(self.rq)

        return list(set(la).intersection(ra))

    def getWarningsTemporal(self, query):
        self.query = query
        return self.getWarningsInPeriod(self.query['onset'],self.query['expires'])

    def debug(self, query):
        self.query = query
        return self.getWarningsInPeriod(self.query['onset'],self.query['expires'])
        # return list(self.query.keys())

    def capPolygonSearch(self, query):
        self.query = query
        self.iDList = wcf.findMatchingBounds(cf.getBounds(self.query))        

        self.q = {'db': 'warnings',
                  'design': 'metcap',
                  'view': 'polygon',
                  'keys': self.iDList
                  }
        self.qs = wcf.getQueryString(self.q)
        self.result = []
        response, status = couch.get(self.qs)
        if len(response.json().keys()) >= 0:
            if('rows' in response.json().keys()):
                for doc in response.json()['rows']:
                    if 'cutoff' in self.query.keys():
                        if (cf.polyOverlaps(wcf.getPolygon(doc['value']), cf.getQueryPoly(self.query), cutoff=self.query['cutoff'])):
                            self.result.append(doc['id'])
                    else:
                        if (cf.polyOverlaps(wcf.getPolygon(doc['value']), cf.getQueryPoly(self.query))):
                            self.result.append(doc['id'])
                return self.result
            else:
                return response.json()
        return self.result

    def getWarningsInHeightRange(self, bottom, top):
        self.lq = {'db': 'warnings',
                   'design': 'metcap',
                   'view': 'altitude',
                   'startkey': bottom,
                   'endkey': 2e6
                   }
        self.rq = {'db': 'warnings',
                   'design': 'metcap',
                   'view': 'ceiling',
                   'startkey': 0,
                   'endkey': top
                   }
        la = ws.getCList(self.lq)
        ra = ws.getCList(self.rq)

        return list(set(la).intersection(ra))

    def getWarningsSpatial(self, query):
        self.query = query
        return self.getWarningsInHeightRange(self.query['altitude'],self.query['ceiling'])

    def capSearch(self, query):
        self.query = query
        return self.getCAPsIntersection(self.query,self.SEARCH_TAGS)

    def getCAPsIntersection(self,query,tags):
        rSets = []
        for t in tags:
            if t in query.keys():
                q = {'db': 'warnings',
                          'design': 'metcap',
                          'view': t,
                          'key': query[t]
                           }
                rSets.append(set(self.getCList(q)))
        if 'features' in query.keys():
            if query['features'][0]['geometry']['type'] == 'Polygon':
                rSets.append(set(self.capPolygonSearch(query)))
        if ('onset' in query.keys() and 'expires' in query.keys()):
            rSets.append(set(self.getWarningsInPeriod(query['onset'],query['expires'])))
        # test{
        # if ('altitude' in query.keys() and 'ceiling' in query.keys()):
        #     rSets.append(set(self.getWarningsInHeightRange(self.query['altitude'],self.query['ceiling'])))
        # test}
        # test{
        # for elem in set.intersection(*rSets):
        #     print(elem)
        # test}
        return set.intersection(*rSets)

    def capSearchLong(self,query):
        self.query = query
        self.query['db'] = 'warnings'
        documents = []
        idSet = self.getCAPsIntersection(self.query,self.SEARCH_TAGS)
        for elem in idSet:
            documents.append(elem)

        self.result = []
        for item in documents:
            qs = f'/{self.query["db"]}/{item}'
            response, status = couch.get(qs)
            self.result.append(response.json())
        return self.result
    
###############################################################################

ws = WSearch()
