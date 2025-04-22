from models import User
from tkinter import messagebox, simpledialog

class UserManager:
    def __init__(self):
        self.registered_users = []
        self.current_user = None

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

    def login(self):
        while True:
            username = simpledialog.askstring("Вход в системата", "Потребителско име (задължително):")
            if username is None:  
                return
                
            if not username or not username.strip():
                messagebox.showerror("Грешка", "Моля, въведете потребителско име!")
                continue
                
            password = simpledialog.askstring("Вход в системата", "Парола (задължително):", show='*')
            if password is None:  
                return
                
            if not password:
                messagebox.showerror("Грешка", "Моля, въведете парола!")
                continue
                
            user = next((u for u in self.registered_users 
                        if u.username == username.strip() 
                        and u.password == password), None)
                        
            if user:
                self.current_user = user
                messagebox.showinfo("Успешен вход", 
                            f"Добре дошли, {user.username}!\n"
                            f"Роля: {user.role}\n"
                            f"Имейл: {user.email}")
                return
            else:
                messagebox.showerror("Грешка", "Невалидно потребителско име или парола!")
                continue

    def logout(self):
        if self.current_user:
            self.current_user = None
            messagebox.showinfo("Изход", "Успешно излязохте от системата.")
        else:
            messagebox.showinfo("Информация", "Не сте влезли в системата.") 