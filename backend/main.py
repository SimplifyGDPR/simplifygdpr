from fastapi import FastAPI
from backend.routers import legal

app = FastAPI()

app.include_router(legal.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
