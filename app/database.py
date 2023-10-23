from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from .config import settings
"""
 a file for connecting to my database
"""



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@'+\
                          f'{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                            bind=engine
                            )
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()


# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi',
#                         user='postgres', password='password',
#                         cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Datebase connected successfully")

# except Exception as error:
#     print("Error connecting to database")
#     print("Error:", error)
#     time.sleep(2)