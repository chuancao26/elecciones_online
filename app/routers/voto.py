from ctypes.wintypes import HACCEL

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from typing import List

from app import schemas, models, oauth2

router = APIRouter(
    prefix="/voto",
    tags=["voto"]
)
@router.post("/", status_code=202)
def create_vote(vote: schemas.VotoCreate,
                db: Session = Depends(get_db),
                current_user: schemas.TokenData=Depends(oauth2.get_current_elector)):
    #make sure id's exist
    lista = db.query(models.Lista).filter(models.Lista.id == vote.id_lista).first()
    if lista is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"list with id: {vote.id_lista} not found")
    new_vote = models.Voto(id_lista=vote.id_lista, id_elector=current_user.id)
    try:
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Vote created successfully!"}
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This vote already exists.")