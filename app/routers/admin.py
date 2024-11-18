from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db

from app import schemas, models, utils, oauth2

from typing import List
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

    persona = (db.query(models.Persona)
               .filter(models.Persona.usuario == admin.usuario)
               .first())
    if persona:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user with username: {admin.usuario} has already been used")

    admin.password = utils.hash_password(admin.password)

    new_persona = models.Persona(**admin.model_dump())
    create_persona(new_persona, db)
    persona = (db.query(models.Persona)
               .filter(models.Persona.usuario == admin.usuario)
               .first())
    new_admin = models.Administrador(id_persona=persona.id)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    persona = (db.query(models.Administrador.id.label("id"),
                        models.Persona.nombres,
                        models.Persona.apellido_paterno,
                        models.Persona.apellido_materno)
               .join(models.Persona,
                     models.Persona.id == models.Administrador.id_persona)
               .filter(models.Persona.usuario == admin.usuario).first())
    return persona
@router.get("/",
           response_model=List[schemas.PersonaOut])
def get_admins(db: Session = Depends(get_db)):
    personas = (db.query(models.Administrador.id.label("id"),
                        models.Persona.nombres,
                        models.Persona.apellido_paterno,
                        models.Persona.apellido_materno)
               .join(models.Persona,
                     models.Persona.id == models.Administrador.id_persona).all())
    return personas
@router.put("/{id}", response_model=schemas.PersonaOut)
def update_admin(id: int, new_admin: schemas.PersonaCreate,
                 db: Session = Depends(get_db),
                 info_admin: schemas.TokenData=Depends(oauth2.get_current_admin)):
    current_admin = db.query(models.Administrador).filter(models.Administrador.id == id)
    if current_admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with id {id} not found")
    current_admin.update(new_admin.model_dump(),
                         synchronize_session=False)
    db.commit()
    return current_admin.first()
