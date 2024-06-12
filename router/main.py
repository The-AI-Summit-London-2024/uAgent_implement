from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
import json

router = APIRouter(
    prefix="/main",
    tags=["main"],
)
