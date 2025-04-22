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
            Gym(1, "Power Gym", "123 Main St", 4.5, 
                services=["Кардио", "Силови тренировки", "Йога", "Пилатес", "Персонални треньори"],
                opening_hours="Понеделник-Петък: 06:00-23:00, Събота-Неделя: 08:00-22:00",
                price="50 лв/месец",
                location="Център"),
            Gym(2, "Fit Life", "456 Oak Ave", 4.2,
                services=["Кардио", "Групови класове", "Бокс", "Кросфит", "Спа зона"],
                opening_hours="Понеделник-Неделя: 00:00-24:00",
                price="45 лв/месец",
                location="Лозенец"),
            Gym(3, "Muscle World", "789 Pine Rd", 4.0,
                services=["Силови тренировки", "Кардио", "Масаж", "Персонални треньори"],
                opening_hours="Понеделник-Петък: 07:00-22:00, Събота: 09:00-20:00",
                price="40 лв/месец",
                location="Младост"),
            Gym(4, "Elite Fitness", "321 Sports Blvd", 4.8,
                services=["Кардио", "Силови тренировки", "Йога", "Пилатес", "Танци", "Басейн", "Сауна"],
                opening_hours="Понеделник-Неделя: 06:00-24:00",
                price="80 лв/месец",
                location="Витоша"),
            Gym(5, "CrossFit Zone", "555 Athlete St", 4.6,
                services=["Кросфит", "Кардио", "Силови тренировки", "Групови класове"],
                opening_hours="Понеделник-Петък: 07:00-21:00, Събота: 09:00-15:00",
                price="70 лв/месец",
                location="Студентски град"),
            Gym(6, "Wellness Center", "888 Health Ave", 4.7,
                services=["Кардио", "Йога", "Пилатес", "Масаж", "Спа", "Басейн", "Сауна", "Джакузи"],
                opening_hours="Понеделник-Неделя: 06:00-23:00",
                price="90 лв/месец",
                location="Бояна"),
            Gym(7, "Sport Complex", "444 Olympic Rd", 4.4,
                services=["Кардио", "Силови тренировки", "Тенис", "Басейн", "Баскетбол", "Волейбол"],
                opening_hours="Понеделник-Петък: 08:00-22:00, Събота-Неделя: 09:00-20:00",
                price="60 лв/месец",
                location="Надежда"),
            Gym(8, "Fitness Studio", "777 Workout St", 4.3,
                services=["Кардио", "Йога", "Пилатес", "Танци", "Персонални треньори"],
                opening_hours="Понеделник-Петък: 07:00-22:00, Събота: 09:00-18:00",
                price="55 лв/месец",
                location="Овча купел")
        ]
        self.registered_users = []
        self.gym_reviews = []
        self.current_user = None

        self.menu_ui()

    def menu_ui(self):

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
            ("Редактиране на фитнес (admin)", self.handle_gym_editing),
            ("Изход", self.root.quit)
        ]

        for label, action in options:
            tk.Button(self.root, text=label, width=40, command=action).pack(pady=3)


    def show_message(self, title, msg):
        messagebox.showinfo(title, msg)

    def handle_registration_login(self):
        while True:  # Цикъл за повторен опит при невалиден вход
            choice = simpledialog.askinteger(
                "Избор на действие",
                "Изберете опция:\n\n1 - Регистрация на нов потребител\n2 - Вход за съществуващ потребител\n\nВъведете номер (1 или 2):",
                minvalue=1,
                maxvalue=2
            )
            
            # Проверка за отказ от потребителя (Cancel)
            if choice is None:
                return  # Излизаме от метода
            
            # Проверка за валиден избор
            if choice in (1, 2):
                break  # Валиден избор, излизаме от цикъла
            
            messagebox.showerror("Грешка", "Моля, въведете валидна опция (1 или 2)!")
        
        # Изпълняваме съответния метод
        if choice == 1:
            self.register()
        else:
            self.login_user()

    def register(self):
        VALID_ROLES = ['guest', 'subscribed', 'admin']

        while True:
            username = simpledialog.askstring("Регистрация", "Потребителско име (мин. 4 символа):")
            if username is None:
                return
            username = username.strip()
            if len(username) < 4:
                messagebox.showerror("Грешка", "Минимална дължина на потребителското име е 4 символа.")
                continue
            if any(u.username == username for u in self.registered_users):
                messagebox.showerror("Грешка", "Потребителското име вече съществува.")
                continue
            break

        while True:
            email = simpledialog.askstring("Регистрация", "Имейл:")
            if email is None or '@' not in email or '.' not in email:
                messagebox.showerror("Грешка", "Моля, въведете валиден имейл.")
                continue
            if any(u.email == email for u in self.registered_users):
                messagebox.showerror("Грешка", "Имейл адресът вече е използван.")
                continue
            break

        while True:
            password = simpledialog.askstring("Регистрация", "Парола (мин. 6 символа):", show='*')
            if password is None or len(password) < 6:
                messagebox.showerror("Грешка", "Паролата трябва да е поне 6 символа.")
                continue
            break

        while True:
            role = simpledialog.askstring("Регистрация", "Роля (guest/subscribed/admin):", initialvalue="guest")
            if role is None:
                return
            role = role.strip().lower()
            if role not in VALID_ROLES:
                messagebox.showerror("Грешка", f"Невалидна роля. Позволени: {', '.join(VALID_ROLES)}")
                continue
            if role == "admin" and "admin" not in username.lower():
                messagebox.showerror("Грешка", "Само потребители с 'admin' в потребителското име могат да бъдат администратори.")
                continue
            break

        new_user = User(username, email, password, role)
        self.registered_users.append(new_user)
        self.current_user = new_user

        messagebox.showinfo("Успешна регистрация", f"Регистриран потребител: {username}\nРоля: {role}")

    def login_user(self):
        while True:
            username = simpledialog.askstring("Вход в системата", "Потребителско име (задължително):")
            if username is None:  
                return
                
            if not username or not username.strip():
                self.show_message("Грешка", "Моля, въведете потребителско име!")
                continue
                
            password = simpledialog.askstring("Вход в системата", "Парола (задължително):", show='*')
            if password is None:  
                return
                
            if not password:
                self.show_message("Грешка", "Моля, въведете парола!")
                continue
                
            user = next((u for u in self.registered_users 
                        if u.username == username.strip() 
                        and u.password == password), None)
                        
            if user:
                self.current_user = user
                self.show_message("Успешен вход", 
                            f"Добре дошли, {user.username}!\n"
                            f"Роля: {user.role}\n"
                            f"Имейл: {user.email}")
                return
            else:
                self.show_message("Грешка", "Невалидно потребителско име или парола!")
                continue

    def view_gyms(self):
        text = "\n".join([f"{g.id}. {g.name} - {g.address} ({g.rating}/5)" for g in self.nearby_gyms])
        messagebox.showinfo("Фитнеси", text)

    def handle_favorite_gyms(self):
            while True:  # Цикъл за повторен опит при невалиден вход
                choice = simpledialog.askinteger(
                    "Избор на действие",
                    "Изберете опция:\n\n1 - Добавете фитнес към любими\n2 - Виште списък с любими фитнеси\n\nВъведете номер (1 или 2):",
                    minvalue=1,
                    maxvalue=2
                )
                
                # Проверка за отказ от потребителя (Cancel)
                if choice is None:
                    return  # Излизаме от метода
                
                # Проверка за валиден избор
                if choice in (1, 2):
                    break  # Валиден избор, излизаме от цикъла
                
                messagebox.showerror("Грешка", "Моля, въведете валидна опция (1 или 2)!")
            
            # Изпълняваме съответния метод
            if choice == 1:
                self.add_favourite_gyms()
            else:
                self.view_favorite_gyms()

    def add_favourite_gyms(self):
        # Показване на списък с фитнеси
        gyms_text = "\n".join([f"{g.id}. {g.name} - {g.address} (Рейтинг: {g.rating})" 
                            for g in self.nearby_gyms])
        self.show_message("Фитнеси в близост", gyms_text)

        # Добавяне към любими (ако потребителят е влязъл в системата)
        if not self.current_user:
            self.show_message("Информация", "Трябва да влезете в системата, за да добавяте към любими.")
            return
            
        while True:
            gym_id = simpledialog.askinteger("Добавяне към любими", 
                                        "Въведете ID на фитнеса за добавяне (или 0 за отказ):",
                                        minvalue=0)
            if gym_id is None or gym_id == 0:  # Потребителят натисна Cancel или въведе 0
                return
                
            # Проверка за валиден ID
            gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
            
            if not gym:
                self.show_message("Грешка", f"Не е намерен фитнес с ID {gym_id}!")
                continue
                
            # Check if gym is already in favorites
            if any(f.id == gym.id for f in self.favorite_gyms):
                self.show_message("Информация", f"{gym.name} вече е във вашите любими!")
                continue
                
            # Добавяне към любими
            self.favorite_gyms.append(gym)
            self.show_message("Успех", 
                            f"{gym.name} е добавен към любими!\n\n"
                            f"Адрес: {gym.address}\n"
                            f"Рейтинг: {gym.rating}\n"
                            f"Локация: {gym.location}\n"
                            f"Цена: {gym.price}")
            return

    def view_favorite_gyms(self):
        if not self.current_user:
            self.show_message("Грешка", "Трябва да влезете в системата, за да видите любимите си фитнеси!")
            return
        
        if not isinstance(self.favorite_gyms, list):
            self.show_message("Грешка", "Невалидни данни за любими фитнеси!")
            return
            
        if len(self.favorite_gyms) == 0:
            self.show_message("Любими фитнеси", "Все още нямате добавени любими фитнеси.")
            return
        
        # Create a detailed display of favorite gyms
        gyms_text = []
        for gym in self.favorite_gyms:
            if not isinstance(gym, Gym):
                continue
                
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
            self.show_message("Любими фитнеси", "Няма валидни любими фитнеси.")
            return
        
        header = f"Вашите любими фитнеси ({len(gyms_text)} общо):\n\n"
        self.show_message("Любими фитнеси", header + "\n".join(gyms_text))

    def search_gyms(self):
        if not self.nearby_gyms or not isinstance(self.nearby_gyms, list):
            self.show_message("Грешка", "Няма налични фитнеси за търсене.")
            return

        while True:
            keyword = simpledialog.askstring("Търсене на фитнес", 
                                        "Въведете ключова дума за търсене\n(име, услуга или локация):")
            
            if keyword is None:  
                return
                
            if not keyword or not keyword.strip():
                self.show_message("Грешка", "Моля, въведете ключова дума за търсене!")
                continue
                
            keyword = keyword.strip().lower()
            break

        valid_results = []
        for gym in self.nearby_gyms:
            try:
                if not isinstance(gym, Gym):
                    continue
                    
                name = getattr(gym, 'name', '').lower()
                address = getattr(gym, 'address', '').lower()
                services = getattr(gym, 'services', [])
                location = getattr(gym, 'location', '').lower()
                
                if (keyword in name or 
                    keyword in address or 
                    keyword in location or
                    any(keyword in s.lower() for s in services if isinstance(s, str))):
                    valid_results.append(gym)
            except Exception:
                continue  

        if not valid_results:
            self.show_message("Резултати от търсене", 
                            f"Няма намерени фитнеси за '{keyword}'.")
            return
            
        results_text = "\n\n".join([
            f" Име: {g.name}\n"
            f" Адрес: {g.address}\n"
            f" Рейтинг: {getattr(g, 'rating', 'няма')}\n"
            f"Работно време: {getattr(g, 'opening_hours', 'няма информация')}\n"
            f" Цена: {getattr(g, 'price', 'няма информация')}\n"
            f" Услуги: {', '.join(getattr(g, 'services', []))}"
            for g in valid_results
        ])
        
        header = f"Намерени фитнеси ({len(valid_results)}):\n\n"
        self.show_message(f"Резултати за '{keyword}'", header + results_text)

    def view_reviews(self):
        if not self.gym_reviews:
            messagebox.showinfo("Ревюта", "Няма налични ревюта.")
            return
            
        reviews_text = []
        for review in self.gym_reviews:
            gym = next((g for g in self.nearby_gyms if g.id == review.gym_id), None)
            if gym:
                review_text = (
                    f"Фитнес: {gym.name}\n"
                    f"Оценка: {review.rating}/5\n"
                    f"Коментар: {review.comment or 'Без коментар'}\n"
                    f"Потребител: {review.user_id}\n"
                    f"{'-'*30}"
                )
                reviews_text.append(review_text)
        
        if reviews_text:
            messagebox.showinfo("Ревюта", "\n".join(reviews_text))
        else:
            messagebox.showinfo("Ревюта", "Няма налични ревюта.")

    def admin_panel(self):
        if not self.current_user or self.current_user.role != "admin":
            self.show_message("Достъп отказан", "Само администратори имат достъп до тази секция.")
            return

        options = [
            ("Добави фитнес", self.add_gym),
            ("Редактирай фитнес", self.edit_gym),
            ("Назад", lambda: None)
        ]

        for label, command in options:
            tk.Button(self.root, text=label, command=command).pack(pady=2)

    def add_review(self):
        if not self.current_user:
            messagebox.showerror("Грешка", "Трябва да влезете в системата, за да пишете ревюта.")
            return
            
        if self.current_user.role not in ["subscribed", "admin"]:
            messagebox.showerror("Грешка", "Само абонирани потребители и администратори могат да пишат ревюта.")
            return

        # Show available gyms first
        gyms_text = "\n".join([f"{g.id}. {g.name} - {g.address}" for g in self.nearby_gyms])
        messagebox.showinfo("Налични фитнеси", gyms_text)

        while True:
            try:
                gym_id = simpledialog.askinteger("Ревю", "Въведете ID на фитнес за ревю:")
                if gym_id is None:  
                    return
                    
                if not isinstance(gym_id, int) or gym_id <= 0:
                    messagebox.showerror("Грешка", "ID на фитнес трябва да бъде положително число!")
                    continue
                    
                gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
                if not gym:
                    messagebox.showerror("Грешка", f"Не е намерен фитнес с ID {gym_id}!")
                    continue
                    
                # Check if user already reviewed this gym
                existing_review = next((r for r in self.gym_reviews 
                                     if r.gym_id == gym_id and r.user_id == self.current_user.username), None)
                if existing_review:
                    messagebox.showerror("Грешка", "Вече сте написали ревю за този фитнес!")
                    return
                    
                break
            except ValueError:
                messagebox.showerror("Грешка", "Моля, въведете валиден номер на фитнес!")
                continue

        while True:
            try:
                rating = simpledialog.askinteger("Оценка", "Дайте оценка (1-5 звезди):", 
                                            minvalue=1, maxvalue=5)
                if rating is None:  
                    return
                    
                if not 1 <= rating <= 5:
                    messagebox.showerror("Грешка", "Оценката трябва да бъде между 1 и 5!")
                    continue
                    
                break
            except ValueError:
                messagebox.showerror("Грешка", "Моля, въведете число между 1 и 5!")
                continue

        comment = None
        while True:
            comment_input = simpledialog.askstring("Коментар", 
                                                "Добавете коментар (по избор, максимум 200 символа):\n\n"
                                                "Можете да пропуснете с Cancel.")
            if comment_input is None:  
                break
                
            comment = comment_input.strip()
            if len(comment) > 200:
                messagebox.showerror("Грешка", "Коментарът не може да бъде по-дълъг от 200 символа!")
                continue
                
            break

        # Create and add the review
        new_review = Review(
            gym_id=gym_id,
            user_id=self.current_user.username,
            rating=rating,
            comment=comment
        )
        self.gym_reviews.append(new_review)
        
        # Update gym rating
        gym_reviews = [r for r in self.gym_reviews if r.gym_id == gym_id]
        if gym_reviews:
            gym.rating = sum(r.rating for r in gym_reviews) / len(gym_reviews)
        
        confirmation_msg = (
            "Ревюто е записано успешно!\n\n"
            f"Фитнес: {gym.name}\n"
            f"Оценка: {rating}/5\n"
        )
        if comment:
            confirmation_msg += f"Коментар: {comment[:50]}..." if len(comment) > 50 else f"Коментар: {comment}"
        
        messagebox.showinfo("Успешно добавено ревю", confirmation_msg)

    def add_gym(self):
        if self.current_user and self.current_user.role == "admin":
            while True:
                name = simpledialog.askstring("Добави фитнес", "Име:")
                if not name or not name.strip():
                    messagebox.showerror("Грешка", "Името не може да бъде празно!")
                    continue
                break
            
            # Валидация за адрес
            while True:
                address = simpledialog.askstring("Добави фитнес", "Адрес:")
                if not address or not address.strip():
                    messagebox.showerror("Грешка", "Адресът не може да бъде празен!")
                    continue
                break
            
            # Валидация за локация
            while True:
                location = simpledialog.askstring("Добави фитнес", "Локация (град/район):")
                if not location or not location.strip():
                    messagebox.showerror("Грешка", "Локацията не може да бъде празна!")
                    continue
                break
            
            # Валидация за рейтинг
            while True:
                rating_input = simpledialog.askstring("Добави фитнес", "Рейтинг (0.0-5.0, по избор):")
                if not rating_input:
                    rating = 0.0
                    break
                try:
                    rating = float(rating_input)
                    if not 0.0 <= rating <= 5.0:
                        messagebox.showerror("Грешка", "Рейтингът трябва да е между 0.0 и 5.0!")
                        continue
                    break
                except ValueError:
                    messagebox.showerror("Грешка", "Моля, въведете валидно число (напр. 4.5)!")
                    continue
            
            # Валидация за услуги
            while True:
                services_input = simpledialog.askstring("Добави фитнес", "Услуги (разделени със запетая):")
                if not services_input or not services_input.strip():
                    messagebox.showerror("Грешка", "Трябва да въведете поне една услуга!")
                    continue
                
                services = [s.strip() for s in services_input.split(",") if s.strip()]
                if not services:
                    messagebox.showerror("Грешка", "Трябва да въведете валидни услуги!")
                    continue
                break
            
            # Валидация за работно време
            while True:
                opening_hours = simpledialog.askstring("Добави фитнес", "Работно време:")
                if not opening_hours or not opening_hours.strip():
                    messagebox.showerror("Грешка", "Работното време не може да бъде празно!")
                    continue
                break
            
            # Валидация за цена
            while True:
                price = simpledialog.askstring("Добави фитнес", "Цена:")
                if not price or not price.strip():
                    messagebox.showerror("Грешка", "Цената не може да бъде празна!")
                    continue
                break
        
            # Създаване на новия фитнес
            new_id = max([g.id for g in self.nearby_gyms], default=0) + 1
            new_gym = Gym(
                id=new_id,
                name=name.strip(),
                address=address.strip(),
                rating=rating,
                services=services,
                opening_hours=opening_hours.strip(),
                price=price.strip(),
                location=location.strip()
            )
        
            self.nearby_gyms.append(new_gym)
            messagebox.showinfo("Успех", 
                f"Успешно добавен фитнес:\n\n"
                f"Име: {new_gym.name}\n"
                f"ID: {new_gym.id}\n"
                f"Адрес: {new_gym.address}\n"
                f"Рейтинг: {new_gym.rating}/5.0")
        else:
            messagebox.showerror("Само хора с админски права могат да достъпят тази функционалност")

    def edit_gym(self):
        if not self.current_user or self.current_user.role != "admin":
            self.show_message("Достъп отказан", "Само администратори могат да редактират или изтриват фитнеси.")
            return

        while True:
            try:
                gym_id = simpledialog.askinteger("Редактиране на фитнес", "Въведете ID на фитнеса за редактиране:")
                if gym_id is None:  
                    return
                if gym_id <= 0:
                    messagebox.showerror("Грешка", "ID трябва да бъде положително число!")
                    continue
                break
            except:
                messagebox.showerror("Грешка", "Моля, въведете валиден номер на ID!")
                continue

        gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
        if not gym:
            messagebox.showerror("Грешка", f"Не е намерен фитнес с ID {gym_id}!")
            return

        while True:
            new_name = simpledialog.askstring("Редактиране на име", 
                                        f"Текущо име: {gym.name}\nНово име:", 
                                        initialvalue=gym.name)
            if new_name is None:  
                return
            if new_name.strip():
                gym.name = new_name.strip()
                break
            messagebox.showerror("Грешка", "Името не може да бъде празно!")

        while True:
            new_address = simpledialog.askstring("Редактиране на адрес", 
                                            f"Текущ адрес: {gym.address}\nНов адрес:", 
                                            initialvalue=gym.address)
            if new_address is None:
                return
            if new_address.strip():
                gym.address = new_address.strip()
                break
            messagebox.showerror("Грешка", "Адресът не може да бъде празен!")

        while True:
            new_location = simpledialog.askstring("Редактиране на локация", 
                                            f"Текуща локация: {gym.location}\nНова локация:", 
                                            initialvalue=gym.location)
            if new_location is None:
                return
            if new_location.strip():
                gym.location = new_location.strip()
                break
            messagebox.showerror("Грешка", "Локацията не може да бъде празна!")

        while True:
            new_hours = simpledialog.askstring("Редактиране на работно време", 
                                            f"Текущо работно време: {gym.opening_hours}\nНово работно време:", 
                                            initialvalue=gym.opening_hours)
            if new_hours is None:
                return
            if new_hours.strip():
                gym.opening_hours = new_hours.strip()
                break
            messagebox.showerror("Грешка", "Работното време не може да бъде празно!")

        while True:
            new_price = simpledialog.askstring("Редактиране на цена", 
                                            f"Текуща цена: {gym.price}\nНова цена:", 
                                            initialvalue=gym.price)
            if new_price is None:
                return
            if new_price.strip():
                gym.price = new_price.strip()
                break
            messagebox.showerror("Грешка", "Цената не може да бъде празна!")

        while True:
            current_services = ", ".join(gym.services)
            new_services = simpledialog.askstring("Редактиране на услуги", 
                                            f"Текущи услуги: {current_services}\nНови услуги (разделени със запетая):", 
                                            initialvalue=current_services)
            if new_services is None:
                return
            if new_services.strip():
                services_list = [s.strip() for s in new_services.split(",") if s.strip()]
                if services_list:
                    gym.services = services_list
                    break
            messagebox.showerror("Грешка", "Трябва да въведете поне една услуга!")

        messagebox.showinfo("Успех", f"Фитнес {gym.name} беше успешно редактиран!")

    def remove_gym(self):
        if not self.current_user or self.current_user.role != "admin":
            self.show_message("Достъп отказан", "Само администратори могат да изтриват фитнеси.")
            return

        try:
            gym_id = simpledialog.askinteger("Изтриване на фитнес", "Въведете ID на фитнеса за изтриване:")
            if gym_id is None:
                return

            gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
            if not gym:
                self.show_message("Грешка", f"Фитнес с ID {gym_id} не е намерен.")
                return

            confirm = messagebox.askyesno("Потвърждение", f"Наистина ли искате да изтриете {gym.name}?")
            if confirm:
                self.nearby_gyms.remove(gym)
                self.show_message("Успешно", f"Фитнесът '{gym.name}' е изтрит успешно.")
        except Exception as e:
            self.show_message("Грешка", f"Грешка при изтриване: {e}")

    def handle_gym_editing(self):
        if not self.current_user or self.current_user.role != "admin":
            self.show_message("Достъп отказан", "Само администратори могат да редактират или изтриват фитнеси.")
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
            self.edit_gym()
        else:
            self.remove_gym()

    def recommend_gyms(self):
    # Validate location input
        while True:
            location = simpledialog.askstring(
                "Препоръки за фитнеси",
                "Въведете локация (град/район) за препоръки:\n\n"
                "Пример: 'София', 'Лозенец', 'Варна'"
            )
            
            # Handle cancellation
            if location is None:  # User pressed Cancel
                return
                
            # Validate input
            location = location.strip()
            if not location:
                messagebox.showerror("Грешка", "Моля, въведете локация за търсене!")
                continue
                
            if len(location) < 2:
                messagebox.showerror("Грешка", "Локацията трябва да бъде поне 2 символа!")
                continue
                
            break
        
        # Filter and sort gyms with validation
        try:
            filtered = [
                g for g in self.nearby_gyms 
                if hasattr(g, 'location') and 
                isinstance(g.location, str) and 
                g.location.lower() == location.lower()
            ]
            
            # Additional validation for gym attributes
            valid_gyms = []
            for gym in filtered:
                if (hasattr(gym, 'rating') and isinstance(gym.rating, (int, float)) and
                    hasattr(gym, 'name') and isinstance(gym.name, str) and
                    hasattr(gym, 'price') and isinstance(gym.price, str)):
                    valid_gyms.append(gym)
            
            # Sort by rating (descending)
            sorted_gyms = sorted(valid_gyms, key=lambda g: g.rating, reverse=True)
            
            # Prepare output
            if not sorted_gyms:
                message = (
                    f"Няма намерени фитнеси в локация '{location}'.\n\n"
                    f"Опитайте с друга локация или проверете дали има правописна грешка."
                )
            else:
                message = [
                    f"Топ препоръки за {location}:\n",
                    *[
                        f" {i+1}. {g.name}\n"
                        f" Рейтинг: {g.rating}/5\n"
                        f" Цена: {g.price}\n"
                        f" Адрес: {getattr(g, 'address', 'няма информация')}\n"
                        for i, g in enumerate(sorted_gyms[:5])  # Show top 5 results
                    ],
                    f"\nНамерени общо {len(sorted_gyms)} фитнеса."
                ]
                message = "\n".join(message)
                
        except Exception as e:
            message = f"Възникна грешка при обработката: {str(e)}"
        
        # Show results
        messagebox.showinfo(
            f"Резултати за {location}",
            message,
            detail="Можете да използвате филтри за по-точни резултати."
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessAppGUI(root)
    root.mainloop()