from fastapi import FastAPI

from app.database import create_db_and_tables
from app.auth import auth_router


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)

@app.get("/")
async def welcome():
    return "Welcome to the Data Type Analyzer API! Please use /docs for API documentation."

@app.get("/health")
async def health_status():
    return {"status": "OK"}