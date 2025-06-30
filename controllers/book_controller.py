# controllers/book_controller.py
from models.book import Book

class BookController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_book(self, title, author, isbn, year, quantity):
        existing_books = self.db_manager.get_all_books()
        for b in existing_books:
            if b.isbn == isbn:
                raise ValueError("ISBN уже существует")
        new_book = Book(title, author, isbn, year, quantity)
        return self.db_manager.add_book(new_book)

    def get_book(self, book_id):
        book = self.db_manager.get_book_by_id(book_id)
        if book:
            return book
        return None

    def get_all_books(self):
        return self.db_manager.get_all_books()

    def update_book(self, book_id, **kwargs):
        self.db_manager.update_book(book_id, **kwargs)

    def delete_book(self, book_id):
        self.db_manager.delete_book(book_id)

    def search_books(self, query):
        return self.db_manager.search_books(query)

    def borrow_book(self, book_id):
        book = self.get_book(book_id)
        if not book:
            raise ValueError("Книга не найдена")
        if book.borrow_book():
            self.db_manager.update_book(book.id, available=book.available)
            return True
        return False

    def return_book(self, book_id):
        book = self.get_book(book_id)
        if not book:
            raise ValueError("Книга не найдена")
        if book.return_book():
            self.db_manager.update_book(book.id, available=book.available)
            return True
        return False

