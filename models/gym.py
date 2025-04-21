from sqlalchemy import Column, Integer, String, Float
from database import Base

class Gym(Base):
    __tablename__ = "gyms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    rating = Column(Float)
    services = Column(String)  # Може да е JSON string или отделна таблица
    working_hours = Column(String)
    price_range = Column(String)
