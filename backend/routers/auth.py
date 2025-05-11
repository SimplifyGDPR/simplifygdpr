from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

# 🔐 Seguridad
SECRET_KEY = "clave-secreta-simplifygdpr"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔐 Ruta para registrarse
from pydantic import BaseModel
class UserInput(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(user: UserInput, db: Session = Depends(get_db)):
    existing_user = db.query(models.UsuarioSistema).filter(models.UsuarioSistema.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_pw = get_password_hash(user.password)
    new_user = models.UsuarioSistema(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"mensaje": "Usuario creado correctamente"}

# ✅ Login con formulario tipo OAuth2 (compatible Swagger UI)
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.UsuarioSistema).filter(models.UsuarioSistema.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
