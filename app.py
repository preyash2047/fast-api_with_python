from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from pydantic import BaseModel
import secrets

from explore_dataset.init import DATA

app = FastAPI()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "appy")
    correct_password = secrets.compare_digest(credentials.password, "appy")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Infigon Industrial API : ERROR : Auth Failed",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def read_root():
    return "Tiger Enterprises Web API v1.0"

#aws.ip
@app.get("/aws-ip")
def read_root():
    return {"aws-ip":"10.11.12.13"}

#container.ip
@app.get("/container-ip")
def read_root():
    return {"container-ip":"127.16.10.11"}


#container-hostname
@app.get("/container-hostname")
def read_root():
    return {"container-hostname":"ContainerXYZ"}

#all
@app.get("/all")
def read_root():
    return {"aws-ip":"10.11.12.13",
            "container-ip": "127.16.10.11",
            "container-hostname": "ContainerXYZ"
            }


#sample code for hosting other data
#to host specify the data inside the init.py file DATA dictionery
@app.get("/explore/data/{field}" )
def get_field_info(field:str,username: str = Depends(get_current_username)):
    return DATA[field]

@app.get("/explore/clg/{field}/{clgName}",)
def get_field_info(field:str,clgName:str,username: str = Depends(get_current_username)):
    return DATA[field][clgName]


@app.get("/explore/clg/{field}/{clgName}/{infoType}")
def get_field_info(field:str,clgName:str,infoType:str,username: str = Depends(get_current_username)):
    return DATA[field][clgName][infoType]
