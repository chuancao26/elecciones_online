from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database import get_db
from typing import List

from app import schemas, models, utils, oauth2

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)
def create_persona(new_persona: models.Persona, db: Session = Depends(get_db)):
    db.add(new_persona)
    db.commit()
    db.refresh(new_persona)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PersonaOut)
def create_admin(admin: schemas.PersonaCreate, db: Session = Depends(get_db)):
    persona = db.query(models.Persona).filter(models.Persona.usuario == admin.usuario).first()
    if persona:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user with username: {admin.usuario} has already been used")

    admin.password = utils.hash_password(admin.password)

    new_persona = models.Persona(**admin.model_dump())
    create_persona(new_persona, db)

    persona = db.query(models.Persona).filter(models.Persona.usuario == admin.usuario).first()
    new_admin = models.Administrador(id_persona=persona.id)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return persona