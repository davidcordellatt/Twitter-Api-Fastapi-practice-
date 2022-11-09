#FastAPI
from fastapi import FastAPI

app = FastAPI()

@app.get(
    path="/"
    )
def home():
    return {"Twitter API" : "All the proccess are working" }