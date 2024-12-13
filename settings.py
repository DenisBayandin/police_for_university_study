import psycopg2
from decouple import config

db_connection = psycopg2.connect(
    dbname=config("DBNAME", cast=str),
    user=config("DBUSER", cast=str),
    password=config("DBPASSWORD", cast=str),
    host=config("DBHOST", cast=str, default="localhost"),
    port=config("DBPORT", cast=int, default=5432)
)
