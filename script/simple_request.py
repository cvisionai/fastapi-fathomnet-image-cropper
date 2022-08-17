# USAGE
# python simple_request.py

# import the necessary packages
import requests

# initialize the REST API endpoint URL along with the input
# image path

REST_API_URL = "https://adamant.tator.io:8092/cropper/"
# Example UUID of image in fathomnet
UUID = "f11816b8-8adb-41b3-8a2b-0ef976d8af29"

data = {
    "uuid": UUID,
    "x1": 100,
    "y1": 100,
    "x2": 405,
    "y2": 302
}

r = requests.post(REST_API_URL, json=data)

# ensure the request was sucessful
print(r.json())
