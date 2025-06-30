# views/reader_view.py

import tkinter as tk
from tkinter import ttk, messagebox


class ReaderView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent)

        form_frame = ttk.LabelFrame(self.frame, text="Добавить читателя")
        form_frame.pack(padx=10, pady=10, fill="x")

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        ttk.Label(form_frame, text="Имя").grid(row=0, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(form_frame, text="Email").grid(row=1, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.email_var).grid(row=1, column=1, sticky="ew")

        ttk.Label(form_frame, text="Телефон").grid(row=2, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.phone_var).grid(row=2, column=1, sticky="ew")

        ttk.Button(form_frame, text="Добавить", command=self.add_reader).grid(
            row=3, columnspan=2, pady=5)

        table_frame = ttk.LabelFrame(self.frame, text="Список читателей")
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame,
                                 columns=("ID", "Имя", "Email", "Телефон", "Дата регистрации"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=5, fill="x")

        ttk.Button(btn_frame, text="Обновить список", command=self.load_readers).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_reader).pack(side="right", padx=5)

        self.load_readers()

    def add_reader(self):
        try:
            self.controller.add_reader(
                self.name_var.get(),
                self.email_var.get(),
                self.phone_var.get()
            )
            self.clear_form()
            self.load_readers()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_form(self):
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")

    def load_readers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        readers = self.controller.get_all_readers()
        for reader in readers:
            self.tree.insert("", "end", values=(
                reader.id,
                reader.name,
                reader.email,
                reader.phone,
                reader.registration_date.strftime("%Y-%m-%d %H:%M") if hasattr(reader.registration_date, 'strftime') else reader.registration_date
            ))

    def delete_reader(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите читателя для удаления")
            return
        item = self.tree.item(selected[0])
        reader_id = item['values'][0]
        if messagebox.askyesno("Подтверждение", "Удалить этого читателя?"):
            try:
                self.controller.delete_reader(reader_id)
                self.load_readers()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

