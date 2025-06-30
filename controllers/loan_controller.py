# controllers/loan_controller.py

from models.loan import Loan
from datetime import datetime

class LoanController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_loan(self, book_id, reader_id, loan_date, return_date):
        if not isinstance(loan_date, datetime):
            raise ValueError("loan_date должен быть объектом datetime")
        if not isinstance(return_date, datetime):
            raise ValueError("return_date должен быть объектом datetime")
        if return_date < loan_date:
            raise ValueError("Дата возврата не может быть раньше даты выдачи")

        book = self.db_manager.get_book_by_id(book_id)
        if not book:
            raise ValueError("Книга не найдена")
        if not book.is_available():
            raise ValueError("Книга недоступна для выдачи")

        reader = self.db_manager.get_reader_by_id(reader_id)
        if not reader:
            raise ValueError("Читатель не найден")

        loan = Loan(book_id, reader_id, loan_date, return_date)
        return self.db_manager.add_loan(loan)

    def get_loan(self, loan_id):
        return self.db_manager.get_loan_by_id(loan_id)

    def get_all_loans(self):
        return self.db_manager.get_all_loans()

    def return_book(self, loan_id):
        loan = self.get_loan(loan_id)
        if not loan:
            raise ValueError("Выдача не найдена")
        if loan.is_returned:
            raise ValueError("Книга уже возвращена")

        # Обновляем статус возврата
        loan.return_book()
        self.db_manager.update_loan(loan.id, is_returned=True)

        # Обновляем количество доступных книг
        book = self.db_manager.get_book_by_id(loan.book_id)
        if book:
            book.return_book()
            self.db_manager.update_book(book.id, available=book.available)

        return True

    def get_reader_loans(self, reader_id):
        return self.db_manager.get_reader_loans(reader_id)

    def get_overdue_loans(self):
        return self.db_manager.get_overdue_loans()

    def get_active_loans(self):
        all_loans = self.db_manager.get_all_loans()
        return [loan for loan in all_loans if not loan.is_returned]


