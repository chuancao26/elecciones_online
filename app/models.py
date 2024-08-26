from .database import Base
from sqlalchemy import Integer, Column, String, ForeignKey

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
    id_persona = Column(Integer, ForeignKey("persona.id", ondelete="CASCADE"), \
                        nullable=True)
class Administrador(Base):
    __tablename__ = "administrador"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_administrador= Column(Integer, ForeignKey("persona.id", ondelete="CASCADE"), \
                        nullable=True)
