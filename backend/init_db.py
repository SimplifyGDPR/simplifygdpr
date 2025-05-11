from backend.database import engine
from backend.models import Base

# Este script se ejecuta una sola vez para crear la base de datos
print("Creando base de datos...")
Base.metadata.create_all(bind=engine)
print("Base de datos creada.")
