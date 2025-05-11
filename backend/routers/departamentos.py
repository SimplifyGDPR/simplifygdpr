from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models

router = APIRouter(
    prefix="/departamentos",
    tags=["Departamentos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crear_departamento(nombre: str, db: Session = Depends(get_db)):
    departamento = models.Departamento(nombre=nombre)
    db.add(departamento)
    db.commit()
    db.refresh(departamento)
    return departamento

@router.get("/")
def listar_departamentos(db: Session = Depends(get_db)):
    return db.query(models.Departamento).all()
