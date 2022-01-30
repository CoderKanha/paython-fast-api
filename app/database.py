from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from psycopg2.extras import RealDictCursor
import time
import psycopg2

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


""" To make a connection with Postgres Driver to use Raw SQL Command """
# while True:
#     try:
#         print('Connecting to database...')
#         conn = psycopg2.connect(
#             host='localhost',
#             database="fastapi",
#             user="postgres",
#             password="admin",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print('Connected to database successfully...')
#         break
#     except Exception as error:
#         print('Failed to connect to database...')
#         print('Error: ', error)
#         time.sleep(5)
