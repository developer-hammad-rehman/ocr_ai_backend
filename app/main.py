from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import api
from app.crud import create_table
from fastapi.middleware.cors import CORSMiddleware


#=====================================================================#

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating Table....")
    create_table()
    yield

#========================================================================#


app = FastAPI(title="OCR_AI" ,lifespan=lifespan)

#========================================================================#

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#========================================================================#

@app.get('/' , tags=["Root Route"])
def root_route():
    return {"message" : "Welcome to ocr app server"}

#==========================================================================#

app.include_router(api.router)

#===========================================================================#