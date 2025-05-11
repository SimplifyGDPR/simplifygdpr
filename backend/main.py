from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from backend.routers import legal, usuarios, departamentos, politicas, auth, panel

app = FastAPI()

# 🔗 Incluimos los routers de tu app
app.include_router(legal.router)
app.include_router(usuarios.router)
app.include_router(departamentos.router)
app.include_router(politicas.router)
app.include_router(auth.router)
app.include_router(panel.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}

# ✅ Swagger: configuración para que muestre el botón "Authorize"
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="SimplifyGDPR API",
        version="1.0.0",
        description="API para gestión automatizada del cumplimiento RGPD",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login"
                }
            }
        }
    }

    openapi_schema["security"] = [
        {
            "OAuth2PasswordBearer": []
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
