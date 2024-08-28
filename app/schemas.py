from pydantic import BaseModel
from datetime import datetime, time
class EleccionCreate(BaseModel):
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    descripcion: str
class EleccionOut(EleccionCreate):
    id: int

class ListaCreate(BaseModel):
    nombre: str
    id_eleccion: int
    propuesta: str

class ListaOut(ListaCreate):
    id: int

class PersonaCreate(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    usuario: str
    password: str

class PersonaOut(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    usuario: str