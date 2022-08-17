
Launch on localhost using docker-compose:
```bash
cd fastapi-fathomnet-image-cropper
docker network create traefik-public
docker-compose up --build
```
You can scale services to be able to handle more requests by using --scale fast=M. Experimentally you want a few web servers to handle multiple concurrent requests or larger requests. 

Browser Windows:
- http://localhost:8080/dashboard
- http://localhost:8092/static/index.html

Test curl commands:
```bash
curl -k http://localhost:8082/

cd images
time curl -X POST 'https://your_domain.com:port_number/cropper/' -H 'Content-Type: application/json' -d '{"uuid": "f11816b8-8adb-41b3-8a2b-0ef976d8af29","x1": "100", "y1": "100", "x2": "405", "y2": "400"}
```

Test simple-request.py
```bash
docker exec -it fast bash
cd /script/
python3 simple_request.py
```

TODO

- Add aspect ratio preserving capability
- Add health checks. Consider https://pypi.org/project/fastapi-health/
