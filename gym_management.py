from models import Gym
from tkinter import messagebox, simpledialog

class GymManager:
    def __init__(self):
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

    def add_gym(self, current_user):
        if not current_user or current_user.role != "admin":
            messagebox.showerror("Достъп отказан", "Само администратори могат да добавят фитнеси.")
            return

        name = simpledialog.askstring("Добави фитнес", "Име:")
        if not name or not name.strip():
            messagebox.showerror("Грешка", "Името не може да бъде празно!")
            return

        address = simpledialog.askstring("Добави фитнес", "Адрес:")
        if not address or not address.strip():
            messagebox.showerror("Грешка", "Адресът не може да бъде празен!")
            return

        location = simpledialog.askstring("Добави фитнес", "Локация (град/район):")
        if not location or not location.strip():
            messagebox.showerror("Грешка", "Локацията не може да бъде празна!")
            return

        services_input = simpledialog.askstring("Добави фитнес", "Услуги (разделени със запетая):")
        if not services_input or not services_input.strip():
            messagebox.showerror("Грешка", "Трябва да въведете поне една услуга!")
            return
        services = [s.strip() for s in services_input.split(",") if s.strip()]

        opening_hours = simpledialog.askstring("Добави фитнес", "Работно време:")
        if not opening_hours or not opening_hours.strip():
            messagebox.showerror("Грешка", "Работното време не може да бъде празно!")
            return

        price = simpledialog.askstring("Добави фитнес", "Цена:")
        if not price or not price.strip():
            messagebox.showerror("Грешка", "Цената не може да бъде празна!")
            return

        new_id = max([g.id for g in self.nearby_gyms], default=0) + 1
        new_gym = Gym(
            id=new_id,
            name=name.strip(),
            address=address.strip(),
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

    def edit_gym(self, current_user):
        if not current_user or current_user.role != "admin":
            messagebox.showerror("Достъп отказан", "Само администратори могат да редактират фитнеси.")
            return

        gym_id = simpledialog.askinteger("Редактиране на фитнес", "Въведете ID на фитнеса за редактиране:")
        if not gym_id:
            return

        gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
        if not gym:
            messagebox.showerror("Грешка", f"Не е намерен фитнес с ID {gym_id}!")
            return

        # Редактиране на различните полета
        new_name = simpledialog.askstring("Редактиране на име", f"Текущо име: {gym.name}\nНово име:", initialvalue=gym.name)
        if new_name and new_name.strip():
            gym.name = new_name.strip()

        new_address = simpledialog.askstring("Редактиране на адрес", f"Текущ адрес: {gym.address}\nНов адрес:", initialvalue=gym.address)
        if new_address and new_address.strip():
            gym.address = new_address.strip()

        new_location = simpledialog.askstring("Редактиране на локация", f"Текуща локация: {gym.location}\nНова локация:", initialvalue=gym.location)
        if new_location and new_location.strip():
            gym.location = new_location.strip()

        new_hours = simpledialog.askstring("Редактиране на работно време", f"Текущо работно време: {gym.opening_hours}\nНово работно време:", initialvalue=gym.opening_hours)
        if new_hours and new_hours.strip():
            gym.opening_hours = new_hours.strip()

        new_price = simpledialog.askstring("Редактиране на цена", f"Текуща цена: {gym.price}\nНова цена:", initialvalue=gym.price)
        if new_price and new_price.strip():
            gym.price = new_price.strip()

        current_services = ", ".join(gym.services)
        new_services = simpledialog.askstring("Редактиране на услуги", f"Текущи услуги: {current_services}\nНови услуги (разделени със запетая):", initialvalue=current_services)
        if new_services and new_services.strip():
            services_list = [s.strip() for s in new_services.split(",") if s.strip()]
            if services_list:
                gym.services = services_list

        messagebox.showinfo("Успех", f"Фитнес {gym.name} беше успешно редактиран!")

    def remove_gym(self, current_user):
        if not current_user or current_user.role != "admin":
            messagebox.showerror("Достъп отказан", "Само администратори могат да изтриват фитнеси.")
            return

        gym_id = simpledialog.askinteger("Изтриване на фитнес", "Въведете ID на фитнеса за изтриване:")
        if not gym_id:
            return

        gym = next((g for g in self.nearby_gyms if g.id == gym_id), None)
        if not gym:
            messagebox.showerror("Грешка", f"Фитнес с ID {gym_id} не е намерен.")
            return

        if messagebox.askyesno("Потвърждение", f"Наистина ли искате да изтриете {gym.name}?"):
            self.nearby_gyms.remove(gym)
            messagebox.showinfo("Успешно", f"Фитнесът '{gym.name}' е изтрит успешно.")

    def search_gyms(self, keyword):
        if not keyword or not keyword.strip():
            return []

        keyword = keyword.strip().lower()
        return [
            gym for gym in self.nearby_gyms
            if keyword in gym.name.lower() or
               keyword in gym.address.lower() or
               keyword in gym.location.lower() or
               any(keyword in service.lower() for service in gym.services)
        ]

    def recommend_gyms(self, location):
        if not location or not location.strip():
            return []

        location = location.strip().lower()
        filtered_gyms = [
            gym for gym in self.nearby_gyms
            if gym.location.lower() == location
        ]
        return sorted(filtered_gyms, key=lambda g: g.rating, reverse=True) 