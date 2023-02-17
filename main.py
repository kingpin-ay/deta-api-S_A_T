from fastapi import FastAPI
from deta import Deta
from model import Feedback
from model import UserData
from DetaDesign.usercreation import User
import hashlib
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# loding the enviorment file
load_dotenv()
APP_KEY = os.getenv('APP_KEY')
KEY_GEN_CODE = os.getenv('KEY_GEN_CODE')

# Initialize with a Project Key
deta = Deta(APP_KEY)

# This how to connect to or create a database.
feedbacks_db = deta.Base("feedbacks_db")
user_db = deta.Base("user_db")

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
    return {"data": "Pong"}


@app.get('/ping')
def pingPage():
    return {"data": "Pong"}


@app.post("/send-feedback")
def recieveFeedBack(feedback: Feedback):
    item_dict = feedback.dict()
    dhash = hashlib.md5()
    current_time = str(datetime.now())
    try:
        encoded = json.dumps(item_dict, sort_keys=True).encode()
        dhash.update(encoded)
        item_dict["hash"] = dhash.hexdigest()
        item_dict["datetime"] = current_time
        result = feedbacks_db.put(item_dict)
        return {"code": result}
    except Exception as e:
        return {"code": 532, "value": e}


@app.post("/user-generation")
def user_data_recieve(userdata: UserData):
    if(user_db.get(key=userdata.username) != None):
        return {"code" : 301 , "value" : "username exists Please select another username"}
    user = User(username=userdata.username,
                password=userdata.password,
                creation_time=str(datetime.now()),
                private_key_gen_code=KEY_GEN_CODE)
    try:
        user_db.put(user.get_dictionary_data() ,
                    key=user.get_username())
        return {"code" : 200 , "value" : f"succesfully created user {userdata.username}"}
    except Exception as e:
        return {"code": 602 , "value" : e}
    
    
@app.post("/log-in")
def auth_log_in(userdata : UserData):
    result = user_db.get(key=userdata.username)
    if(result != None):
        if (result["password"] != userdata.password):
            return {"code" : 401 , "value" : "wrong password"}
        return {"code": 200 , "value" : "successfully logged in" , "address_code" : result["address_code"]}
    return {"code": 402 , "value" : "user does not exists"}