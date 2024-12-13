from typing import List

from fastapi import FastAPI, HTTPException

from .models import Address, Location
from .services import FindMyItem

app = FastAPI(title="Find My Items API")
findmy = FindMyItem()


@app.get("/items", response_model=List[str])
async def get_items():
    """Get all items"""
    return findmy.get_system_items()


@app.get("/items/{item_name}/location", response_model=Location)
async def get_item_location(item_name: str):
    """Get the location of a specific item"""
    try:
        return findmy.get_location(item_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/items/{item_name}/address", response_model=Address)
async def get_item_address(item_name: str):
    """Get the address of a specific item"""
    try:
        return findmy.get_address(item_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
