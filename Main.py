from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --- Модели --- #
class User(BaseModel):
    id: int
    name: str
    email: str

class Gym(BaseModel):
    id: int
    name: str
    location: str
    price: float

class Review(BaseModel):
    gym_id: int
    user_id: int
    comment: str
    rating: float

class Favorite(BaseModel):
    user_id: int
    gym_id: int

# --- Данни в паметта --- #
users: List[User] = []
gyms: List[Gym] = []
reviews: List[Review] = []
favorites: List[Favorite] = []

# --- Потребители --- #
@app.post("/register")
def register_user(user: User):
    users.append(user)
    return {"message": "User registered!"}

# --- Фитнес зали --- #
@app.post("/gyms")
def add_gym(gym: Gym):
    gyms.append(gym)
    return {"message": "Gym added!"}

@app.get("/gyms")
def list_gyms(location: Optional[str] = "", max_price: Optional[float] = 9999):
    result = [g for g in gyms if location.lower() in g.location.lower() and g.price <= max_price]
    return result

@app.get("/gyms/{gym_id}")
def get_gym_details(gym_id: int):
    for gym in gyms:
        if gym.id == gym_id:
            return gym
    raise HTTPException(status_code=404, detail="Gym not found")

# --- Рецензии --- #
@app.post("/reviews")
def add_review(review: Review):
    reviews.append(review)
    return {"message": "Review added!"}

@app.get("/gyms/{gym_id}/reviews")
def get_gym_reviews(gym_id: int):
    return [r for r in reviews if r.gym_id == gym_id]

# --- Любими --- #
@app.post("/favorites")
def add_favorite(fav: Favorite):
    favorites.append(fav)
    return {"message": "Gym added to favorites!"}

@app.get("/users/{user_id}/favorites")
def get_favorites(user_id: int):
    fav_ids = [f.gym_id for f in favorites if f.user_id == user_id]
    return [g for g in gyms if g.id in fav_ids]
