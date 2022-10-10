# import asyncio
# import mimetypes
# from typing import Any, Counter, Optional
# from urllib import response

# # import httpx
import socket
from fastapi import APIRouter, Depends, HTTPException, Query, Request

# from app.core.search import ms
from app.core.wsearch import ws

FQDN = socket.getfqdn()
# # test{
# from fastapi import FastAPI, Response
# import prometheus_client
# from prometheus_client.core import CollectorRegistry
# from prometheus_client import Summary, Counter, Histogram, Gauge
# import time
# # test}

router = APIRouter()
# MAP_SUBREDDITS = ["maps"]

# test{
# _INF = float("inf")
# graphs = {}
# graphs['c'] = Counter('python_request_operations_total','The total number of processed requests')
# graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds',buckets=(1, 2, 5, 6, 10, _INF))
# test}


@router.get("/")
def greet() -> dict:
    """
    Returns a simple greeting message.
    """
    # # test{
    # start = time.time()
    # graphs['c'].inc()
    # time.sleep(0.600)
    # end = time.time()
    # graphs['h'].observe(end - start)
    # # test}

    return {
        "msg": "Welcome to METCAP CAP API at METNO!"
    }


@router.get("/archived/list/")
async def get_warnings_archived_list():
    """
    Returns list of current CAP warning archived statuses in the database.
    """
    return ws.getWarningsArchivedList()

@router.get("/areaDesc/list/")
async def get_warnings_areaDesc_list():
    """
    Returns list of current CAP warning area descriptions in the database.
    """
    return ws.getWarningsAreaDescList()

@router.get("/author/list/")
async def get_warnings_author_list():
    """
    Returns list of current CAP warning authors in the database.
    """
    return ws.getWarningsAuthorList()


@router.get("/certainty/list/")
async def get_warnings_certainty_list():
    """
    Returns list of current CAP warning certainties in the database.
    """
    return ws.getWarningsCertaintyList()


@router.get("/color/list/")
async def get_warnings_colour_list():
    """
    Returns list of current CAP warning colours in the database.
    """
    return ws.getWarningsColourList()

@router.get("/customArea/list/")
async def get_warnings_customArea_list():
    """
    Returns list of current CAP warning customAreas in the database.
    """
    return ws.getWarningsCustomAreaList()


@router.get("/incident/name/list/")
async def get_incidents_name_list():
    """
    Returns list of current CAP incident names in the database.
    """
    return ws.getIncidentsNameList()

@router.get("/incident/description/list/")
async def get_incidents_description_list():
    """
    Returns list of current CAP incident descriptions in the database.
    """
    return ws.getIncidentsDescriptionList()


@router.get("/msgType/list/")
async def get_warnings_msgType_list():
    """
    Returns list of current CAP warning message types in the database.
    """
    return ws.getWarningsMsgTypeList()


@router.get("/phenomenon/list/")
async def get_warnings_phenomenon_list():
    """
    Returns list of current CAP warning phenomena in the database.
    """
    return ws.getWarningsPhenomenonList()


@router.get("/severity/list/")
async def get_warnings_severity_list():
    """
    Returns list of current CAP warning severities in the database.
    """
    return ws.getWarningsSeverityList()


@router.get("/status/list/")
async def get_warnings_status_list():
    """
    Returns list of current CAP warning statuses in the database.
    """
    return ws.getWarningsStatusList()


@router.get("/{incidentId}")
async def get_warnings_by_incident_id(incidentId):
    """
    Returns list of current CAP warnings with given incident ID.
    """
    return ws.getWarningsByIncidentId(incidentId)


@router.get("/incident/{name}")
async def get_warnings_by_incident_name(name):
    """
    Returns list of current CAP warnings with given incident name.
    """
    return ws.getWarningsByIncidentName(name)

# @router.get("/incident/{description}")
# async def get_warnings_by_incident_description(description):
#     """
#     Returns list of current CAP warnings with given incident description.
#     """
#     return ws.getWarningsByIncidentDescription(description)

@router.post("/echo/", status_code=200)
async def echo_query(query: Request):
    """
    Echos the query data.
    """
    myQuery = await query.json()
    return myQuery

@router.post("/", status_code=200)
async def search(query: Request):
  """
    Returns array of GeoJSON CAP documents for complex searches.\n
    example query for service listening at \<Fully Qualified Domain Name\> and \<PORT\>:\n
        curl -X 'POST' 'https://<FQDN>:<PORT>/api/v1/cap/' -H 'accept: application/json' -d @query-cap-polygon-august-Yellow.geojson
        where query-cap-polygon-august-Yellow.geojson is a file with the contents:
        {
          "colour": "Yellow",
          "onset": "2022-08-01T00:00",
          "expires": "2022-08-03T16:00",
          "cutoff": 0.5,
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "properties": {},
              "geometry": {
                "type": "Polygon",
                "coordinates": [
                  [
                    [
                      7.91015625,
                      63.51427544737998
                    ],
                    [
                      5.09765625,
                      61.95961583829658
                    ],
                    [
                      4.998779296875,
                      61.60639637138628
                    ],
                    [
                      6.328125,
                      60.63548951646859
                    ],
                    [
                      9.228515625,
                      60.973107109199404
                    ],
                    [
                      10.283203125,
                      61.81466389468391
                    ],
                    [
                      9.700927734375,
                      62.58322502941986
                    ],
                    [
                      7.91015625,
                      63.51427544737998
                    ]
                  ]
                ]
              }
            }
          ]
        }

  """  
  myQuery = await query.json()
  return ws.capSearchLong(myQuery)

@router.post("/short/", status_code=200)
async def search(query: Request):
    """
    Returns CAP IDs for complex searches.\n
    example query for service listening at \<Fully Qualified Domain Name\> and \<PORT\>:\n
        curl -X 'POST' 'https://<FQDN>:<PORT>/api/v1/cap/' -H 'accept: application/json' -d @query-cap-polygon-august-Yellow.geojson
        where query-cap-polygon-august-Yellow.geojson is a file with the contents:
        {
          "colour": "Yellow",
          "onset": "2022-08-01T00:00",
          "expires": "2022-08-03T16:00",
          "cutoff": 0.5,
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "properties": {},
              "geometry": {
                "type": "Polygon",
                "coordinates": [
                  [
                    [
                      7.91015625,
                      63.51427544737998
                    ],
                    [
                      5.09765625,
                      61.95961583829658
                    ],
                    [
                      4.998779296875,
                      61.60639637138628
                    ],
                    [
                      6.328125,
                      60.63548951646859
                    ],
                    [
                      9.228515625,
                      60.973107109199404
                    ],
                    [
                      10.283203125,
                      61.81466389468391
                    ],
                    [
                      9.700927734375,
                      62.58322502941986
                    ],
                    [
                      7.91015625,
                      63.51427544737998
                    ]
                  ]
                ]
              }
            }
          ]
        }

    """
    myQuery = await query.json()
    return ws.capSearch(myQuery)

@router.post("/polygon/", status_code=200)
async def polygon_query(query: Request):
    """
    Returns CAP warning polygon search results.\n
    example query for service listening at \<Fully Qualified Domain Name\> and \<PORT\>:\n
        curl -X 'POST' 'https://<FQDN>:<PORT>/api/v1/cap/polygon/' -H 'accept: application/json'   -d @polygonSearch.geojson
        where polygonSearch.geojson is a file with the contents:
        {
          "cutoff" : 0.5,
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "properties": {},
              "geometry": {
                "type": "Polygon",
                "coordinates": [
                  [
                    [
                      4.7021484375,
                      60.48970392643919
                    ],
                    [
                      4.0869140625,
                      59.09138238455909
                    ],
                    [
                      7.437744140625,
                      57.73934950049299
                    ],
                    [
                      11.898193359375,
                      59.3051602771705
                    ],
                    [
                      10.294189453125,
                      60.44096253530979
                    ],
                    [
                      4.7021484375,
                      60.48970392643919
                    ]
                  ]
                ]
              }
            }
          ]
        }

    """
    myQuery = await query.json()
    return ws.capPolygonSearch(myQuery)


@router.post("/date/", status_code=200)
async def temporal_query(query: Request):
    """
    Returns list of CAP warnings for given temporal interval.\n
    example query for service listening at \<Fully Qualified Domain Name\> and \<PORT\>:\n
        curl -X 'POST' 'https://<FQDN>:<PORT>/api/v1/cap/date/' -H 'accept: application/json' -d '{"onset":"2022-06-27T12:00", "expires":"2022-07-02T07:00"}'

    """
    myQuery = await query.json()
    return ws.getWarningsTemporal(myQuery)

@router.post("/height/", status_code=200)
async def height_query(query: Request):
    """
    Returns list of CAP warnings for given height interval.\n
    example query for service listening at \<Fully Qualified Domain Name\> and \<PORT\>:\n
        curl -X 'POST' 'https://<FQDN>:<PORT>/api/v1/cap/height/' -H 'accept: application/json' -d '{"altitude":0,"ceiling":4000}'

    """
    myQuery = await query.json()
    return ws.getWarningsSpatial(myQuery)



# @router.post("/debug/", status_code=200)
# async def debug_query(query: Request):
#     """
#     Echos the query data.
#     """
#     myQuery = await query.json()
#     return ws.debug(myQuery)

