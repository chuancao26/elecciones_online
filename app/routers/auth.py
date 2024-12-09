from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database import get_db
from typing import List

from app import schemas, models, utils, oauth2

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)

INVALID_CREDENTIALS="Invalid Credentials"

@router.post("/", response_model=schemas.TokenCreated)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user_elector = (
        db.query(models.Elector.id, models.Persona.password)
        .join(models.Persona, models.Elector.id_persona == models.Persona.id, isouter=True)
        .filter(models.Persona.usuario == user_credentials.username)
        .first()
    )
    user_admin= (
        db.query(models.Administrador.id, models.Persona.password)
        .join(models.Persona, models.Administrador.id_persona == models.Persona.id, isouter=True)
        .filter(models.Persona.usuario == user_credentials.username)
        .first()
    )
    if not user_elector and not user_admin:
        raise HTTPException(status_code=404, detail=INVALID_CREDENTIALS)
    elif user_elector and not user_admin:
        if not utils.verify_password(user_credentials.password, user_elector.password):
            raise HTTPException(status_code=404, detail=INVALID_CREDENTIALS)
        access_token = oauth2.create_access_token(data={"id": user_elector.id, "type_user": "elector"})

        return {"access_token": access_token, "token_type": "bearer"}
    elif user_admin and not user_elector:
        if not utils.verify_password(user_credentials.password, user_admin.password):
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        access_token = oauth2.create_access_token(data={"id": user_admin.id, "type_user": "admin"})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=404, detail="Duplicated User")

@router.get("/", response_model=schemas.CurrentUserData)
def get_current_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Problems with credentials, token not valid",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = oauth2.verify_access_token(token, credentials_exception)
    if token.type_user == "elector":
        elector = (
            db.query(models.Elector.id,
                     models.Persona.nombres,
                     models.Persona.apellido_paterno,
                     models.Persona.apellido_materno)
            .join(models.Elector, models.Elector.id_persona == models.Persona.id)
            .filter(models.Elector.id == token.id)
            .first()
        )
        elector = schemas.PersonaOut(id=elector.id,
                                     nombres=elector.nombres,
                                     apellido_paterno=elector.apellido_paterno,
                                     apellido_materno=elector.apellido_materno)
        current_user_data = schemas.CurrentUserData(persona=elector, type_user=token.type_user)
        return current_user_data
    else:
        admin = (
            db.query(models.Administrador.id,
                     models.Persona.nombres,
                     models.Persona.apellido_paterno,
                     models.Persona.apellido_materno)
           .join(models.Administrador, models.Administrador.id_persona == models.Persona.id)
           .filter(models.Administrador.id == token.id)
           .first()
        )
        admin= schemas.PersonaOut(id=admin.id,
                                  nombres=admin.nombres,
                                  apellido_paterno=admin.apellido_paterno,
                                  apellido_materno=admin.apellido_materno)
        current_user_data = schemas.CurrentUserData(persona=admin, type_user=token.type_user)
        return current_user_data
