from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from typing import List

from app import schemas, models, oauth2

router = APIRouter(
    tags=["Lista"],
    prefix="/lista",
)

@router.get("/", response_model=List[schemas.ListaOut])
def get_lists(db: Session = Depends(get_db)):
    lists = db.query(models.Lista).all()
    return lists

@router.get("/{id}", response_model=List[schemas.ListaOut])
def get_lists(id: int,
              db: Session = Depends(get_db),
              current_admin: schemas.TokenData=Depends(oauth2.get_current_admin)):
    list = db.query(models.Lista).filter(models.Lista.id == id).first()
    if list is None:
        raise HTTPException(status_code=404, detail=f"Lista with id: {id} not found")
    return list
    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ListaOut)
def create_list(list: schemas.ListaCreate, db: Session = Depends(get_db),
                current_admin: schemas.TokenData=Depends(oauth2.get_current_admin)):

    election = db.query(models.Eleccion).filter(models.Eleccion.id==list.id_eleccion).first()
    if election is None:
        raise HTTPException(status_code=404,
                             detail=f"Election with id: {list.id_eleccion} does not exist") 
    new_list = models.Lista(**list.model_dump())
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(id: int, db: Session = Depends(get_db),
              current_admin: schemas.TokenData=Depends(oauth2.get_current_admin)):
    list = db.query(models.Lista).filter(models.Lista.id == id)
    if list.first() is None:
        raise HTTPException(status_code=404, detail=f"Lista with id: {id} not found")
    list.delete(synchronize_session=False)
    db.commit()
    db.refresh(list)
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)