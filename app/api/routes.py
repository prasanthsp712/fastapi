from fastapi import APIRouter, HTTPException
from app.models.item import Item
from app.core.database import db
from typing import List

router = APIRouter()

@router.get("/items", response_model=List[Item])
async def get_items():
    return db.get_all_items()

@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = db.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items", response_model=Item)
async def create_item(item: Item):
    return db.add_item(item)
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@router.post("/items")
async def create_item(item: Item):
    return {
        "message": "Item created successfully",
        "data": item
    }

@router.get("/items")
async def get_items():
    return [
        {"name": "Laptop", "price": 75000, "in_stock": True}
    ]