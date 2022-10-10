import asyncio
from typing import Any, Optional

# import httpx
from fastapi import APIRouter, Depends, HTTPException, Query


router = APIRouter()
MISC_SUBREDDITS = ["misc"]


@router.get("/", status_code=200)
def hello() -> Any:
    """
    Say hello
    """
    return {"msg": "Welcome to METCAP at METNO!"}
