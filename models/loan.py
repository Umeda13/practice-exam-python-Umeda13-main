# models/loan.py

from datetime import datetime


class Loan:
    def __init__(self, book_id, reader_id, loan_date, return_date):
        if not isinstance(book_id, int) or book_id <= 0:
            raise ValueError("book_id должен быть положительным целым числом")
        if not isinstance(reader_id, int) or reader_id <= 0:
            raise ValueError("reader_id должен быть положительным целым числом")
        if not isinstance(loan_date, datetime):
            raise ValueError("loan_date должен быть объектом datetime")
        if not isinstance(return_date, datetime):
            raise ValueError("return_date должен быть объектом datetime")
        if return_date < loan_date:
            raise ValueError("Дата возврата не может быть раньше даты выдачи")

        self.id = None
        self.book_id = book_id
        self.reader_id = reader_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_returned = False

    def return_book(self):
        if not self.is_returned:
            self.is_returned = True
            return True
        return False

    def is_overdue(self):
        return not self.is_returned and datetime.now() > self.return_date

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "reader_id": self.reader_id,
            "loan_date": self.loan_date,
            "return_date": self.return_date,
            "is_returned": self.is_returned
        }
