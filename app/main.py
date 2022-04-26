# import the necessary packages
from fastapi import FastAPI, File, UploadFile
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

origins = [
    "http://fast.localhost",
    "http://fast.localhost:8080",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.post("/cropper/")
def crop(image: ImageCrop):

    url = images.find_by_uuid(image.uuid)

    if exists(f'/static-files/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.png'):
        pass  
    else:
        img = Image.open(requests.get(url, stream=True).raw)
        img_crop = img.crop((image.x1,image.y1,image.x2,image.y2))
        img_crop.save(f'/static-files/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.png')

    data = {'url' : f'/static-files/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.png'}
    return JSONResponse(content=jsonable_encoder(data))

# for debugging purposes, it's helpful to start the Flask testing
# server (don't use this for production)
if __name__ == "__main__":
    print("* Starting web service...")
    app.run()
