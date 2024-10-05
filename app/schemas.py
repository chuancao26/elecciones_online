from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

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
    eleccion: EleccionCreate

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

class TokenCreated(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    type_user: Optional[str] = None

class CandidatoCreate(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    id_lista: int

class CandidatoOut(BaseModel):
    candidato: CandidatoCreate
    nombre_lista: str

class VotoCreate(BaseModel):
    id_eleccion: int 
    id_lista: int

class CurrentUserData(BaseModel):
    persona: PersonaOut
    type_user: str