# models/book.py

from datetime import datetime


class Book:
    def __init__(self, title, author, isbn, year, quantity, id=None, available=None):
        if not isinstance(year, int) or year <= 0:
            raise ValueError("Год должен быть положительным целым числом")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Количество должно быть положительным целым числом")
        if not title or not isinstance(title, str):
            raise ValueError("Название должно быть непустой строкой")

        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.quantity = quantity
        self.available = available if available is not None else quantity

    def borrow_book(self):
        if self.available > 0:
            self.available -= 1
            return True
        return False

    def return_book(self):
        if self.available < self.quantity:
            self.available += 1
            return True
        return False

    def is_available(self):
        return self.available > 0

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
            "quantity": self.quantity,
            "available": self.available
        }

