from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models

router = APIRouter(
    prefix="/politicas",
    tags=["Políticas"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crear_politica(titulo: str, tipo: str, contenido: str, db: Session = Depends(get_db)):
    politica = models.Politica(titulo=titulo, tipo=tipo, contenido=contenido)
    db.add(politica)
    db.commit()
    db.refresh(politica)
    return politica

@router.get("/")
def listar_politicas(db: Session = Depends(get_db)):
    return db.query(models.Politica).all()
