from pydantic import BaseModel
from datetime import datetime, time
class EleccionCreate(BaseModel):
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    descripcion: str
class EleccionOut(EleccionCreate):
    id: int
