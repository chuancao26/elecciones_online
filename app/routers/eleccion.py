from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from typing import List

from app import schemas, models, oauth2

router = APIRouter(prefix="/eleccion",
                   tags=["eleccion"])
@router.get("/", response_model=List[schemas.EleccionOut])
def get_elections(db: Session = Depends(get_db),
                 current_user: schemas.TokenData = Depends(oauth2.get_current_admin)):
    elections = db.query(models.Eleccion).all()
    return elections

@router.post("/", response_model=schemas.EleccionOut)
def create_election(election: schemas.EleccionCreate, db: Session = Depends(get_db), 
                    current_user: schemas.TokenData = Depends(oauth2.get_current_admin)):
    new_election = models.Eleccion(**election.model_dump())
    db.add(new_election)
    db.commit()
    db.refresh(new_election)
    return new_election

@router.get("/{id}", response_model=schemas.EleccionOut)
def get_election(id: int, db: Session = Depends(get_db),
                 current_user: schemas.TokenData = Depends(oauth2.get_current_admin)):
    election = db.query(models.Eleccion).filter(models.Eleccion.id == id)
    if election.first() is None:
        raise HTTPException(status_code=404, detail=f"id: {id} not found")
    return election.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_election(id: int, db: Session = Depends(get_db), 
                    current_user: schemas.TokenData = Depends(oauth2.get_current_admin)):
    election = db.query(models.Eleccion).filter(models.Eleccion.id == id)
    if election.first() is None:
        raise HTTPException(status_code=404, detail=f"id: {id} not found")
    election.delete(synchronize_session=False)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.EleccionOut, status_code=status.HTTP_200_OK)
def update_election(election: schemas.EleccionCreate, id: int, db: Session = Depends(get_db),
                    current_user: schemas.TokenData = Depends(oauth2.get_current_admin)):
    updated_election = db.query(models.Eleccion).filter(models.Eleccion.id == id)
    if updated_election.first() is None:
        raise HTTPException(status_code=404, detail=f"id: {id} not found")
    updated_election.update(election.model_dump(), synchronize_session=False)
    db.commit()
    return updated_election.first()
