from fastapi import FastAPI, HTTPException, APIRouter
from openai import OpenAI
import os
import asyncio
from dotenv import load_dotenv
from api1 import *
from api2 import *
from api3 import *
from api4 import *
from api5 import *
from api6 import *
from api7 import *
from api8 import *
from api9 import *
from api10 import *

load_dotenv()
app = FastAPI()
router = APIRouter()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("Missing OpenAI API key. Set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=openai_api_key)

api1 = Api1(client, router)
api2 = Api2(client, router)
api3 = Api3(client, router)
api4 = Api4(client, router)
api5 = Api5(client, router)
api6 = Api6(client, router)
api7 = Api7(client, router)
api8 = Api8(client, router)
api9 = Api9(client, router)
api10 = Api10(client, router)

app.include_router(router)
 
#start server from /core with below
#python -m uvicorn main:app --reload

