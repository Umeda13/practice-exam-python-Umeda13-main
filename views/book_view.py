# views/book_view.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class BookView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent)

        form_frame = ttk.LabelFrame(self.frame, text="Добавить книгу")
        form_frame.pack(padx=10, pady=10, fill="x")

        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.year_var = tk.IntVar()
        self.quantity_var = tk.IntVar()

        ttk.Label(form_frame, text="Название").grid(row=0, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.title_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(form_frame, text="Автор").grid(row=1, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.author_var).grid(row=1, column=1, sticky="ew")

        ttk.Label(form_frame, text="ISBN").grid(row=2, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.isbn_var).grid(row=2, column=1, sticky="ew")

        ttk.Label(form_frame, text="Год издания").grid(row=3, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.year_var).grid(row=3, column=1, sticky="ew")

        ttk.Label(form_frame, text="Количество").grid(row=4, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.quantity_var).grid(row=4, column=1, sticky="ew")

        ttk.Button(form_frame, text="Добавить", command=self.add_book).grid(
            row=5, columnspan=2, pady=5)

        table_frame = ttk.LabelFrame(self.frame, text="Список книг")
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame,
                                 columns=("ID", "Название", "Автор", "ISBN", "Год", "Доступно"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=5, fill="x")

        ttk.Button(btn_frame, text="Обновить список", command=self.load_books).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Поиск", command=self.search_books).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_book).pack(side="right", padx=5)

        self.load_books()

    def add_book(self):
        try:
            self.controller.add_book(
                self.title_var.get(),
                self.author_var.get(),
                self.isbn_var.get(),
                self.year_var.get(),
                self.quantity_var.get()
            )
            self.clear_form()
            self.load_books()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_form(self):
        self.title_var.set("")
        self.author_var.set("")
        self.isbn_var.set("")
        self.year_var.set(0)
        self.quantity_var.set(0)

    def load_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        books = self.controller.get_all_books()
        for book in books:
            self.tree.insert("", "end", values=(
                book.id,
                book.title,
                book.author,
                book.isbn,
                book.year,
                book.available
            ))

    def search_books(self):
        query = simpledialog.askstring("Поиск", "Введите запрос:")
        if query:
            try:
                books = self.controller.search_books(query)
                self.tree.delete(*self.tree.get_children())  # Очищаем таблицу

                if not books:
                    messagebox.showinfo("Результат", "Книги не найдены")
                    self.load_books()  # Возвращаем полный список
                    return

                for book in books:
                    self.tree.insert("", "end", values=(
                        book.id,
                        book.title,
                        book.author,
                        book.isbn,
                        book.year,
                        book.available
                    ))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при поиске: {str(e)}")
                self.load_books()


    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу для удаления")
            return
        item = self.tree.item(selected[0])
        book_id = item['values'][0]
        if messagebox.askyesno("Подтверждение", "Удалить эту книгу?"):
            try:
                self.controller.delete_book(book_id)
                self.load_books()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

