class Gym:
    def __init__(self, id, name, address, rating=None, services=None, opening_hours=None, price=None, location=None):
        self.id = id
        self.name = name
        self.address = address
        self.rating = rating or 0.0
        self.services = services or []
        self.opening_hours = opening_hours or ""
        self.price = price or ""
        self.location = location or ""

class User:
    def __init__(self, username, email, password, role="guest", full_name=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role  
        self.full_name = full_name

class Review:
    def __init__(self, gym_id, user_id, rating, comment=None):
        self.gym_id = gym_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment 