from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from backend.database import SessionLocal
from sqlalchemy.orm import Session

SECRET_KEY = "clave-secreta-simplifygdpr"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/panel",
    tags=["Panel"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/")
def acceso_panel(usuario: str = Depends(get_current_user)):
    return {"mensaje": f"Bienvenido al panel, {usuario}"}
