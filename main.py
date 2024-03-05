from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define pydantic model for the item
class Item(BaseModel):
    id : int
    name : str
    description : str
    price : int
    quantity : int

#Storage for item and item_id
item_db = []
next_item_id = 1

#create Item
@app.post("/items",response_model=Item)
async def create_item(item : Item):
   global next_item_id
   new_item_id = next_item_id
   next_item_id += 1

   item_dict = item.dict(exclude_unset=True)
   item_dict["id"] = new_item_id
   item_db.append(item_dict)
   print(item_db)
   return item

#route to get all items
@app.get("/items",response_model=List[Item])
async def read_items():
    return item_db

#route to get a specific item by ID
@app.get("/items/{item_id}",response_model=Item)
async def read_item(item_id : int):
    for item in item_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404,detail = "Item not found!!")

#update item based on ID
@app.put("/items/{item_id}")
async def update_item(item_id : int, update_item : Item):
    for index, item in enumerate(item_db):
        if item["id"] == item_id:
            item_db[index] = update_item.dict(exclude_unset=True)
            item_db[index]["id"] = item_id
            return item_db[index]
    raise HTTPException(status_code=404,detail = " Item not Found!!")

#Delete item based on Id
@app.delete("/items/{item_id}")
async def deleted_item(item_id : int, deleted_item : Item):
    for index,item in enumerate(item_db):
        if item['id'] == item_id:
            deleted_item = item_db.pop(index)
            return deleted_item
        
    raise HTTPException(status_code=404,detail="Item not found!!")
