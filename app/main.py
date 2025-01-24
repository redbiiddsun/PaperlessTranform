from typing import Union

from fastapi import FastAPI

from app.auth.routers import auth_router


app = FastAPI()

app.include_router(auth_router.router)


@app.get("/")
async def health_status():
    return {"status": "OK"}
