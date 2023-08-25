# Quickstart

First build the container:
```bash
docker build -t ztp-browser:latest .
```

Here is a docker command to get the container up and running quickly.

```bash
docker run --rm -it --name ztp-browser \
    -e DOMAIN_NAME=ztp.dev \
    -e KEYCLOAK_HOST=http://keycloak.ztp.dev \
    -e KEYCLOAK_CLIENT_SECRET=BJ8BFHBhs90zbwfgKW705QOOxsxAc4lx \
    -e KEYCLOAK_REALM=ztp \
    -e KEYCLOAK_CLIENT_ID=ztp-browser \
    -p 8000:8000 \
    ztp-browser:latest
```

or if everything is running on localhost.
```bash
docker run --rm -it --name ztp-browser \
    -e DOMAIN_NAME=localhost \
    -e KEYCLOAK_HOST=http://localhost:8080 \
    -e KEYCLOAK_CLIENT_SECRET=BJ8BFHBhs90zbwfgKW705QOOxsxAc4lx \
    -p 8000:8000 \
    ztp-browser:latest
```
