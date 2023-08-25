# Quickstart

Here is a docker command to get the container up and running quickly.

```bash
# Generate a secret key
export DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

docker run --rm -it --name ztp-browser \
    -e DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
    -e DJANGO_SETTINGS_MODULE=ztp_browser.settings.production \
    -e DOMAIN_NAME=ztp.dev \
    -e DB_NAME=postgres \
    -e DB_USER=postgres \
    -e DB_PASSWORD=postgres \
    -e DB_HOST=postgres.internal \
    -e KEYCLOAK_HOST=https://keycloak.ztp.dev \
    -e KEYCLOAK_CLIENT_SECRET=BJ8BFHBhs90zbwfgKW705QOOxsxAc4lx \
    -p 80:8000 \
    ztp-browser:latest
```

# Getting Started

Set the following environment variable to use production mode settings.

```sh
DJANGO_SETTINGS_MODULE=ztp_browser.settings.production
```

A unique secret key needs to be generated and set via an environment variable. Generate a key with the following command:

```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Set the following environment variable to the generated secret key.

```sh
DJANGO_SECRET_KEY=generated_secret_key
```

The domain name of the site needs to be set.

```sh
DOMAIN_NAME=ztp.dev
```

The following environment variables need to be set to the postgres connection information.

```sh
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

The following environment variables need to be set to the Keycloak connection information.

```sh
KEYCLOAK_HOST
KEYCLOAK_REALM
KEYCLOAK_CLIENT_ID
KEYCLOAK_CLIENT_SECRET
```
