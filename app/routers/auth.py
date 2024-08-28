from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import notendswith_op

from app.database import get_db
from app.utils import hash_password, verify_password
from typing import List

from app import schemas, models, utils, oauth2

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)
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
        db.query(models.Administrador.id).
        join(models.Persona, models.Administrador.id_persona == models.Persona.id, isouter=True)
        .filter(models.Persona.usuario == user_credentials.username)
        .first()
    )
    if not user_elector and not user_admin:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    elif user_elector and not user_admin:
        if not utils.verify_password(user_credentials.password, user_elector.password):
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        access_token = oauth2.create_access_token(data={"id": user_elector.id, "type_user": "elector"})

        return {"access_token": access_token, "token_type": "bearer"}
    elif user_admin and not user_elector:
        if not utils.verify_password(user_credentials.password, user_admin.password):
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        access_token = oauth2.create_access_token(data={"id": user_admin.id, "type_user": "admin"})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=404, detail="Duplicated User")


