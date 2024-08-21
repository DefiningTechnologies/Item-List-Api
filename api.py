from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define data models
class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float

class CreateItem(BaseModel):
    name: str
    description: str
    price: float

# Sample data
items = [
    Item(id=1, name="Item 1", description="Description 1", price=9.99),
    Item(id=2, name="Item 2", description="Description 2", price=14.99),
    Item(id=3, name="Item 3", description="Description 3", price=19.99),
]

# Endpoints
@app.get("/items/", response_model=List[Item])
def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
):
    """
    Retrieve a list of items.
    - **skip**: Number of items to skip (for pagination).
    - **limit**: Maximum number of items to return.
    - **name**: Filter items by name (optional).
    """
    filtered_items = items
    if name:
        filtered_items = [item for item in items if name.lower() in item.name.lower()]
    return filtered_items[skip:skip+limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int = Path(..., gt=0)):
    """
    Retrieve an item by its ID.
    - **item_id**: ID of the item to retrieve.
    """
    try:
        return next(item for item in items if item.id == item_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: CreateItem):
    """
    Create a new item.
    """
    new_id = max(item.id for item in items) + 1 if items else 1
    new_item = Item(id=new_id, **item.dict())
    items.append(new_item)
    return new_item