
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
        self.clear()
        tk.Label(self.root, text="Добре дошли във Фитнес Приложението!", font=("Arial", 14)).pack(pady=10)

        options = [
            ("Вход / Регистрация", self.handle_registration_login),
            ("Преглед на фитнеси", self.view_gyms),
            ("Търсене на фитнес", self.search_gyms),
            ("Любими фитнеси", self.handle_favorite_gyms),
            ("Преглед на ревюта", self.view_reviews),
            ("Добавяне на ревю", self.add_review),
            ("Препоръки", self.recommend_gyms),
            ("Добавяне на фитнес (admin)", self.add_gym),
            ("Редактиране на фитнес (admin)", self.edit_gym),
            ("Изход", self.root.quit)
        ]

        for label, action in options:
            tk.Button(self.root, text=label, width=40, command=action).pack(pady=3)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_message(self, title, msg):
        messagebox.showinfo(title, msg)

    def handle_registration_login(self):
        choice = simpledialog.askinteger("Избор", "1 - Регистрация\n2 - Вход", minvalue=1, maxvalue=2)
        if choice == 1:
            self.register()
        elif choice == 2:
            self.login_user()

    def register(self):
        username = simpledialog.askstring("Регистрация", "Потребителско име:")
        email = simpledialog.askstring("Регистрация", "Имейл:")
        password = simpledialog.askstring("Регистрация", "Парола:", show='*')
        role = simpledialog.askstring("Регистрация", "Роля (guest/subscribed/admin):", initialvalue="guest")

        if any(u.username == username for u in self.registered_users):
            self.show_message("Грешка", "Потребителското име вече съществува!")
            return
        if any(u.email == email for u in self.registered_users):
            self.show_message("Грешка", "Имейлът вече е регистриран!")
            return

        self.current_user = User(username, email, password, role)
        self.registered_users.append(self.current_user)
        self.show_message("Успех", f"Добре дошли, {username}!")

    def login_user(self):
        username = simpledialog.askstring("Вход", "Потребителско име:")
        password = simpledialog.askstring("Вход", "Парола:", show='*')
        user = next((u for u in self.registered_users if u.username == username and u.password == password), None)
        if user:
            self.current_user = user
            self.show_message("Успех", f"Влязохте като {user.username}")
        else:
            self.show_message("Грешка", "Невалидни данни!")

    def view_gyms(self):
        text = "\n".join([f"{g.id}. {g.name} - {g.address} ({g.rating}/5)" for g in self.nearby_gyms])
        messagebox.showinfo("Фитнеси", text)

    def search_gyms(self):
        keyword = simpledialog.askstring("Търсене", "Ключова дума:")
        results = [g for g in self.nearby_gyms if keyword.lower() in g.name.lower()]
        if not results:
            self.show_message("Резултати", "Няма съвпадения.")
            return
        text = "\n".join([f"{g.name} - {g.address}" for g in results])
        self.show_message("Резултати", text)

    def handle_favorite_gyms(self):
        if not self.favorite_gyms:
            self.show_message("Любими", "Нямате добавени фитнеси.")
            return
        text = "\n".join([f"{g.name} - {g.address}" for g in self.favorite_gyms])
        self.show_message("Любими", text)

    def view_reviews(self):
        if not self.gym_reviews:
            self.show_message("Ревюта", "Няма ревюта.")
            return
        text = "\n".join([f"{r.user_id} за {r.gym_id}: {r.rating}/5" for r in self.gym_reviews])
        self.show_message("Ревюта", text)

    def add_review(self):
        if not self.current_user:
            self.show_message("Грешка", "Трябва да сте влезли в системата.")
            return
        gym_id = simpledialog.askinteger("Ревю", "ID на фитнес:")
        rating = simpledialog.askinteger("Ревю", "Оценка (1-5):", minvalue=1, maxvalue=5)
        comment = simpledialog.askstring("Ревю", "Коментар:")
        self.gym_reviews.append(Review(gym_id, self.current_user.username, rating, comment))
        self.show_message("Успех", "Ревюто е записано!")

    def recommend_gyms(self):
        location = simpledialog.askstring("Препоръки", "Локация:")
        results = [g for g in self.nearby_gyms if location.lower() in g.location.lower()]
        sorted_gyms = sorted(results, key=lambda g: g.rating, reverse=True)
        text = "\n".join([f"{g.name} - {g.rating}/5" for g in sorted_gyms])
        self.show_message("Препоръки", text if text else "Няма препоръки.")

    def add_gym(self):
        if not self.current_user or self.current_user.role != "admin":
            self.show_message("Достъп отказан", "Само администратори!")
            return
        name = simpledialog.askstring("Добавяне", "Име:")
        address = simpledialog.askstring("Добавяне", "Адрес:")
        location = simpledialog.askstring("Добавяне", "Локация:")
        new_id = max([g.id for g in self.nearby_gyms], default=0) + 1
        self.nearby_gyms.append(Gym(new_id, name, address, location=location))
        self.show_message("Успех", f"Добавен е фитнес: {name}")

    def edit_gym(self):
        if not self.current_user or self.current_user.role != "admin":
            self.show_message("Достъп отказан", "Само администратори!")
            return
        gym_id = simpledialog.askinteger("Редакция", "ID на фитнес:")
        gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
        if not gym:
            self.show_message("Грешка", "Фитнесът не е намерен.")
            return
        new_name = simpledialog.askstring("Редакция", f"Ново име (сега: {gym.name}):")
        if new_name:
            gym.name = new_name
        self.show_message("Успех", f"Редактиран: {gym.name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessAppGUI(root)
    root.mainloop()
