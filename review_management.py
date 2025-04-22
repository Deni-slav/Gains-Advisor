from models import Review
from tkinter import messagebox, simpledialog

class ReviewManager:
    def __init__(self):
        self.gym_reviews = []

    def add_review(self, current_user, gym_manager):
        if not current_user:
            messagebox.showerror("Грешка", "Трябва да влезете в системата, за да пишете ревюта.")
            return
            
        if current_user.role not in ["subscribed", "admin"]:
            messagebox.showerror("Грешка", "Само абонирани потребители и администратори могат да пишат ревюта.")
            return

        # Показване на налични фитнеси
        gyms_text = "\n".join([f"{g.id}. {g.name} - {g.address}" for g in gym_manager.nearby_gyms])
        messagebox.showinfo("Налични фитнеси", gyms_text)

        while True:
            try:
                gym_id = simpledialog.askinteger("Ревю", "Въведете ID на фитнес за ревю:")
                if gym_id is None:  
                    return
                    
                if not isinstance(gym_id, int) or gym_id <= 0:
                    messagebox.showerror("Грешка", "ID на фитнес трябва да бъде положително число!")
                    continue
                    
                gym = next((g for g in gym_manager.nearby_gyms if g.id == gym_id), None)
                if not gym:
                    messagebox.showerror("Грешка", f"Не е намерен фитнес с ID {gym_id}!")
                    continue
                    
                # Проверка за вече съществуващо ревю
                existing_review = next((r for r in self.gym_reviews 
                                     if r.gym_id == gym_id and r.user_id == current_user.username), None)
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

        # Създаване и добавяне на ревюто
        new_review = Review(
            gym_id=gym_id,
            user_id=current_user.username,
            rating=rating,
            comment=comment
        )
        self.gym_reviews.append(new_review)
        
        # Обновяване на рейтинга на фитнеса
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

    def view_reviews(self, gym_manager):
        if not self.gym_reviews:
            messagebox.showinfo("Ревюта", "Няма налични ревюта.")
            return
            
        reviews_text = []
        for review in self.gym_reviews:
            gym = next((g for g in gym_manager.nearby_gyms if g.id == review.gym_id), None)
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