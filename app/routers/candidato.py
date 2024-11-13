from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from typing import List

from app import schemas, models, oauth2

router = APIRouter(
    tags=["candidato"],
    prefix="/candidato"
)

@router.post("/", status_code=202, response_model=schemas.CandidatoCreate)
def create_candidate(candidate: schemas.CandidatoCreate,
                     db: Session=Depends(get_db),
                     current_admin: schemas.TokenData=Depends(oauth2.get_current_admin)):
    lista = db.query(models.Lista).filter(models.Lista.id == candidate.id_lista).first()
    if lista is None:
        raise HTTPException(status_code=404,
                            detail=f"List with id: {candidate.id_lista} does not exist!")
    new_lista = models.Candidato(**candidate.model_dump())
    db.add(new_lista)
    db.commit()
    db.refresh(new_lista)
    return new_lista

@router.get("/", response_model=List[schemas.CandidatoOut])
def get_candidates(db: Session=Depends(get_db)):
    candidates = (
        db.query(models.Candidato, models.Lista.nombre)
        .join(models.Lista, models.Lista.id == models.Candidato.id_lista)
        .all()
    ) 
    result = [{"candidato": candidate, "nombre_lista": name } for candidate, name in candidates]
    return result

@router.put("/{id}", response_model= schemas.CandidatoOut, status_code=202)
def update_a_candidate(id: int, new_candidate: schemas.CandidatoCreate,
                       db: Session=Depends(get_db),
                       current_admin: schemas.TokenData=Depends(oauth2.get_current_admin)):
    current_candidate = db.query(models.Candidato).filter(models.Candidato.id == id)
    if current_candidate.first() is None:
        return HTTPException(status_code=404, detail=f"Candidate with id {id} not found!")
    current_candidate.update(new_candidate.model_dump(), synchronize_session=False)
    db.add(current_candidate)
    db.commit()
    return current_candidate.first()
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_candidate(id: int,
                       db: Session=Depends(get_db),
                       current_admin: schemas.TokenData = Depends(oauth2.get_current_admin)):
    current_candidate = db.query(models.Candidato).filter(models.Candidato.id == id)
    if current_candidate.first() is None:
        return HTTPException(status_code=404, detail=f"Candidate with id {id} not found!")
    current_candidate.delete()
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
