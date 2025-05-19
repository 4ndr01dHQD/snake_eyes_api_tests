from decouple import config
from sqlalchemy import create_engine, URL

API_HOST = config('API_HOST')
API_PORT = config('API_PORT')

DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_NAME = config('DB_NAME')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')


connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
)
engine = create_engine(connection_url, pool_pre_ping=True)