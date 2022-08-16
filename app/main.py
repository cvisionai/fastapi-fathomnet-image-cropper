# import the necessary packages
from fastapi import FastAPI, Request, Response, Body, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from PIL import Image
from pydantic import BaseModel
from fathomnet.api import images
from os.path import exists
import requests
import numpy as np
import app.settings as settings
import app.helpers as helpers
import redis
import uuid
import time
import json
import io
import logging

logging.basicConfig(
    handlers=[logging.StreamHandler()],
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class ImageCrop(BaseModel):
    uuid: str
    x1 : int
    y1 : int
    x2 : int
    y2: int
    
class ImageCropList(BaseModel):
    uuidList: list

app.mount("/static", StaticFiles(directory="/static-files"), name="static")

@app.get("/")
async def homepage():
    return FileResponse('/static-files/index.html')

@app.post("/cropper/")
def crop(image: ImageCrop):

    url = images.find_by_uuid(image.uuid).url
    path_string = f'/static/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.png'
    path_check_string = f'/static-files/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.png'
    if exists(path_check_string):
        logger.info("Requested file exists, skipping crop operation")
    else:
        img = Image.open(requests.get(url, stream=True).raw)
        img_crop = img.crop((image.x1,image.y1,image.x2,image.y2))
        img_crop.save(path_check_string) 

    deployment_url = 'https://adamant.tator.io:8092'
    data = {'url' : deployment_url + path_string} 
    
    return JSONResponse(content=jsonable_encoder(data))

@app.post("/cropper-list/")
def croplist(uuidList: ImageCropList):
    dataList = {}
    for image in uuidList:
        url = images.find_by_uuid(image.uuid).url
        path_string = f'/static/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.png'
        path_check_string = f'/static-files/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.png'
        if exists(path_check_string):
            logger.info("Requested file exists, skipping crop operation")
        else:
            img = Image.open(requests.get(url, stream=True).raw)
            img_crop = img.crop((image.x1,image.y1,image.x2,image.y2))
            img_crop.save(path_string) 

        deployment_url = 'https://adamant.tator.io:8092'
        dataList[image.uuid] = deployment_url + path_string
        
    return JSONResponse(content=jsonable_encoder(dataList))

# for debugging purposes, it's helpful to start the Flask testing
# server (don't use this for production)
if __name__ == "__main__":
    print("* Starting web service...")
    app.run()
