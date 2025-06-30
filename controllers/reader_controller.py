# controllers/reader_controller.py

from models.reader import Reader


class ReaderController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_reader(self, name, email, phone):
        readers = self.db_manager.get_all_readers()
        for r in readers:
            if r.email == email:
                raise ValueError("Email уже зарегистрирован")
        new_reader = Reader(name, email, phone)
        return self.db_manager.add_reader(new_reader)

    def get_reader(self, reader_id):
        return self.db_manager.get_reader_by_id(reader_id)

    def get_all_readers(self):
        return self.db_manager.get_all_readers()

    def update_reader(self, reader_id, **kwargs):
        if 'email' in kwargs:
            readers = self.db_manager.get_all_readers()
            for r in readers:
                if r.email == kwargs['email'] and r.id != reader_id:
                    raise ValueError("Email уже зарегистрирован другим пользователем")
        self.db_manager.update_reader(reader_id, **kwargs)

    def delete_reader(self, reader_id):
        self.db_manager.delete_reader(reader_id)

    def get_reader_loans(self, reader_id):
        return self.db_manager.get_reader_loans(reader_id)
