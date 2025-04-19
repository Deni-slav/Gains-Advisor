from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --- Модел за фитнес зала --- #
class Gym(BaseModel):
    id: int
    name: str
    location: str
    price: float
    description: str

# --- Временен списък със зали --- #
gyms: List[Gym] = [
    Gym(id=1, name="FitZone", location="София", price=35, description="Модерна зала в центъра."),
    Gym(id=2, name="Iron Paradise", location="Пловдив", price=45, description="Голяма зала с много оборудване."),
    Gym(id=3, name="BodyWorks", location="София", price=30, description="Бюджетна зала с основни удобства.")
]

# --- UR3: Търсене на зали по локация --- #
@app.get("/gyms/search")
def search_gyms(location: Optional[str] = ""):
    results = [g for g in gyms if location.lower() in g.location.lower()]
    return results


# --- UR4: Преглед на конкретна зала по ID --- #
@app.get("/gyms/{gym_id}")
def get_gym_details(gym_id: int):
    for gym in gyms:
        if gym.id == gym_id:
            return gym
    return {"error": "Залата не е намерена"}
