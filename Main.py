from routers import gym_router
from typing import Optional, List, Dict

class Gym:
    def __init__(self, id: int, name: str, address: str, rating: Optional[float] = None,
                 services: Optional[List[str]] = None, opening_hours: Optional[str] = None,
                 price: Optional[str] = None, location: Optional[str] = None):
        self.id = id
        self.name = name
        self.address = address
        self.rating = rating
        self.services = services or []
        self.opening_hours = opening_hours
        self.price = price
        self.location = location

class User:
    def __init__(self, username: str, email: str, password: str, full_name: Optional[str] = None):
        self.username = username
        self.email = email
        self.password = password
        self.full_name = full_name

class Review:
    def __init__(self, gym_id: int, user_id: int, rating: int, comment: Optional[str] = None):
        self.gym_id = gym_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

class FitnessApp:
    def __init__(self):
        self.favorite_gyms: List[Gym] = []
        self.nearby_gyms = [
            Gym(1, "Power Gym", "123 Main St", 4.5),
            Gym(2, "Fit Life", "456 Oak Ave", 4.2),
            Gym(3, "Muscle World", "789 Pine Rd", 4.0)
        ]
        self.registered_users: List[User] = []
        self.gym_reviews: List[Review] = []
        self.current_user: Optional[User] = None

    def display_menu(self):
        print("\nФитнес Приложение - Меню:")
        print("--------------------------")
        print("1. Любими фитнеси")
        print("2. Локация на близки фитнеси")
        print("3. Регистрация/Вход")
        print("4. Ревюта на фитнеси")
        print("5. Добави фитнес")
        print("6. Редактирай фитнес")
        print("7. Препоръки по локация")
        print("8. Търсене на фитнес")
        print("9. Изход")
        
        while True:
            try:
                choice = int(input("\nВъведете числото, спрямо услугата която искате: "))
                if 1 <= choice <= 9:
                    return choice
                print("Моля, въведете число между 1 и 9!")
            except ValueError:
                print("Моля, въведете валидно число!")

    def run(self):
        print("Добре дошли във Фитнес Приложението!")
        
        while True:
            choice = self.display_menu()
            
            match choice:
                case 1:
                    self.handle_favorite_gyms()
                case 2:
                    self.handle_nearby_gyms()
                case 3:
                    self.handle_registration_login()
                case 4:
                    self.handle_reviews()
                case 5:
                    self.add_gym()
                case 6:
                    self.edit_gym()
                case 7:
                    self.recommend_gyms()
                case 8:
                    self.search_gyms()
                case 9:
                    print("\nДовиждане! Благодарим, че използвахте нашето приложение.")
                    break

    def handle_favorite_gyms(self):
        if not self.favorite_gyms:
            print("\nНямате любими фитнеси все още.")
            if self.current_user:
                print("Добавете фитнес към любими от списъка с близки фитнеси (Опция 2).")
            return
        
        print("\nВашите любими фитнеси:")
        for gym in self.favorite_gyms:
            print(f"{gym.id}. {gym.name} - {gym.address} (Рейтинг: {gym.rating or 'няма'})")

    def handle_nearby_gyms(self):
        print("\nБлизки фитнеси:")
        for gym in self.nearby_gyms:
            print(f"{gym.id}. {gym.name} - {gym.address} (Рейтинг: {gym.rating})")
        
        if self.current_user:
            print("\nДействия:")
            print("1. Добави към любими")
            print("2. Преглед на ревюта")
            print("3. Напиши ревю")
            print("4. Назад")
            
            try:
                action = int(input("Изберете действие: "))
                if action == 1:
                    self.add_to_favorites()
                elif action == 2:
                    self.view_gym_reviews()
                elif action == 3:
                    self.add_review()
            except ValueError:
                pass

    def add_gym(self):
        print("\nДобавяне на нов фитнес:")
        try:
            name = input("Име: ")
            address = input("Адрес: ")
            location = input("Локация (град/район): ")
            rating = float(input("Рейтинг (по избор): ") or 0.0)
            services = input("Услуги (разделени със запетая): ").split(",")
            opening_hours = input("Работно време: ")
            price = input("Цена: ")

            new_id = max([g.id for g in self.nearby_gyms], default=0) + 1
            new_gym = Gym(new_id, name, address, rating, services, opening_hours, price, location)
            self.nearby_gyms.append(new_gym)
            print(f"Фитнесът '{name}' е добавен успешно!")
        except ValueError:
            print("Невалидни данни!")

    def add_to_favorites(self):
        try:
            gym_id = int(input("Въведете ID на фитнеса, който искате да добавите: "))
            gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
            
            if gym and gym not in self.favorite_gyms:
                self.favorite_gyms.append(gym)
                print(f"{gym.name} е добавен към любими!")
            elif gym in self.favorite_gyms:
                print("Този фитнес вече е във любими!")
            else:
                print("Невалидно ID на фитнес!")
        except ValueError:
            print("Моля, въведете валидно число!")

    def handle_registration_login(self):
        print("\n1. Регистрация")
        print("2. Вход")
        print("3. Назад")
        
        try:
            choice = int(input("Изберете опция: "))
            if choice == 1:
                self.register_user()
            elif choice == 2:
                self.login_user()
        except ValueError:
            pass

    def register_user(self):
        print("\nРегистрация на нов потребител:")
        username = input("Потребителско име: ")
        email = input("Имейл адрес: ")
        password = input("Парола: ")
        full_name = input("Пълно име (по избор): ") or None
        
        if any(u.username == username for u in self.registered_users):
            print("Потребителското име вече съществува!")
            return
        
        if any(u.email == email for u in self.registered_users):
            print("Имейл адресът вече е регистриран!")
            return
        
        new_user = User(username, email, password, full_name)
        self.registered_users.append(new_user)
        self.current_user = new_user
        print("Регистрацията е успешна! Влезли сте в системата.")

    def login_user(self):
        print("\nВход в системата:")
        username = input("Потребителско име: ")
        password = input("Парола: ")
        
        user = next((u for u in self.registered_users if u.username == username and u.password == password), None)
        if user:
            self.current_user = user
            print(f"Добре дошли, {user.username}!")
        else:
            print("Невалидно потребителско име или парола!")

    def search_gyms(self):
        keyword = input("Търси по име или услуга: ").lower()
        results = [g for g in self.nearby_gyms if keyword in g.name.lower() or
                   any(keyword in s.lower() for s in g.services)]
        if not results:
            print("Няма съвпадения.")
            return

        print("\nРезултати от търсенето:")
        for gym in results:
            print(f"{gym.name} - {gym.address}, Услуги: {', '.join(gym.services)}")

    def edit_gym(self):
        try:
            gym_id = int(input("ID на фитнеса, който искате да редактирате: "))
            gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
            if not gym:
                print("Фитнес с такова ID не съществува.")
                return

            print(f"Редактиране на '{gym.name}' (оставете празно за без промяна)")
            gym.name = input(f"Име ({gym.name}): ") or gym.name
            gym.address = input(f"Адрес ({gym.address}): ") or gym.address
            gym.location = input(f"Локация ({gym.location}): ") or gym.location
            gym.opening_hours = input(f"Работно време ({gym.opening_hours}): ") or gym.opening_hours
            gym.price = input(f"Цена ({gym.price}): ") or gym.price
            services = input("Услуги (разделени със запетая): ")
            if services:
                gym.services = [s.strip() for s in services.split(",")]

            print("Редакцията е завършена.")
        except ValueError:
            print("Невалидно ID!")

    def recommend_gyms(self):
        location = input("Въведете желана локация: ")
        gyms = [g for g in self.nearby_gyms if g.location and g.location.lower() == location.lower()]
        if not gyms:
            print("Няма фитнеси в тази локация.")
            return

        sorted_gyms = sorted(gyms, key=lambda g: g.rating or 0.0, reverse=True)
        print(f"\nПрепоръчани фитнеси в {location}:")
        for gym in sorted_gyms:
            print(f"{gym.name} - Рейтинг: {gym.rating}/5, Цена: {gym.price}, Работно време: {gym.opening_hours}")

    def handle_reviews(self):
        if not self.gym_reviews:
            print("\nВсе още няма ревюта.")
            return
        
        print("\nПоследни ревюта:")
        for review in self.gym_reviews[-5:]:  # Показва последните 5 ревюта
            gym = next(g for g in self.nearby_gyms if g.id == review.gym_id)
            user = next(u for u in self.registered_users if u.username == review.user_id)
            print(f"Фитнес: {gym.name}, Потребител: {user.username}, Оценка: {review.rating}/5")
            if review.comment:
                print(f"Коментар: {review.comment}")
            print()

    def view_gym_reviews(self):
        try:
            gym_id = int(input("Въведете ID на фитнеса за преглед на ревюта: "))
            gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
            
            if not gym:
                print("Невалидно ID на фитнес!")
                return
            
            reviews = [r for r in self.gym_reviews if r.gym_id == gym_id]
            if not reviews:
                print(f"Фитнесът {gym.name} все още няма ревюта.")
                return
            
            print(f"\nРевюта за {gym.name}:")
            for review in reviews:
                user = next(u for u in self.registered_users if u.username == review.user_id)
                print(f"Потребител: {user.username}, Оценка: {review.rating}/5")
                if review.comment:
                    print(f"Коментар: {review.comment}")
                print()
        except ValueError:
            print("Моля, въведете валидно число!")

    def add_review(self):
        if not self.current_user:
            print("Трябва да сте влезли в системата, за да пишете ревюта!")
            return
        
        try:
            gym_id = int(input("Въведете ID на фитнеса, за който пишете ревю: "))
            gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
            
            if not gym:
                print("Невалидно ID на фитнес!")
                return
            
            rating = int(input("Оценка (1-5): "))
            if rating < 1 or rating > 5:
                print("Оценката трябва да е между 1 и 5!")
                return
            
            comment = input("Коментар (по избор): ") or None
            
            new_review = Review(gym_id, self.current_user.username, rating, comment)
            self.gym_reviews.append(new_review)
            print("Ревюто е добавено успешно!")
        except ValueError:
            print("Моля, въведете валидни данни!")

if __name__ == "__main__":
    app = FitnessApp()
    app.run()

