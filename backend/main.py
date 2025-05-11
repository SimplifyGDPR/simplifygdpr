from fastapi import FastAPI
from backend.routers import legal, usuarios, departamentos, politicas, auth

app = FastAPI()

app.include_router(legal.router)
app.include_router(usuarios.router)
app.include_router(departamentos.router)
app.include_router(politicas.router)
app.include_router(auth.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
