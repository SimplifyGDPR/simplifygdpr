from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

class Responsable(Base):
    __tablename__ = "responsables"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cargo = Column(String)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))

    departamento = relationship("Departamento")

class Clausula(Base):
    __tablename__ = "clausulas"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    contenido = Column(String)

class UsuarioAutorizado(Base):
    __tablename__ = "usuarios_autorizados"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cargo = Column(String)
    ubicacion = Column(String)
    fecha_baja = Column(Date, nullable=True)

class Politica(Base):
    __tablename__ = "politicas"

    class UsuarioSistema(Base):
    __tablename__ = "usuarios_sistema"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Ej: Aviso Legal, Cookies...
    contenido = Column(String, nullable=False)

