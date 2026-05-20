#colocar python -m pip install python-dotenv no readme
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["Aposta"]

cavalos_collection = db["Cavalos"]
corridas_collection = db["Corridas"]
pistas_collection = db["Pistas"]