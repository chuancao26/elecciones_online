from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

from app import schemas
from app import models

router = APIRouter(prefix="/eleccion",
                   tags=["eleccion"])
@router.get("/", response_model=List[schemas.EleccionOut])
def get_elections(db: Session = Depends(get_db)):
    elections = db.query(models.Eleccion).all()
    return elections

@router.post("/", response_model=schemas.EleccionOut)
def create_election(election: schemas.EleccionCreate, db: Session = Depends(get_db)):
    new_election = models.Eleccion(**election.model_dump())
    db.add(new_election)
    db.commit()
    db.refresh(new_election)
    return new_election
