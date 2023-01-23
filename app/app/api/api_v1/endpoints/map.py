import asyncio
import mimetypes
from typing import Any, Counter, Optional
from urllib import response

# import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.search import ms

# test{
from fastapi import FastAPI, Response
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time
# test}

router = APIRouter()
MAP_SUBREDDITS = ["maps"]

# test{
_INF = float("inf")
graphs = {}
graphs['c'] = Counter('python_request_operations_total','The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds',buckets=(1, 2, 5, 6, 10, _INF))
# test}

@router.get("/")
def greet() -> dict:
    """
    Returns a simple greeting message.
    """
    # test{
    start = time.time()
    graphs['c'].inc()
    time.sleep(0.600)
    end = time.time()
    graphs['h'].observe(end - start)
    # test}

    return {
        "msg": "Welcome to METCAP MAP API at METNO!"
    }

# test{
@router.get("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    # return response(res[0], mimetypes="text/plain")
    # return JSONResponse(content=res)
    # return Response(content=res, media_type="text/plain")
    # return res
# test}


@router.get("/lowres/fylke/{administrativeId}")
async def search_lowres_fylke(administrativeId):
    """
    Returns low resolution GeoJSON of administrative unit.
    """
    return ms.mapSearchLowres(administrativeId, 'fylke')


@router.get("/lowres/fylke/list/")
async def get_lowres_fylke_list():
    """
    Returns list of all low resolution GeoJSON administrative units (Fylker).
    """
    return ms.mapGetLowresList('fylkeList')


@router.get("/lowres/kommune/list/")
async def get_lowres_kommune_list():
    """
    Returns list of all low resolution GeoJSON administrative units (Fylker).
    """
    return ms.mapGetLowresList('kommuneList')


@router.get("/lowres/kommune/{administrativeId}")
async def search_lowres_kommune(administrativeId):
    """
    Returns low resolution GeoJSON of administrative unit.
    """
    return ms.mapSearchLowres(administrativeId, 'kommune')


@router.post("/", status_code=200)
async def search(query: Request):
    """
    Returns map search results as Geojson.
    """
    myQuery = await query.json()
    return ms.mapSearch(myQuery)


@router.post("/short/", status_code=200)
async def search_short(query: Request):
    """
    Returns map search results as a list of administrative names and id's:\n
    [["name 1","id 1"], ["name 2", "id 2"],...] 
    """
    myQuery = await query.json()
    return ms.mapSearchShort(myQuery)


@router.post("/echo/", status_code=200)
async def echo_query(query: Request):
    """
    Echos the query data.
    """
    myQuery = await query.json()
    return myQuery

