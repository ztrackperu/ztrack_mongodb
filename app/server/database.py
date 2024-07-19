import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#DB_URL = DB_URL = os.getenv("DB_URL")
DB_URL = config("DB_URL")
engine = create_engine(DB_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()


MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
#integrado es nombre para la base de datos
#DATA_BASE = config("DATA_BASE")
#database = client.DATA_BASE
#print(DATA_BASE)
#database = client.intranet


#def collection(data):
    #student_collection = database.get_collection("students_collection")
    #student_collection = database.get_collection(data)
    #return student_collection

