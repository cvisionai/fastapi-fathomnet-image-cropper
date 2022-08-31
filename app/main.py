# import the necessary packages
from fastapi import FastAPI
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
from typing import List
import time
import logging
import os
import wget
from urllib.parse import unquote
from fastapi import FastAPI, Request

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

@app.middleware("http")
async def add_cache_header(request: Request, call_next):
    response = await call_next(request)
    # This is a one year cache on the response
    response.headers["Cache-Control"] = "max-age=31536000"
    return response

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
    path_string = f'/static/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.jpeg'
    path_check_string = f'/static-files/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.jpeg'
    if exists(path_check_string):
        logger.info("Requested file exists, skipping crop operation")
    else:
        start_time = time.time()
        img_name = wget.download(unquote(url))
        fetch_time = time.time() - start_time
        img = Image.open(img_name)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        open_time = time.time() - start_time
        img_crop = img.crop((image.x1,image.y1,image.x2,image.y2))
        img_crop.save(path_check_string, quality='web_high') 
        finish_time = time.time() - start_time
        logger.info(f"Image fetch time: {fetch_time}, Image open time: {open_time}, Total process time: {finish_time}")
        os.remove(img_name)

    deployment_url = os.getenv("SERVER_URL") + ':' + os.getenv("SERVER_PORT")
    data = {'url' : deployment_url + path_string} 
    
    return JSONResponse(content=jsonable_encoder(data))

@app.post("/cropper-list/")
def croplist(uuidList: List[ImageCrop]):
    dataList = {}
    for image in uuidList:
        url = images.find_by_uuid(image.uuid).url
        path_string = f'/static/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.jpeg'
        path_check_string = f'/static-files/{image.uuid}_{image.x1}_{image.y1}_{image.x2}_{image.y2}.jpeg'
        if exists(path_check_string):
            logger.info("Requested file exists, skipping crop operation")
        else:
            start_time = time.time()
            img_name = wget.download(unquote(url))
            fetch_time = time.time() - start_time
            img = Image.open(img_name)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            open_time = time.time() - start_time
            img_crop = img.crop((image.x1,image.y1,image.x2,image.y2))
            img_crop.save(path_check_string, quality='web_high') 
            finish_time = time.time() - start_time
            logger.info(f"Image fetch time: {fetch_time}, Image open time: {open_time}, Total process time: {finish_time}")
            
        deployment_url = os.getenv("SERVER_URL") + ':' + os.getenv("SERVER_PORT")
        dataList[image.uuid] = deployment_url + path_string
        
    return JSONResponse(content=jsonable_encoder(dataList))

# for debugging purposes, it's helpful to start the testing
# server (don't use this for production)
if __name__ == "__main__":
    print("* Starting web service...")
    app.run()
