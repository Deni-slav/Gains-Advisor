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

reviews: List[Review] = []

# --- UR6: Добавяне на рецензия --- #
@app.post("/reviews")
def add_review(review: Review):
    reviews.append(review)
    return {"message": "Рецензията е добавена успешно!"}

@app.get("/gyms/{gym_id}/reviews")
def get_reviews_for_gym(gym_id: int):
    return [r for r in reviews if r.gym_id == gym_id]