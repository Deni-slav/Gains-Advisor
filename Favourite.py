from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- Модели --- #
class Review(BaseModel):
    gym_id: int
    user_id: int
    comment: str
    rating: float

class Favorite(BaseModel):
    user_id: int
    gym_id: int

# --- Данни в паметта --- #
favorites: List[Favorite] = []

# --- UR7: Запазване на любима зала --- #
@app.post("/favorites")
def add_favorite(fav: Favorite):
    # Проверка за дублиране
    for f in favorites:
        if f.user_id == fav.user_id and f.gym_id == fav.gym_id:
            return {"message": "Залата вече е в любими"}
    favorites.append(fav)
    return {"message": "Залата е добавена в любими"}

@app.get("/users/{user_id}/favorites")
def get_user_favorites(user_id: int):
    return [f.gym_id for f in favorites if f.user_id == user_id]
