
import tkinter as tk
from tkinter import messagebox, simpledialog

class Gym:
    def __init__(self, id, name, address, rating=0.0, services=None, opening_hours="", price="", location=""):
        self.id = id
        self.name = name
        self.address = address
        self.rating = rating
        self.services = services or []
        self.opening_hours = opening_hours
        self.price = price
        self.location = location

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

        self.gyms = [
            Gym(1, "Power Gym", "123 Main St", 4.5, ["Кардио", "Йога"], "7:00-22:00", "40 лв", "София"),
            Gym(2, "Fit Life", "456 Oak Ave", 4.2, ["Фитнес", "Спининг"], "6:00-23:00", "35 лв", "Пловдив"),
        ]
        self.users = []
        self.reviews = []
        self.favorites = []
        self.current_user = None

        self.menu_ui()

    def menu_ui(self):
        self.clear()
        tk.Label(self.root, text="Добре дошли във Фитнес Приложението!", font=("Arial", 14)).pack(pady=10)

        options = [
            ("Вход / Регистрация", self.login_or_register),
            ("Преглед на фитнеси", self.view_gyms),
            ("Търсене на фитнес", self.search_gyms),
            ("Любими фитнеси", self.view_favorites),
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

    def login_or_register(self):
        choice = simpledialog.askinteger("Опция", "1 - Регистрация\n2 - Вход")
        if choice == 1:
            self.register()
        elif choice == 2:
            self.login()

    def register(self):
        username = simpledialog.askstring("Регистрация", "Потребителско име:")
        email = simpledialog.askstring("Регистрация", "Имейл:")
        password = simpledialog.askstring("Регистрация", "Парола:")
        role = simpledialog.askstring("Роля (guest/subscribed/admin):", initialvalue="guest")
        if any(u.username == username for u in self.users):
            messagebox.showerror("Грешка", "Потребителското име вече съществува.")
            return
        self.current_user = User(username, email, password, role)
        self.users.append(self.current_user)
        messagebox.showinfo("Успешно", f"Регистриран като {role}")

    def login(self):
        username = simpledialog.askstring("Вход", "Потребителско име:")
        password = simpledialog.askstring("Вход", "Парола:")
        user = next((u for u in self.users if u.username == username and u.password == password), None)
        if user:
            self.current_user = user
            messagebox.showinfo("Успешно", f"Влязохте като {user.role}")
        else:
            messagebox.showerror("Грешка", "Невалидни данни.")

    def view_gyms(self):
        text = "\n".join([f"{g.id}. {g.name} - {g.address} ({g.rating}/5)" for g in self.gyms])
        messagebox.showinfo("Фитнеси", text)

    def search_gyms(self):
        keyword = simpledialog.askstring("Търсене", "Въведи име или услуга:").lower()
        results = [g for g in self.gyms if keyword in g.name.lower() or any(keyword in s.lower() for s in g.services)]
        if results:
            text = "\n".join([f"{g.name} - {g.address}, Услуги: {', '.join(g.services)}" for g in results])
        else:
            text = "Няма съвпадения."
        messagebox.showinfo("Резултати", text)

    def view_favorites(self):
        if not self.current_user:
            messagebox.showerror("Грешка", "Моля, влезте в профила си.")
            return
        favs = [g for g in self.favorites if g["user"] == self.current_user.username]
        if not favs:
            messagebox.showinfo("Любими", "Нямате любими фитнеси.")
            return
        text = "\n".join([f"{g['gym'].name} - {g['gym'].address}" for g in favs])
        messagebox.showinfo("Любими фитнеси", text)

    def add_review(self):
        if not self.current_user or self.current_user.role not in ["subscribed", "admin"]:
            messagebox.showerror("Грешка", "Само абонирани потребители могат да пишат ревюта.")
            return
        gym_id = simpledialog.askinteger("Ревю", "ID на фитнес:")
        gym = next((g for g in self.gyms if g.id == gym_id), None)
        if not gym:
            messagebox.showerror("Грешка", "Фитнесът не съществува.")
            return
        rating = simpledialog.askinteger("Оценка", "Оценка (1-5):")
        comment = simpledialog.askstring("Коментар", "Коментар (по избор):")
        self.reviews.append(Review(gym_id, self.current_user.username, rating, comment))
        messagebox.showinfo("Успех", "Ревюто е записано.")

    def view_reviews(self):
        if not self.reviews:
            messagebox.showinfo("Ревюта", "Няма налични ревюта.")
            return
        text = "\n\n".join([f"Фитнес ID: {r.gym_id}, {r.rating}/5 - {r.comment or 'Без коментар'}" for r in self.reviews])
        messagebox.showinfo("Ревюта", text)

    def recommend_gyms(self):
        location = simpledialog.askstring("Препоръки", "Локация:")
        filtered = [g for g in self.gyms if g.location.lower() == location.lower()]
        sorted_gyms = sorted(filtered, key=lambda g: g.rating, reverse=True)
        if sorted_gyms:
            text = "\n".join([f"{g.name} - {g.rating}/5, {g.price}" for g in sorted_gyms])
        else:
            text = "Няма препоръки за тази локация."
        messagebox.showinfo("Препоръки", text)

    def add_gym(self):
        if not self.current_user or self.current_user.role != "admin":
            messagebox.showerror("Грешка", "Само администратор може да добавя фитнеси.")
            return
        name = simpledialog.askstring("Фитнес", "Име:")
        address = simpledialog.askstring("Фитнес", "Адрес:")
        rating = simpledialog.askfloat("Фитнес", "Рейтинг:")
        services = simpledialog.askstring("Фитнес", "Услуги (разделени със запетая):").split(",")
        hours = simpledialog.askstring("Фитнес", "Работно време:")
        price = simpledialog.askstring("Фитнес", "Цена:")
        location = simpledialog.askstring("Фитнес", "Локация:")
        new_id = max([g.id for g in self.gyms], default=0) + 1
        self.gyms.append(Gym(new_id, name, address, rating, services, hours, price, location))
        messagebox.showinfo("Успешно", "Фитнесът е добавен.")

    def edit_gym(self):
        if not self.current_user or self.current_user.role != "admin":
            messagebox.showerror("Грешка", "Само администратор може да редактира.")
            return
        gym_id = simpledialog.askinteger("Редакция", "ID на фитнес:")
        gym = next((g for g in self.gyms if g.id == gym_id), None)
        if not gym:
            messagebox.showerror("Грешка", "Фитнесът не съществува.")
            return
        gym.name = simpledialog.askstring("Име", f"Име ({gym.name}):") or gym.name
        gym.address = simpledialog.askstring("Адрес", f"Адрес ({gym.address}):") or gym.address
        gym.price = simpledialog.askstring("Цена", f"Цена ({gym.price}):") or gym.price
        messagebox.showinfo("Успешно", "Фитнесът е редактиран.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessAppGUI(root)
    root.mainloop()
