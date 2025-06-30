# views/loan_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkinter import simpledialog

class LoanView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent)

        form_frame = ttk.LabelFrame(self.frame, text="Выдать книгу")
        form_frame.pack(padx=10, pady=10, fill="x")

        self.book_id_var = tk.IntVar()
        self.reader_id_var = tk.IntVar()

        ttk.Label(form_frame, text="ID Книги").grid(row=0, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.book_id_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(form_frame, text="ID Читателя").grid(row=1, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.reader_id_var).grid(row=1, column=1, sticky="ew")

        ttk.Button(form_frame, text="Выдать", command=self.create_loan).grid(
            row=2, columnspan=2, pady=5)

        table_frame = ttk.LabelFrame(self.frame, text="Список выдач")
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame,
                                 columns=("ID", "ID Книги", "ID Читателя", "Дата выдачи", "Дата возврата", "Статус"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=5, fill="x")

        ttk.Button(btn_frame, text="Обновить список", command=self.load_loans).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Вернуть", command=self.return_loan).pack(side="right", padx=5)

        self.load_loans()

    def create_loan(self):
        try:
            book_id = self.book_id_var.get()
            reader_id = self.reader_id_var.get()
            loan_date = datetime.now()
            return_date = loan_date + timedelta(days=14)
            self.controller.create_loan(book_id, reader_id, loan_date, return_date)
            self.load_loans()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def load_loans(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        loans = self.controller.get_all_loans()
        for loan in loans:
            if not loan.is_returned:  # Показываем только не возвращенные книги
                self.tree.insert("", "end", values=(
                    loan.id,
                    loan.book_id,
                    loan.reader_id,
                    loan.loan_date.strftime("%Y-%m-%d %H:%M") if hasattr(loan.loan_date,
                                                                         'strftime') else loan.loan_date,
                    loan.return_date.strftime("%Y-%m-%d %H:%M") if hasattr(loan.return_date,
                                                                           'strftime') else loan.return_date,
                    "Активна"
                ))

    def return_loan(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите выдачу для возврата")
            return
        item = self.tree.item(selected[0])
        loan_id = item['values'][0]
        try:
            if self.controller.return_book(loan_id):
                messagebox.showinfo("Успех", "Книга успешно возвращена")
                self.load_loans()  # Обязательно обновляем список после возврата
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def search_books(self):
        query = tk.simpledialog.askstring("Поиск", "Введите запрос:")  # Оставлено tk.
        if query:
            books = self.controller.search_books(query)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for book in books:
                self.tree.insert("", "end", values=(
                    book.id,
                    book.title,
                    book.author,
                    book.isbn,
                    book.year,
                    book.available
                ))
