from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(models.UsuarioSistema).filter(models.UsuarioSistema.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_pw = get_password_hash(password)
    user = models.UsuarioSistema(email=email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"mensaje": "Usuario creado correctamente"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.UsuarioSistema).filter(models.UsuarioSistema.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"mensaje": f"Bienvenido, {email}"}
