# import the necessary packages
from fastapi import FastAPI, Body, File, UploadFile
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

'''
origins = [
    "http://fast.localhost",
    "http://fast.localhost:8080",
    "http://localhost",
    "http://localhost:8080",
]
'''

origins = ["*"]

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
    y2 : int

app.mount("/static", StaticFiles(directory="/static-files"), name="static")

@app.get("/")
async def homepage():
    return FileResponse('/static-files/index.html')

@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = origins
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response

@app.post("/cropper/")
def crop(image: str = Body(...)):

    image= json.loads(image)
    url = images.find_by_uuid(image.get('uuid')).url

    if exists(f'/static-files/{image.get("uuid")}_{image.get("x1")}_{image.get("y1")}_{image.get("x2")}_{image.get("y2")}.png'):
        pass  
    else:
        img = Image.open(requests.get(url, stream=True).raw)
        img_crop = img.crop((image.x1,image.y1,image.x2,image.y2))
        img_crop.save(f'/static-files/{image.get("uuid")}_{image.get("x1")}_{image.get("y1")}_{image.get("x2")}_{image.get("y2")}.png') 

    data = {'url' : f'/static-files/{image.get("uuid")}_{image.get("x1")}_{image.get("y1")}_{image.get("x2")}_{image.get("y2")}.png'}
    '''
    headers = {"Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
            "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"}
    '''
    return JSONResponse(content=jsonable_encoder(data), headers=headers)

# for debugging purposes, it's helpful to start the Flask testing
# server (don't use this for production)
if __name__ == "__main__":
    print("* Starting web service...")
    app.run()
