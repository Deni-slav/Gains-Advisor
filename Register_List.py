from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- Модел за потребител --- #
class User(BaseModel):
    id: int
    name: str
    email: str

# --- Временен списък с потребители --- #
users: List[User] = []

# --- UR1: Регистрация на потребител --- #
@app.post("/register")
def register_user(user: User):
    for u in users:
        if u.email == user.email:
            return {"message": "Имейл адресът вече е регистриран."}
    users.append(user)
    return {"message": "Регистрацията е успешна!"}

    # --- Модел за фитнес зала (ако не е добавен още) --- #


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
]


# --- UR2: Преглед на всички зали --- #
@app.get("/gyms")
def list_gyms():
    return gyms
