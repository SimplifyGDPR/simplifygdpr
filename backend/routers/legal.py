from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models

router = APIRouter(
    prefix="/clausula",
    tags=["Cláusulas legales"]
)

# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crear_clausula(tipo: str, contenido: str, db: Session = Depends(get_db)):
    clausula = models.Clausula(tipo=tipo, contenido=contenido)
    db.add(clausula)
    db.commit()
    db.refresh(clausula)
    return clausula

@router.get("/")
def listar_clausulas(db: Session = Depends(get_db)):
    return db.query(models.Clausula).all()
