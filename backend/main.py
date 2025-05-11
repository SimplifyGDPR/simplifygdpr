from fastapi import FastAPI
from backend.routers import legal, usuarios, departamentos

app = FastAPI()

app.include_router(legal.router)
app.include_router(usuarios.router)
app.include_router(departamentos.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
