import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from del_form2 import Ui_del_form
from add_form import Ui_add_form
from personal_library import Ui_list_shelfes
from change_form import Ui_change_form
from more_a import Ui_more_authors
from more_g import Ui_more_genres


class MainWork(Ui_list_shelfes, QMainWindow):  # основной класс
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.adding_book = AddingBook(self)
        self.delete_book = DeleteBook(self)
        self.change_inf = ChangeInf(self)
        self.more_authors = AddAuthor(self)
        self.more_genre = AddGenre(self)

        self.con = sqlite3.connect('books.sqlite')
        self.create_table()
        self.titles = None

        self.names_a = []
        self.titles_g = []

        self.params = {'id': 'id', 'Название': 'title',
                       'Автор': 'author', 'Год издания': 'year', 'Жанр': 'genre'}
        self.cB_choosepar.addItems(list(self.params))
        self.find.clicked.connect(self.find_books)

        self.row_shelves = 0
        self.shelf = 1
        self.shelves = []

        self.add_new_book.clicked.connect(self.show_add_form)
        self.change.clicked.connect(self.show_change_form)
        self.del_elem.clicked.connect(self.show_del_form)

    def initUi(self):
        self.table_shelfes.setRowCount(len(self.shelves))
        self.table_shelfes.setColumnCount(1)
        self.table_shelfes.setHorizontalHeader('№ Полки')
        self.add_shelf.clicked.connect(self.new_shelf)
        self.del_shelf.clicked.connect(self.no_shelf)
        self.table_shelfes.itemClicked()  # по идее выбор полки

    def create_table(self):
        cur = self.con.cursor()
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
        self.con.commit()
        genres = ['детектив', 'фантастика', 'приключения', 'роман', 'научно-популярная литература',
                  'юмор', 'фэнтези', 'учебная литература', 'поэзия']
        for i in genres:
            cur.execute('''INSERT INTO genres (title)  VALUES (?)''', [i])
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
        req = """DELETE FROM books WHERE id = ?"""
        self.con.execute(req, [id])
        self.con.commit()

    def new_shelf(self):
        self.table_shelfes.setItem(self.row_shelfes, 0, self.shelf)  # исправить
        self.shelves.append(self.shelf)
        self.row_shelfes += 1
        self.shelf += 1

    def no_shelf(self):
        valid = QMessageBox.question(self, 'Удаление', 'Действительно удалить последнюю полку?',
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.table_shelfes.removeCellWidget(self.row_shelfes, 0)
            del self.shelves[-1]
            self.row_shelfes -= 1
            self.shelf -= 1

    def show_more_a(self):
        self.more_authors.show()

    def show_more_g(self):
        self.more_genre.show()

    def author_add(self, name_a):  # добавление элементов в таблицу авторов
        cur = self.con.cursor()
        req = """INSERT INTO authors (title) VALUES (?)"""
        cur.execute(req, [name_a])
        self.con.commit()

    def genres_add(self, title_g):  # добавление элементов в таблицу жанров
        cur = self.con.cursor()
        req = """INSERT INTO genres (title) VALUES (?)"""
        cur.execute(req, [title_g])
        self.con.commit()

    def take_info_authors(self):  # формат!
        self.con = sqlite3.connect('books.sqlite')
        cur = self.con.cursor()
        self.names_a = cur.execute("""SELECT name FROM authors""").fetchall()
        self.con.commit()
        return map(list, self.names_a)

    def take_info_genres(self):
        self.con = sqlite3.connect('books.sqlite')
        cur = self.con.cursor()
        # self.con.row_factory = lambda self.cur, row: (str(row[0]) + ". " + row[1], row[0])
        self.titles_g = cur.execute("""SELECT title FROM genres""").fetchall()
        self.con.commit()
        return map(list, self.titles_g)

    def current_author(self, name):
        cur = self.con.cursor()
        author = cur.execute("""SELECT author FROM books_inf WHERE name = ?""", [name])
        self.con.commit()
        return author

    def current_genre(self, name):
        cur = self.con.cursor()
        genre = cur.execute("""SELECT genre FROM books_inf WHERE name = ?""", [name])
        self.con.commit()
        return genre

    def current_shelf(self, name):
        cur = self.con.cursor()
        shelf = cur.execute("""SELECT shelf FROM books_inf WHERE name = ?""", [name])
        self.con.commit()
        return shelf


class AddingBook(QMainWindow, Ui_add_form):  # класс формы добавления
    def __init__(self, parent=None):
        super(AddingBook, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_elem)
        self.more_authors.clicked.connect(self.parent().show_more_a)
        self.more_genres.clicked.connect(self.parent().show_more_g)
        self.more_shelfes.clicked.connect(self.parent().new_shelf)

        # self.cB_author.addItems(self.parent().take_info_authors())
        # self.cB_genre.addItems(self.parent().take_info_genres())
        # self.cB_shelf.addItems(self.parent().shelves)

    def add_elem(self):
        name = self.name_inp.text()
        author = self.cB_author.currentText()
        year = self.year_inp.text()
        genre = self.cB_genre.currentText()
        num_shelf = self.cB_shelf.currentText()
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
        self.more_authors.clicked.connect(self.parent().show_more_a)
        self.more_genres.clicked.connect(self.parent().show_more_g)
        self.more_shelfes.clicked.connect(self.parent().new_shelf)

        # self.cB_author.addItems(list(self.parent().take_info_authors()))
        # self.cB_genre.addItems(list(self.parent().take_info_genres()))
        # self.cB_shelf.addItems(self.parent().shelves)

    def set_info(self, name, year):  # изменить
        self.name = name
        self.author = self.parent().current_author(name)
        self.year = year
        self.genre = self.parent().current_genre(name)
        self.num_shelf = self.parent().current_shelf(name)
        self.name_inp.setText(name)
        self.cB_author.setCurrentText(self.parent().current_author(name))
        self.year_inp.setText(year)
        self.genre_inp.setText(self.parent().current_genre(name))
        self.schelf_inp.setText(self.parent().current_shelf(name))

    def change_info(self):
        name = self.name_inp.text()
        author = self.cB_author.currentText()
        year = self.year_inp.text()
        genre = self.cB_genre.currentText()
        num_shelf = self.cB_shelf.currentText()
        self.parent().change_item(name, author, year, genre, num_shelf)
        self.close()


class AddAuthor(Ui_more_authors, QMainWindow):  # класс формы добавления авторов
    def __init__(self, parent=None):
        super(AddAuthor, self).__init__(parent)
        self.setupUi(self)
        self.save_new_a.clicked.connect(self.new_elem)

    def new_elem(self):
        name_a = self.author_inp.text()
        self.parent().author_add(name_a)
        self.close()


class AddGenre(Ui_more_genres, QMainWindow):    # класс формы добавления жанров
    def __init__(self, parent=None):
        super(AddGenre, self).__init__(parent)
        self.setupUi(self)
        self.save_new_g.clicked.connect(self.new_elem)

    def new_elem(self):
        title_g = self.genre_inp.text()
        self.parent().genre_add(title_g)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWork()
    mw.show()
    sys.exit(app.exec())
