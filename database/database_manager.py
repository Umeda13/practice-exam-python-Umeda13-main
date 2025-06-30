# database/database_manager.py

import sqlite3
from datetime import datetime
from models.book import Book
from models.reader import Reader
from models.loan import Loan


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT NOT NULL UNIQUE,
                    year INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    available INTEGER NOT NULL
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS readers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL,
                    registration_date TEXT NOT NULL
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    reader_id INTEGER NOT NULL,
                    loan_date TEXT NOT NULL,
                    return_date TEXT NOT NULL,
                    is_returned INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY(book_id) REFERENCES books(id),
                    FOREIGN KEY(reader_id) REFERENCES readers(id)
                )
            ''')

    # Books methods
    def add_book(self, book):
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('''
                INSERT INTO books (title, author, isbn, year, quantity, available)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (book.title, book.author, book.isbn, book.year, book.quantity, book.available))
            book.id = cur.lastrowid
            return book.id

    def get_book_by_id(self, book_id):
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        row = cur.fetchone()
        if row:
            return Book(
                title=row[1],
                author=row[2],
                isbn=row[3],
                year=row[4],
                quantity=row[5],
                id=row[0],
                available=row[6]
            )
        return None

    def get_all_books(self):
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM books')
        return [
            Book(
                title=row[1],
                author=row[2],
                isbn=row[3],
                year=row[4],
                quantity=row[5],
                id=row[0],
                available=row[6]
            )
            for row in cur.fetchall()
        ]

    def update_book(self, book_id, **kwargs):
        with self.connection:
            fields = ', '.join(f"{k} = ?" for k in kwargs)
            values = list(kwargs.values()) + [book_id]
            self.connection.execute(f'UPDATE books SET {fields} WHERE id = ?', values)

    def delete_book(self, book_id):
        with self.connection:
            self.connection.execute('DELETE FROM books WHERE id = ?', (book_id,))

    def search_books(self, query):
        search_term = f"%{query}%"
        cur = self.connection.cursor()
        cur.execute('''
            SELECT * FROM books 
            WHERE title LIKE ? COLLATE NOCASE
            OR author LIKE ? COLLATE NOCASE
            OR isbn LIKE ? COLLATE NOCASE
        ''', (search_term, search_term, search_term))
        return [
            Book(
                title=row[1],
                author=row[2],
                isbn=row[3],
                year=row[4],
                quantity=row[5],
                id=row[0],
                available=row[6]
            )
            for row in cur.fetchall()
        ]

    # Readers methods
    def add_reader(self, reader):
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('''
                INSERT INTO readers (name, email, phone, registration_date)
                VALUES (?, ?, ?, ?)
            ''', (reader.name, reader.email, reader.phone,
                  reader.registration_date.isoformat()))
            reader.id = cur.lastrowid
            return reader.id

    def get_reader_by_id(self, reader_id):
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM readers WHERE id = ?', (reader_id,))
        row = cur.fetchone()
        if row:
            reader = Reader(row[1], row[2], row[3])
            reader.id = row[0]
            reader.registration_date = datetime.fromisoformat(row[4])
            return reader
        return None

    def get_all_readers(self):
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM readers')
        return [
            self._create_reader_from_row(row) for row in cur.fetchall()
        ]

    def update_reader(self, reader_id, **kwargs):
        with self.connection:
            fields = ', '.join(f"{k} = ?" for k in kwargs)
            values = list(kwargs.values()) + [reader_id]
            self.connection.execute(f'UPDATE readers SET {fields} WHERE id = ?', values)

    def delete_reader(self, reader_id):
        with self.connection:
            self.connection.execute('DELETE FROM readers WHERE id = ?', (reader_id,))

    # Loans methods
    def add_loan(self, loan):
        with self.connection:
            cur = self.connection.cursor()
            cur.execute('''
                INSERT INTO loans (book_id, reader_id, loan_date, return_date, is_returned)
                VALUES (?, ?, ?, ?, ?)
            ''', (loan.book_id, loan.reader_id,
                  loan.loan_date.isoformat(),
                  loan.return_date.isoformat(),
                  int(loan.is_returned)))
            loan.id = cur.lastrowid
            return loan.id

    def get_loan_by_id(self, loan_id):
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM loans WHERE id = ?', (loan_id,))
        row = cur.fetchone()
        if row:
            return self._create_loan_from_row(row)
        return None

    def get_all_loans(self, only_active=False):
        cur = self.connection.cursor()
        if only_active:
            cur.execute('SELECT * FROM loans WHERE is_returned = 0')
        else:
            cur.execute('SELECT * FROM loans')
        return [
            self._create_loan_from_row(row)
            for row in cur.fetchall()
        ]

    def update_loan(self, loan_id, **kwargs):
        with self.connection:
            if 'loan_date' in kwargs and isinstance(kwargs['loan_date'], datetime):
                kwargs['loan_date'] = kwargs['loan_date'].isoformat()
            if 'return_date' in kwargs and isinstance(kwargs['return_date'], datetime):
                kwargs['return_date'] = kwargs['return_date'].isoformat()
            if 'is_returned' in kwargs:
                kwargs['is_returned'] = int(kwargs['is_returned'])

            fields = ', '.join(f"{k} = ?" for k in kwargs)
            values = list(kwargs.values()) + [loan_id]
            self.connection.execute(f'UPDATE loans SET {fields} WHERE id = ?', values)

    def get_reader_loans(self, reader_id):
        cur = self.connection.cursor()
        cur.execute('''
            SELECT * FROM loans 
            WHERE reader_id = ? AND is_returned = 0
        ''', (reader_id,))
        return [
            self._create_loan_from_row(row)
            for row in cur.fetchall()
        ]

    def get_overdue_loans(self):
        now = datetime.now().isoformat()
        cur = self.connection.cursor()
        cur.execute('''
            SELECT * FROM loans
            WHERE is_returned = 0 AND return_date < ?
        ''', (now,))
        return [
            self._create_loan_from_row(row) for row in cur.fetchall()
        ]

    # Helper methods
    def _create_reader_from_row(self, row):
        reader = Reader(row[1], row[2], row[3])
        reader.id = row[0]
        reader.registration_date = datetime.fromisoformat(row[4])
        return reader

    def _create_loan_from_row(self, row):
        loan = Loan(
            row[1],
            row[2],
            datetime.fromisoformat(row[3]),
            datetime.fromisoformat(row[4])
        )
        loan.id = row[0]
        loan.is_returned = bool(row[5])
        return loan

    def close(self):
        if self.connection:
            self.connection.close()
