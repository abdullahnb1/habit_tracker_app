from datetime import datetime
from typing import List
import bcrypt
import os
import hashlib
import uuid

class User:
    def __init__(self, user_id: str, salt: bytes, full_name: str, hashed_password: bytes, email: str, habits: List['Habit']):
        self.user_id = user_id
        self.salt = salt
        self.full_name = full_name
        self.hashed_password = hashed_password
        self.creation_date = datetime.now()
        self.recent_login = self.creation_date
        self.email = email
        self.habits = habits

    def update_last_login(self):
        self.recent_login = datetime.now()

    def clear_data(self, category: str):
        if hasattr(self, category):
            setattr(self, category, None)

    def get_info(self) -> str:
        return f"User ID: {self.user_id}, Full Name: {self.full_name}, Email: {self.email}"

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    def authenticate(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())

    def add_habit(self, habit: 'Habit'):
        self.habits.append(habit)

    def remove_habit(self, habit_id: str):
        self.habits = [habit for habit in self.habits if habit.habit_id != habit_id]


class UserList:
    def __init__(self):
        self.users = []

    def create(self, name: str, password: str):
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        user_id = str(uuid.uuid4())
        new_user = User(user_id, salt, name, hashed_password, email=None, habits=[])
        self.users.append(new_user)

    def reset(self):
        self.users = []

    def delete_user(self, user_id: str):
        self.users = [user for user in self.users if user.user_id != user_id]
