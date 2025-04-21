from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.gym import *
from services import gym_service

router = APIRouter(prefix="/gyms", tags=["Gyms"])

@router.post("/", response_model=GymOut)
def add_gym(gym: GymCreate, db: Session = Depends(get_db)):
    return gym_service.create_gym(db, gym)

@router.get("/", response_model=list[GymOut])
def list_gyms(location: str = None, db: Session = Depends(get_db)):
    return gym_service.get_gyms(db, location)

@router.put("/{gym_id}", response_model=GymOut)
def edit_gym(gym_id: int, updates: GymUpdate, db: Session = Depends(get_db)):
    gym = gym_service.update_gym(db, gym_id, updates)
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")
    return gym

@router.get("/recommendations/", response_model=list[GymOut])
def get_recommendations(location: str, db: Session = Depends(get_db)):
    return gym_service.get_recommendations(db, location)
