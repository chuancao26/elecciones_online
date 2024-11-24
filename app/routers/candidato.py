from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session

from app.database import get_db
from typing import List

from app import schemas, models, oauth2
from sqlalchemy.exc import IntegrityError

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
    try:
        new_lista = models.Candidato(**candidate.model_dump())
        db.add(new_lista)
        db.commit()
        db.refresh(new_lista)
        return new_lista
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,
                            detail=f"candidato with problems, change information!")

@router.get("/{id}", response_model=schemas.CandidatoCreate)
def get_a_candidate(id: int,
                    db: Session=Depends(get_db)):
    candidate = db.query(models.Candidato).filter(models.Candidato.id == id)
    if candidate.first() is None:
        raise HTTPException(status_code=404, detail=f"Candidato with id: {id} does not exist!")
    return candidate.first()

@router.get("/", response_model=List[schemas.CandidatoOut])
def get_candidates(db: Session=Depends(get_db)):
    candidates = (
        db.query(models.Candidato, models.Lista.nombre)
        .join(models.Lista, models.Lista.id == models.Candidato.id_lista)
        .all()
    ) 
    result = [{"candidato": candidate, "nombre_lista": name } for candidate, name in candidates]
    return result

@router.put("/{id}", response_model=schemas.CandidatoCreate,
            status_code=202)
def update_a_candidate(id: int, new_candidate: schemas.CandidatoCreate,
                       db: Session=Depends(get_db),
                       current_admin: schemas.TokenData=Depends(oauth2.get_current_admin)):
    current_candidate = db.query(models.Candidato).filter(models.Candidato.id == id)
    if current_candidate.first() is None:
        raise HTTPException(status_code=404, detail=f"Candidate with id {id} not found!")
    current_candidate.update(new_candidate.model_dump(), synchronize_session=False)
    db.commit()
    return current_candidate.first()
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_candidate(id: int,
                       db: Session=Depends(get_db),
                       current_admin: schemas.TokenData = Depends(oauth2.get_current_admin)):
    current_candidate = db.query(models.Candidato).filter(models.Candidato.id == id)
    if current_candidate.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate with id {id} not found!")
    current_candidate.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
