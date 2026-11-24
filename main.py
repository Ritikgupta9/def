from typing import Annotated

from fastapi import FastAPI, status
from pydantic import BaseModel, Field, StringConstraints


class ItemCreate(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    quantity: Annotated[int, Field(strict=True, gt=0)]


class Item(ItemCreate):
    id: int


app = FastAPI(title="Inventory API")
items: list[Item] = []


@app.get("/items", response_model=list[Item])
async def list_items() -> list[Item]:
    return items.copy()


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate) -> Item:
    created = Item(id=len(items) + 1, name=item.name, quantity=item.quantity)
    items.append(created)
    return created
