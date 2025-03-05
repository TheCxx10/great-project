from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
print("Hello world")

db = {}
pythagorean_cache = {}


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if dict.get(db, item_id) is not None:
        return db[item_id]
    else:
        return "In the database with the key "+str(item_id)+", nothing was found"


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    db[item_id] = item
    return {"item_price": item.price, "item_id": item_id}

@app.get("/pythagorean")
def pythagorean(a: int | None = None, b: int | None = None, c:int | None = None):
    # cache

    key = (a and ("a="+str(a)) or "") + (b and ("b="+str(b)) or "") + (c and ("c="+str(c)) or "")
    
    if key in pythagorean_cache:
        #cache time hehe
        return pythagorean_cache[key], "this was in a cache!"

    if a and b:
        # add to cache
        pythagorean_cache[key] = (a**2 + b**2)**0.5
        return {"result": (a**2 + b**2)**0.5}
    elif a and c:
        pythagorean_cache[key] = (c**2 - a**2)**0.5
        return {"result": (c**2 - a**2)**0.5}
    elif b and c:
        pythagorean_cache[key] = (c**2 - b**2)**0.5
        return {"result": (c**2 - b**2)**0.5}
    raise HTTPException(status_code=400, detail="Invalid input")