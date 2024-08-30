from app.database import Base
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Time

class Persona(Base):
    __tablename__= "persona"
    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True)
    nombres = Column(String, nullable = False)
    apellido_paterno = Column(String, nullable = False)
    apellido_materno = Column(String, nullable = False)
    usuario = Column(String, unique = True, nullable = True)
    password = Column(String, nullable=False)

class Elector(Base):
    __tablename__ = "elector"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_persona = Column(Integer, ForeignKey("persona.id", ondelete="CASCADE"), nullable=True)

class Administrador(Base):
    __tablename__ = "administrador"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_persona = Column(Integer, ForeignKey("persona.id", ondelete="CASCADE"), nullable=True)

class Eleccion(Base):
    __tablename__ = "eleccion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(TIMESTAMP(timezone=True), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    descripcion = Column(String, nullable=False, server_default="")

class Lista(Base):
    __tablename__ = "lista"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    id_eleccion = Column(Integer, ForeignKey("eleccion.id", ondelete="CASCADE"), nullable=False)
    propuesta = Column(String, nullable=False, server_default="")

class Candidato(Base):
    __tablename__ = "candidato"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String, nullable = False)
    apellido_paterno = Column(String, nullable = False)
    apellido_materno = Column(String, nullable = False)
    id_lista = Column(ForeignKey("lista.id", ondelete="CASCADE"), nullable=False)
