from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.utils import hash_password, verify_password
from typing import List

from app import schemas, models

router = APIRouter(
    tags=["elector"],
    prefix="/elector"
)
def create_persona(new_persona: models.Persona, db: Session = Depends(get_db)):
    db.add(new_persona)
    db.commit()
    db.refresh(new_persona)

@router.get("/", response_model=List[schemas.PersonaOut])
def get_persona(db: Session = Depends(get_db)):
    personas = db.query(models.Persona).all()
    return personas
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PersonaOut)
def create_elector(elector: schemas.PersonaCreate, db: Session = Depends(get_db)):
    persona = db.query(models.Persona).filter(models.Persona.usuario == elector.usuario).first()
    if persona:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Elector ya existe")
    elector.password = hash_password(elector.password)
    new_persona = models.Persona(**elector.model_dump())
    create_persona(new_persona, db)
    persona = db.query(models.Persona).filter(models.Persona.usuario == elector.usuario).first()
    new_elector = models.Elector(id_persona=persona.id)
    db.add(new_elector)
    db.commit()
    db.refresh(new_elector)
    return persona