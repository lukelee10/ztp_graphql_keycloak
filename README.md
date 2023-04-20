# Quickstart

```bash
docker-compose -f docker-compose/docker-compose.yml up -d
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --python $(which python)
pipenv shell
./manage.py makemigrations documents users
./manage.py migrate
./manage.py loaddata data/sample_data.json
./manage.py collectstatic
./manage.py runserver
```

# Getting Started

Start the postgres and keycloak container services:

```bash
docker-compose -f docker-compose/docker-compose.yml up -d
```

Install all dependencies with pipenv:

```bash
pip install pipenv
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --python $(which python)
```

Activate your virtual environment:

```bash
pipenv shell
```

Create and run the migrations:

```bash
python manage.py makemigrations documents users
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Setup static files:

```bash
python manage.py collectstatic
```

Run the server:

```bash
python manage.py runserver
```

# URLS

Page | Description
---|---
http://localhost:8000/ | Home Page
http://localhost:8000/login | SSO Login
http://localhost:8000/logout | SSO Logout
http://localhost:8000/graphql | GraphQL API
http://localhost:8000/graphql | Django Admin

# Users

Username | Password | Clearance
---|---|---
admin* | admin | TOPSECRET
ts_user | password | TOPSECRET
s_user | password | SECRET
c_user | password | CONFIDENTIAL
u_user | password | UNCLASSIFIED
anon | password | None

*\*admin user is not in the ztp realm of Keycloak. You can login via /admin*

# Loading Sample Data

To load sample data into the database, run the following command:

```bash
python manage.py loaddata data/sample_data.json
```

To export the data from the database, run the following command:

```bash
python manage.py dumpdata documents users > data/sample_data.json
```