# views/main_window.py

import tkinter as tk
from tkinter import ttk
from views.book_view import BookView
from views.reader_view import ReaderView
from views.loan_view import LoanView


class MainWindow:
    def __init__(self, root, book_controller, reader_controller, loan_controller):
        self.root = root
        self.root.title("Библиотечная система")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.book_view = BookView(self.notebook, book_controller)
        self.reader_view = ReaderView(self.notebook, reader_controller)
        self.loan_view = LoanView(self.notebook, loan_controller)

        self.notebook.add(self.book_view.frame, text="Книги")
        self.notebook.add(self.reader_view.frame, text="Читатели")
        self.notebook.add(self.loan_view.frame, text="Выдачи")

