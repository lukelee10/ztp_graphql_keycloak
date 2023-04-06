"""This class is used to connect to the database and perform queries."""

from psycopg2.pool import SimpleConnectionPool

from ztpvis import settings

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=settings.postgres_host,
    port=settings.postgres_port,
    database=settings.postgres_database,
    user=settings.postgres_user,
    password=settings.postgres_password,
)
