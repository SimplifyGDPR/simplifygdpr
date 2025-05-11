from fastapi import FastAPI
from backend.routers import legal, usuarios, departamentos, politicas, auth, panel

app = FastAPI()

app.include_router(legal.router)
app.include_router(usuarios.router)
app.include_router(departamentos.router)
app.include_router(politicas.router)
app.include_router(auth.router)
app.include_router(panel.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
