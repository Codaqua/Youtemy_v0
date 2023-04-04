from fastapi import FastAPI
from app.env import config

MODE = config("MODE", cast=str, default="defecto")

app = FastAPI()

@app.get("/")
def home_page():
    return {"Hello": "World", "mode": MODE}

