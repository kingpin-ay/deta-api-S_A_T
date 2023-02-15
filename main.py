from fastapi import FastAPI
from deta import Deta
from model import Feedback
import hashlib
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# loding the enviorment file
load_dotenv()
APP_KEY = os.getenv('APP_KEY')


# Initialize with a Project Key
deta = Deta(APP_KEY)


# This how to connect to or create a database.
feedbacks_db = deta.Base("feedbacks_db")




app = FastAPI()


# adding cors for the Cross origin resourse sharing 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"data" : "Pong"}

@app.get('/ping')
def pingPage():
    return {"data" : "Pong"}


@app.post("/send-feedback")
async def recieveFeedBack(feedback : Feedback):
    item_dict = feedback.dict()
    dhash = hashlib.md5()
    try:
        encoded = json.dumps(item_dict, sort_keys=True).encode()
        await dhash.update(encoded)
        item_dict["hash"] = dhash.hexdigest() 
        await feedbacks_db.put(item_dict)
        return {"code" : 200}
    except:
        return{"code" : 532 , "value" : "data is not accepted by the deta base"}