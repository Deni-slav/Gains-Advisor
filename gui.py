import tkinter as tk
from tkinter import messagebox, simpledialog
from gym_management import GymManager
from user_management import UserManager
from review_management import ReviewManager

class FitnessAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Фитнес Приложение")

        self.gym_manager = GymManager()
        self.user_manager = UserManager()
        self.review_manager = ReviewManager()
        self.favorite_gyms = []

        self.menu_ui()

    def menu_ui(self):
        tk.Label(self.root, text="Добре дошли във Фитнес Приложението!", font=("Arial", 14)).pack(pady=10)

        options = [
            ("Вход / Регистрация", self.handle_registration_login),
            ("Моят профил", self.show_user_profile),
            ("Преглед на фитнеси", self.view_gyms),
            ("Търсене на фитнес", self.search_gyms),
            ("Любими фитнеси", self.handle_favorite_gyms),
            ("Преглед на ревюта", self.view_reviews),
            ("Добавяне на ревю", self.add_review),
            ("Препоръки", self.recommend_gyms),
            ("Добавяне на фитнес (admin)", self.add_gym),
            ("Редактиране на фитнес (admin)", self.handle_gym_editing),
            ("Изход", self.root.quit)
        ]

        for label, action in options:
            tk.Button(self.root, text=label, width=40, command=action).pack(pady=3)

    def show_message(self, title, msg):
        messagebox.showinfo(title, msg)

    def handle_registration_login(self):
        while True:
            choice = simpledialog.askinteger(
                "Избор на действие",
                "Изберете опция:\n\n1 - Регистрация на нов потребител\n2 - Вход за съществуващ потребител\n\nВъведете номер (1 или 2):",
                minvalue=1,
                maxvalue=2
            )
            
            if choice is None:
                return
            
            if choice in (1, 2):
                break
            
            messagebox.showerror("Грешка", "Моля, въведете валидна опция (1 или 2)!")
        
        if choice == 1:
            self.user_manager.register()
        else:
            self.user_manager.login()

    def view_gyms(self):
        text = "\n".join([f"{g.id}. {g.name} - {g.address} ({g.rating}/5)" for g in self.gym_manager.nearby_gyms])
        messagebox.showinfo("Фитнеси", text)

    def handle_favorite_gyms(self):
        while True:
            choice = simpledialog.askinteger(
                "Избор на действие",
                "Изберете опция:\n\n1 - Добавете фитнес към любими\n2 - Вижте списък с любими фитнеси\n\nВъведете номер (1 или 2):",
                minvalue=1,
                maxvalue=2
            )
            
            if choice is None:
                return
            
            if choice in (1, 2):
                break
            
            messagebox.showerror("Грешка", "Моля, въведете валидна опция (1 или 2)!")
        
        if choice == 1:
            self.add_favourite_gyms()
        else:
            self.view_favorite_gyms()

    def add_favourite_gyms(self):
        if not self.user_manager.current_user:
            messagebox.showerror("Грешка", "Трябва да влезете в системата, за да добавяте към любими.")
            return

        gyms_text = "\n".join([f"{g.id}. {g.name} - {g.address} (Рейтинг: {g.rating})" 
                            for g in self.gym_manager.nearby_gyms])
        messagebox.showinfo("Фитнеси в близост", gyms_text)

        while True:
            gym_id = simpledialog.askinteger("Добавяне към любими", 
                                        "Въведете ID на фитнеса за добавяне (или 0 за отказ):",
                                        minvalue=0)
            if gym_id is None or gym_id == 0:
                return
                
            gym = next((g for g in self.gym_manager.nearby_gyms if g.id == gym_id), None)
            
            if not gym:
                messagebox.showerror("Грешка", f"Не е намерен фитнес с ID {gym_id}!")
                continue
                
            if any(f.id == gym.id for f in self.favorite_gyms):
                messagebox.showerror("Информация", f"{gym.name} вече е във вашите любими!")
                continue
                
            self.favorite_gyms.append(gym)
            messagebox.showinfo("Успех", 
                            f"{gym.name} е добавен към любими!\n\n"
                            f"Адрес: {gym.address}\n"
                            f"Рейтинг: {gym.rating}\n"
                            f"Локация: {gym.location}\n"
                            f"Цена: {gym.price}")
            return

    def view_favorite_gyms(self):
        if not self.user_manager.current_user:
            messagebox.showerror("Грешка", "Трябва да влезете в системата, за да видите любимите си фитнеси!")
            return
        
        if not isinstance(self.favorite_gyms, list):
            messagebox.showerror("Грешка", "Невалидни данни за любими фитнеси!")
            return
            
        if len(self.favorite_gyms) == 0:
            messagebox.showinfo("Любими фитнеси", "Все още нямате добавени любими фитнеси.")
            return
        
        gyms_text = []
        for gym in self.favorite_gyms:
            gym_info = (
                f"Име: {gym.name}\n"
                f"Адрес: {gym.address}\n"
                f"Локация: {gym.location}\n"
                f"Рейтинг: {gym.rating}/5.0\n"
                f"Цена: {gym.price}\n"
                f"Работно време: {gym.opening_hours}\n"
                f"Услуги: {', '.join(gym.services)}\n"
                f"{'-'*30}"
            )
            gyms_text.append(gym_info)
        
        if not gyms_text:
            messagebox.showinfo("Любими фитнеси", "Няма валидни любими фитнеси.")
            return
        
        header = f"Вашите любими фитнеси ({len(gyms_text)} общо):\n\n"
        messagebox.showinfo("Любими фитнеси", header + "\n".join(gyms_text))

    def search_gyms(self):
        keyword = simpledialog.askstring("Търсене на фитнес", 
                                    "Въведете ключова дума за търсене\n(име, услуга или локация):")
        
        if not keyword or not keyword.strip():
            messagebox.showerror("Грешка", "Моля, въведете ключова дума за търсене!")
            return
            
        results = self.gym_manager.search_gyms(keyword)
        
        if not results:
            messagebox.showinfo("Резултати от търсене", 
                            f"Няма намерени фитнеси за '{keyword}'.")
            return
            
        results_text = "\n\n".join([
            f"Име: {g.name}\n"
            f"Адрес: {g.address}\n"
            f"Рейтинг: {g.rating}\n"
            f"Работно време: {g.opening_hours}\n"
            f"Цена: {g.price}\n"
            f"Услуги: {', '.join(g.services)}"
            for g in results
        ])
        
        header = f"Намерени фитнеси ({len(results)}):\n\n"
        messagebox.showinfo(f"Резултати за '{keyword}'", header + results_text)

    def view_reviews(self):
        self.review_manager.view_reviews(self.gym_manager)

    def add_review(self):
        self.review_manager.add_review(self.user_manager.current_user, self.gym_manager)

    def recommend_gyms(self):
        location = simpledialog.askstring(
            "Препоръки за фитнеси",
            "Въведете локация (град/район) за препоръки:\n\n"
            "Пример: 'Младост', 'Лозенец', 'Център'"
        )
        
        if not location or not location.strip():
            messagebox.showerror("Грешка", "Моля, въведете локация за търсене!")
            return
            
        results = self.gym_manager.recommend_gyms(location)
        
        if not results:
            messagebox.showinfo("Резултати", 
                            f"Няма намерени фитнеси в локация '{location}'.\n\n"
                            f"Опитайте с друга локация или проверете дали има правописна грешка.")
            return
            
        message = [
            f"Топ препоръки за {location}:\n",
            *[
                f"{i+1}. {g.name}\n"
                f"Рейтинг: {g.rating}/5\n"
                f"Цена: {g.price}\n"
                f"Адрес: {g.address}\n"
                for i, g in enumerate(results[:5])
            ],
            f"\nНамерени общо {len(results)} фитнеса."
        ]
        
        messagebox.showinfo(
            f"Резултати за {location}",
            "\n".join(message),
            detail="Можете да използвате филтри за по-точни резултати."
        )

    def add_gym(self):
        self.gym_manager.add_gym(self.user_manager.current_user)

    def handle_gym_editing(self):
        if not self.user_manager.current_user or self.user_manager.current_user.role != "admin":
            messagebox.showerror("Достъп отказан", "Само администратори могат да редактират или изтриват фитнеси.")
            return

        while True:
            choice = simpledialog.askinteger(
                "Избор на действие",
                "Изберете опция:\n\n1 - Редактиране на фитнес\n2 - Изтриване на фитнес\n\nВъведете номер (1 или 2):",
                minvalue=1,
                maxvalue=2
            )
            
            if choice is None:
                return
            
            if choice in (1, 2):
                break
            
            messagebox.showerror("Грешка", "Моля, въведете валидна опция (1 или 2)!")
        
        if choice == 1:
            self.gym_manager.edit_gym(self.user_manager.current_user)
        else:
            self.gym_manager.remove_gym(self.user_manager.current_user)

    def show_user_profile(self):
        if not self.user_manager.current_user:
            messagebox.showerror("Грешка", "Трябва да влезете в системата, за да видите профила си!")
            return

        user = self.user_manager.current_user
        profile_info = (
            f"Потребителски профил:\n\n"
            f"Потребителско име: {user.username}\n"
            f"Имейл: {user.email}\n"
            f"Роля: {user.role}\n"
            f"Пълно име: {user.full_name}\n"
            f"Брой любими зали: {len(self.favorite_gyms)}"
        )
        
        messagebox.showinfo("Моят профил", profile_info) 