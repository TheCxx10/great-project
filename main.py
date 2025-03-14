from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from time import sleep as wait
import threading


app = FastAPI()

db = {}
pythagorean_cache = dict()

cacheTimer = 10


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class pytCache(BaseModel):
    answer: float
    timer: int


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
        return pythagorean_cache[key].answer, "this was in a cache!"

    if a and b:
        # add to cache
        answer: float = (a**2 + b**2)**0.5 
        pythagorean_cache[key] = pytCache(answer=answer, timer=cacheTimer)
        return {"result": answer}
    elif a and c:
        answer : float = (c**2 - a**2)**0.5
        pythagorean_cache[key] = pytCache(answer=answer, timer=cacheTimer)
        return {"result": answer}
    elif b and c:
        answer : float = (c**2 - b**2)**0.5
        pythagorean_cache[key] = pytCache(answer= answer, timer=cacheTimer)
        return {"result": answer}
    raise HTTPException(status_code=400, detail="Invalid input")

def cache_cleaner():
    while True:
        wait(1)
        # runs every second to decrease the cachetimer and remove the old posts
        for key in list(pythagorean_cache.keys()):
            pythagorean_cache[key].timer -= 1
            if pythagorean_cache[key].timer <= 0:
                # remove cache
                print(f"Removed cache {key}, {pythagorean_cache[key].answer}")
                pythagorean_cache.pop(key)

# Start the cache cleaner in a new thread
threading.Thread(target=cache_cleaner, daemon=False).start()
