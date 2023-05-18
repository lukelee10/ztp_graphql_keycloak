# Quickstart

```bash
docker-compose -f docker-compose/docker-compose.yml up -d
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --python $(which python)
pipenv shell
./manage.py makemigrations data_tables users
./manage.py migrate
./manage.py loaddata data/sample_data.json
./manage.py collectstatic --no-input
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
python manage.py makemigrations data_tables users
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
sci1_user | password | TOPSECRET SCI1/NTK1
sci2_user | password | TOPSECRET SCI2/NTK2/NTK4
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
python manage.py dumpdata data_tables users > data/sample_data.json
```

# How to run a query

Running the following query should give you enough information to render a table when pieced together:

```graphql
query MySearchQuery {
  search(searchTerm: "") {
    data
    classification {
      name
    }
    row {
      id
      accessAttributes {
        name
      }
      classification {
        name
      }
    }
    accessAttributes {
      name
    }
    column {
      id
      classification {
        name
      }
      accessAttributes {
        name
      }
      name
    }
  }
}
```

# OPA
policies located at docker-compose/opa/policies get loaded to container

Query for all policies

GET http://localhost:8181/v1/policies

Query for a "policy" under "policy" ID

GET http://localhost:8181/v1/policies/policy

Uploaded a policy under "policy" ID

PUT http://localhost:8181/v1/policies/policy

Query for "allow_login" rule under the "policy" ID returns true if data given meets rule requirements, false if it fails to meet rule, or {} if not found

POST http://localhost:8181/v1/policies/policy/allow_login
