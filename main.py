import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from del_form2 import Ui_del_form
from add_form import Ui_add_form
from personal_library import Ui_list_shelfes
from change_form import Ui_change_form


class MainWork(Ui_list_shelfes, QMainWindow):  # основной класс
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.adding_book = AddingBook(self)
        self.delete_book = DeleteBook(self)
        self.change_inf = ChangeInf(self)

        self.con = sqlite3.connect('books.sqlite')
        self.create_table()
        self.titles = None

        self.params = {'id': 'id', 'Название': 'title',
                       'Автор': 'author', 'Год издания': 'year', 'Жанр': 'genre'}
        self.cB_choosepar.addItems(list(self.params))
        self.find.clicked.connect(self.find_books)

        self.row_shelfes = 0
        self.shelf = 1

        self.add_new_book.clicked.connect(self.show_add_form)
        self.change.clicked.connect(self.show_change_form)
        self.del_elem.clicked.connect(self.show_del_form)

    def initUi(self):
        self.add_shelf.clicked.connect(self.new_shelf)
        self.del_shelf.clicked.connect(self.no_shelf)
        self.table_shelfes.itemClicked()  # по идее выбор полки

    def create_table(self):
        cur = self.con.cursor()  # добавь бд в папку
        request_bi = """CREATE TABLE IF NOT EXISTS books_inf(    
            id     INTEGER PRIMARY KEY UNIQUE NOT NULL,
            name   TEXT    UNIQUE NOT NULL,
            author INTEGER NOT NULL REFERENCES authors (id),
            year   INTEGER NOT NULL,
            genre  INTEGER NOT NULL REFERENCES genres (id),
            shelf  INTEGER NOT NULL)"""
        request_a = """CREATE TABLE IF NOT EXISTS authors(
            id  INTEGER PRIMARY KEY UNIQUE NOT NULL,
            name    TEXT UNIQUE NOT NULL)"""
        request_g = """CREATE TABLE IF NOT EXISTS genres(
            id    INTEGER PRIMARY KEY UNIQUE NOT NULL,
            title TEXT UNIQUE NOT NULL)"""
        cur.execute(request_a)
        cur.execute(request_g)
        cur.execute(request_bi)
        genres = ['детектив', 'фантастика', 'приключения', 'роман', 'научно-популярная литература',
                  'юмор', 'фэнтези', 'учебная литература', 'поэзия']
        id = 1
        for i in range(len(genres)):
            cur.execute('''INSERT INTO genres (id, title) VALUES (?, ?)''', [id, genres[i]])
            id += 1
        self.con.commit()

    def find_books(self):
        need_text = self.lineEdit.text()
        need = self.params.get(self.cB_choosepar.currentText())

    def add_item(self, name, author, year, genre, num_shelf):
        req = """INSERT INTO books (name, author, year, genre, num_shelf)
        VALUES (?, ?, ?, ?, ?)"""
        self.con.execute(req, [name, author, year, genre, num_shelf])
        self.con.commit()

    def show_add_form(self):
        self.adding_book.show()

    def show_change_form(self):  # нужно добавить
        self.change_inf.show()

    def change_item(self, name, author, year, genre, num_shelf):
        req = """UPDATE books SET name = ?, author = ?,
        year = ?, genre = ?, shelf = ? WHERE id = ?"""
        self.con.execute(req, [name, author, year, genre, num_shelf])
        self.con.commit()

    def show_del_form(self):
        self.delete_book.show()

    def delete_item(self, id):
        req = """DELETE FROM books WHERE id = ?;"""
        self.con.execute(req, [id])
        self.con.commit()

    def new_shelf(self):
        self.table_shelfes.setItem(self.row_shelfes, 0, self.shelf)  # исправить
        self.row_shelfes += 1
        self.shelf += 1

    def no_shelf(self):
        valid = QMessageBox.question(self, 'Удаление', 'Действительно удалить последнюю полку?',
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.table_shelfes.removeCellWidget(self.row_shelfes, 0)
            self.row_shelfes -= 1
            self.shelf -= 1


class AddingBook(QMainWindow, Ui_add_form):  # класс формы добавления
    def __init__(self, parent=None):
        super(AddingBook, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_elem)

    def add_elem(self):
        name = self.name_inp.text()
        author = self.author_inp.text()
        year = self.year_inp.text()
        genre = self.genre_inp.text()
        num_shelf = self.schelf_inp.text()
        self.parent().add_item(name, author, year, genre, num_shelf)
        self.close()


class DeleteBook(QMainWindow, Ui_del_form):  # класс формы удаления
    def __init__(self, parent=None):
        super(DeleteBook, self).__init__(parent)
        self.setupUi(self)
        self.del_btn.clicked.connect(self.del_book)

    def del_book(self):
        id = self.lineEdit.text()
        valid = QMessageBox.question(self, 'Удаление', 'Действительно удалить элемент с id:' + str(id),
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.parent().delete_item(id)
        self.close()


class ChangeInf(QMainWindow, Ui_change_form):  # класс формы редактирования
    def __init__(self, parent=None):
        super(ChangeInf, self).__init__(parent)
        self.setupUi(self)
        self.name = None
        self.author = None
        self.year = None
        self.genre = None
        self.num_shelf = None
        self.pushButton.clicked.connect(self.change_info)

    def set_info(self, name, author, year, genre, num_shelf):
        self.name = name
        self.author = author
        self.year = year
        self.genre = genre
        self.num_shelf = num_shelf
        self.name_inp.setText(name)
        self.author_inp.setText(author)
        self.year_inp.setText(year)
        self.genre_inp.setText(genre)
        self.schelf_inp.setText(num_shelf)

    def change_info(self):
        name = self.name_inp.text()
        author = self.author_inp.text()
        year = self.year_inp.text()
        genre = self.genre_inp.text()
        num_shelf = self.schelf_inp.text()
        self.parent().change_item(name, author, year, genre, num_shelf)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWork()
    mw.show()
    sys.exit(app.exec())
