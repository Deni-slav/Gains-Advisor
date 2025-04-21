from sqlalchemy.orm import Session
from models.gym import Gym
from schemas.gym import GymCreate, GymUpdate

def create_gym(db: Session, gym: GymCreate):
    db_gym = Gym(**gym.dict())
    db.add(db_gym)
    db.commit()
    db.refresh(db_gym)
    return db_gym

def get_gyms(db: Session, location: str = None):
    if location:
        return db.query(Gym).filter(Gym.location == location).all()
    return db.query(Gym).all()

def update_gym(db: Session, gym_id: int, updates: GymUpdate):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if not gym:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(gym, key, value)
    db.commit()
    db.refresh(gym)
    return gym

def get_recommendations(db: Session, location: str):
    return db.query(Gym).filter(Gym.location == location).order_by(Gym.rating.desc()).limit(5).all()
