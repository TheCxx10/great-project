from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_price": item.price, "item_id": item_id}

@app.get("/pythagorean")
def pythagorean(a: int | None = None, b: int | None = None, c:int | None = None):
    if a and b:
        return {"result": (a**2 + b**2)**0.5}
    elif a and c:
        return {"result": (c**2 - a**2)**0.5}
    elif b and c:
        return {"result": (c**2 - b**2)**0.5}
    raise HTTPException(status_code=400, detail="Invalid input")

