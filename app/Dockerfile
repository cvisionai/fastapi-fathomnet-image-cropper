FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip3 install Pillow numpy python-multipart requests aiofiles fathomnet wget

RUN mkdir -p /app/app
COPY . /app/app
