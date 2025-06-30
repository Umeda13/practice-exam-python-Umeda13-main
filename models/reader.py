# models/reader.py

from datetime import datetime
import re


class Reader:
    def __init__(self, name, email, phone):
        if not name or not isinstance(name, str):
            raise ValueError("Имя должно быть непустой строкой")
        if "@" not in email or "." not in email:
            raise ValueError("Некорректный email")
        if not phone.startswith("+"):
            raise ValueError("Телефон должен начинаться с '+'")

        self.id = None
        self.name = name
        self.email = email
        self.phone = phone
        self.registration_date = datetime.now()

    def update_info(self, name=None, email=None, phone=None):
        if name is not None:
            if not name or not isinstance(name, str):
                raise ValueError("Имя должно быть непустой строкой")
            self.name = name
        if email is not None:
            if "@" not in email or "." not in email:
                raise ValueError("Некорректный email")
            self.email = email
        if phone is not None:
            if not phone.startswith("+"):
                raise ValueError("Телефон должен начинаться с '+'")
            self.phone = phone

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "registration_date": self.registration_date
        }

