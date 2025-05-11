from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models
from datetime import date
from typing import Optional

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios autorizados"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crear_usuario(nombre: str, cargo: str, ubicacion: str, db: Session = Depends(get_db)):
    usuario = models.UsuarioAutorizado(
        nombre=nombre,
        cargo=cargo,
        ubicacion=ubicacion
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.get("/")
def listar_usuarios(activos: Optional[bool] = True, db: Session = Depends(get_db)):
    query = db.query(models.UsuarioAutorizado)
    if activos:
        query = query.filter(models.UsuarioAutorizado.fecha_baja == None)
    return query.all()

@router.put("/{usuario_id}/baja")
def dar_de_baja(usuario_id: int, fecha: Optional[date] = date.today(), db: Session = Depends(get_db)):
    usuario = db.query(models.UsuarioAutorizado).filter(models.UsuarioAutorizado.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.fecha_baja = fecha
    db.commit()
    return {"mensaje": f"Usuario {usuario.nombre} dado de baja el {fecha}"}
