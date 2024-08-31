from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from typing import List

from app import schemas, models, oauth2

router = APIRouter(
    prefix="/voto",
    tags=["voto"]
)
@router.post("/", status_code=202)
def create_vote()