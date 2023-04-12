# Quickstart

Refer to the `Setup > settings.yaml` section of this README then run the following:

```
make setup
make
```

Naviate to http://localhost:8000/

# Setup
Start the containers.

```
docker-compose -f docker-compose/docker-compose.yml up -d
```

Install all dependencies.

```
pip install pipenv
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --python $(which python)
```

## settings.yaml
Create a `settings.yaml` file in the root directory with the following variables:

```
# Keycloak
keycloak_server_url: http://localhost:8080/auth/
keycloak_realm: ztp
keycloak_client_id: ztp-client
keycloak_client_secret: BJ8BFHBhs90zbwfgKW705QOOxsxAc4lx

# Postgres
postgres_host: localhost
postgres_port: 5432
postgres_database: postgres
postgres_user: postgres
postgres_password: postgres

# FastAPI
fastapi_secret_key: "super-secret-key"
```

Run the fastapi server

```
uvicorn ztpvis.main:app --host 0.0.0.0 --port 8000 --reload
```

# Pages

Page | Description
---|---
http://localhost:8000/ | Index
http://localhost:8000/hello | User Info
http://localhost:8000/docs | FastAPI Swagger UI
http://localhost:8000/login | SSO Login
http://localhost:8000/logout | SSO Logout
http://localhost:8000/callback | SSO Callback
http://localhost:8000/graphql | GraphQL Explorer

# How to Query

Go to http://localhost:8000/graphql to use the GraphQL explorer.

Show the current user and list all documents the user has access to.

```
query {
  currentUser {
    username
    active
    roles
  }
  documents {
    id
    title
    classification
    createdAt
    portions {
      id
      text
      classification
      createdAt
    }
  }
}
```

## Roles

Role | Attributes
---|---
clearance_top_secret | fouo='true',sap=['sci']
clearance_secret | fouo='true'
clearance_confidential | fouo='true'
clearance_unclassified | fouo='true'

## Users

Username | Password | Role
---|---|---
admin | admin | admin
ts_user | password | clearance_top_secret
s_user | password | clearance_secret
c_user | password | clearance_confidential
u_user | password | clearance_unclassified
anon | password | None

# Database

You can use psql to troubleshoot the database.

```
docker run --rm -it --network gql_default -e "PGSSLMODE=disable" postgres:latest psql -U postgres -h db -p 5432
```

# Deprecated Queries

Get a list of all records

```graphql
query {
  records {
    id
    data
    clearance
  }
}
```

