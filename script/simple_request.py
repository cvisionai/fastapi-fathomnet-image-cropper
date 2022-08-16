# USAGE
# python simple_request.py

# import the necessary packages
import requests

# initialize the REST API endpoint URL along with the input
# image path

REST_API_URL = "https://your_domain_for_the_server/cropper/"
# Example UUID of image in fathomnet
UUID = "939cec0f-882f-499c-b538-1c56c6c5e9ff"

data = {
    "uuid": UUID,
    "x1": 100,
    "y1": 100,
    "x2": 405,
    "y2": 400
}

r = requests.post(REST_API_URL, json=data)

# ensure the request was sucessful
print(r.json())
