
# coding: utf-8
import tkinter as tk
from tkinter import messagebox, simpledialog

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
    def __init__(self, username, email, password, full_name=None):
        self.username = username
        self.email = email
        self.password = password
        self.full_name = full_name

class Review:
    def __init__(self, gym_id, user_id, rating, comment=None):
        self.gym_id = gym_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

class FitnessAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Фитнес Приложение")

        self.favorite_gyms = []
        self.nearby_gyms = [
            Gym(1, "Power Gym", "123 Main St", 4.5),
            Gym(2, "Fit Life", "456 Oak Ave", 4.2),
            Gym(3, "Muscle World", "789 Pine Rd", 4.0)
        ]
        self.registered_users = []
        self.gym_reviews = []
        self.current_user = None

        self.menu_ui()

    def menu_ui(self):
        tk.Label(self.root, text="Добре дошли във Фитнес Приложението!", font=("Arial", 14)).pack(pady=10)

        options = [
            ("Любими фитнеси", self.handle_favorite_gyms),
            ("Локация на близки фитнеси", self.handle_nearby_gyms),
            ("Регистрация / Вход", self.handle_registration_login),
            ("Ревюта на фитнеси", self.handle_reviews),
            ("Добави фитнес", self.add_gym),
            ("Редактирай фитнес", self.edit_gym),
            ("Препоръки по локация", self.recommend_gyms),
            ("Търсене на фитнес", self.search_gyms),
            ("Изход", self.root.quit)
        ]

        for label, command in options:
            tk.Button(self.root, text=label, width=40, command=command).pack(pady=3)

    def show_message(self, title, msg):
        messagebox.showinfo(title, msg)

    def handle_favorite_gyms(self):
        if not self.favorite_gyms:
            self.show_message("Любими", "Нямате любими фитнеси.")
        else:
            text = "\n".join([f"{g.name} - {g.address} (Рейтинг: {g.rating})" for g in self.favorite_gyms])
            self.show_message("Любими фитнеси", text)

    def handle_nearby_gyms(self):
        gyms_text = "\n".join([f"{g.id}. {g.name} - {g.address} (Рейтинг: {g.rating})" for g in self.nearby_gyms])
        self.show_message("Близки фитнеси", gyms_text)

        if self.current_user:
            gym_id = simpledialog.askinteger("Добави към любими", "Въведете ID на фитнес:")
            gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
            if gym and gym not in self.favorite_gyms:
                self.favorite_gyms.append(gym)
                self.show_message("Успех", f"{gym.name} е добавен към любими!")

    def handle_registration_login(self):
        option = simpledialog.askinteger("Регистрация/Вход", "1 - Регистрация, 2 - Вход")
        if option == 1:
            self.register_user()
        elif option == 2:
            self.login_user()

    def register_user(self):
        username = simpledialog.askstring("Регистрация", "Потребителско име:")
        email = simpledialog.askstring("Регистрация", "Имейл:")
        password = simpledialog.askstring("Регистрация", "Парола:")
        full_name = simpledialog.askstring("Регистрация", "Пълно име (по избор):")

        if any(u.username == username for u in self.registered_users):
            self.show_message("Грешка", "Потребителското име вече съществува.")
            return

        if any(u.email == email for u in self.registered_users):
            self.show_message("Грешка", "Имейл адресът вече е регистриран.")
            return

        user = User(username, email, password, full_name)
        self.registered_users.append(user)
        self.current_user = user
        self.show_message("Успех", "Регистрацията е успешна.")

    def login_user(self):
        username = simpledialog.askstring("Вход", "Потребителско име:")
        password = simpledialog.askstring("Вход", "Парола:")
        user = next((u for u in self.registered_users if u.username == username and u.password == password), None)
        if user:
            self.current_user = user
            self.show_message("Успех", f"Добре дошли, {user.username}!")
        else:
            self.show_message("Грешка", "Невалидни данни.")

    def add_gym(self):
        name = simpledialog.askstring("Добави фитнес", "Име:")
        address = simpledialog.askstring("Добави фитнес", "Адрес:")
        location = simpledialog.askstring("Добави фитнес", "Локация:")
        rating = simpledialog.askfloat("Добави фитнес", "Рейтинг:")
        services = simpledialog.askstring("Добави фитнес", "Услуги (разделени със запетая):").split(",")
        opening_hours = simpledialog.askstring("Добави фитнес", "Работно време:")
        price = simpledialog.askstring("Добави фитнес", "Цена:")

        new_id = max([g.id for g in self.nearby_gyms], default=0) + 1
        gym = Gym(new_id, name, address, rating, services, opening_hours, price, location)
        self.nearby_gyms.append(gym)
        self.show_message("Успех", f"Фитнесът '{name}' е добавен успешно!")

    def edit_gym(self):
        gym_id = simpledialog.askinteger("Редактирай фитнес", "ID на фитнеса:")
        gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
        if not gym:
            self.show_message("Грешка", "Фитнес не е намерен.")
            return

        gym.name = simpledialog.askstring("Редактирай фитнес", f"Име ({gym.name}):") or gym.name
        gym.address = simpledialog.askstring("Редактирай фитнес", f"Адрес ({gym.address}):") or gym.address
        gym.location = simpledialog.askstring("Редактирай фитнес", f"Локация ({gym.location}):") or gym.location
        gym.opening_hours = simpledialog.askstring("Редактирай фитнес", f"Работно време ({gym.opening_hours}):") or gym.opening_hours
        gym.price = simpledialog.askstring("Редактирай фитнес", f"Цена ({gym.price}):") or gym.price
        services = simpledialog.askstring("Редактирай фитнес", "Услуги (разделени със запетая):")
        if services:
            gym.services = [s.strip() for s in services.split(",")]
        self.show_message("Успех", "Редакцията е завършена.")

    def recommend_gyms(self):
        location = simpledialog.askstring("Препоръки", "Въведете локация:")
        gyms = [g for g in self.nearby_gyms if g.location.lower() == location.lower()]
        gyms.sort(key=lambda g: g.rating, reverse=True)
        if gyms:
            text = "\n".join([f"{g.name} - Рейтинг: {g.rating}" for g in gyms])
            self.show_message(f"Препоръки за {location}", text)
        else:
            self.show_message("Инфо", "Няма фитнеси в тази локация.")

    def search_gyms(self):
        keyword = simpledialog.askstring("Търсене", "Въведете дума за търсене:").lower()
        results = [g for g in self.nearby_gyms if keyword in g.name.lower() or any(keyword in s.lower() for s in g.services)]
        if results:
            text = "\n".join([f"{g.name} - {g.address}" for g in results])
            self.show_message("Резултати", text)
        else:
            self.show_message("Резултати", "Няма съвпадения.")

    def handle_reviews(self):
        if not self.gym_reviews:
            self.show_message("Ревюта", "Все още няма ревюта.")
            return
        text = "\n\n".join([f"Фитнес ID: {r.gym_id}, Оценка: {r.rating}, Коментар: {r.comment or 'Няма'}" for r in self.gym_reviews])
        self.show_message("Последни ревюта", text)

# Стартиране
if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessAppGUI(root)
    root.mainloop()
