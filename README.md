
This project is a simple server that accepts POSTs with Fathomnet UUIDs and a crop region, generates those crops, and hosts the resulting images. A simple hash function that takes the image UUID, and adds the dimensions of the crops is used to determine if an image exists in the cache or not, to prevent extra downloads and crops. The server responds to a POST with the URL of the cropped image.

Some important notes for getting started. You will need a .env with the appropriate values filled in, corresponding to your host domain, host url, and host port, as well as the location of your traefik configuration folder, which you will need to have if you wish to use HTTPS. Some helpful hints about that folder. You will want to have three files, certificates.toml, fullchain.pem, privkey.pem (you don't need to keep the fullchain or privkey naming convention, but you need them to be consistent in the certificates.toml file). The certificates.toml file will contain

```
[[tls.certificates]] #first certificate
    certFile = "/configuration/files/fullchain.pem" # managed by Certbot
    keyFile = "/configuration/files/privkey.pem" # managed by Certbot
```

The permissions for these files should be
* certificates.toml - 664
* fullchain.pem - 600
* privkey.pem - 600

Not setting these files up correctly will result in much heartburn in using TLS.

Launch on localhost using docker-compose:
```bash
cd fastapi-fathomnet-image-cropper
docker network create traefik-public
docker-compose up --build
```
You can scale services to be able to handle more requests by using --scale fast=M. Experimentally you want a few web servers to handle multiple concurrent requests or larger requests. 

Browser Windows:
- http://localhost:8080/dashboard

Currently there is no front end for the API, but a test one could be made if one were inclined to contribute.

Test curl command:
```bash
time curl -X POST 'https://your_domain.com:port_number/cropper/' -H 'Content-Type: application/json' -d '{"uuid": "f11816b8-8adb-41b3-8a2b-0ef976d8af29","x1": "100", "y1": "100", "x2": "405", "y2": "400"}
```

Test simple-request.py
```bash
docker exec -it fast bash
cd /script/
python3 simple_request.py
```

TODO

- Add health checks. Consider https://pypi.org/project/fastapi-health/
