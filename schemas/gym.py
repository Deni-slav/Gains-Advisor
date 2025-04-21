from pydantic import BaseModel
from typing import Optional

class GymBase(BaseModel):
    name: str
    location: str
    rating: float
    services: str
    working_hours: str
    price_range: str

class GymCreate(GymBase):
    pass

class GymUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    rating: Optional[float]
    services: Optional[str]
    working_hours: Optional[str]
    price_range: Optional[str]

class GymOut(GymBase):
    id: int

    model_config = {
        "from_attributes": True
    }
