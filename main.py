import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from del_form2 import Ui_del_form
from add_form import Ui_add_form
from personal_library import Ui_list_shelfes
from change_form import Ui_change_form
from more_a import Ui_more_authors
from more_g import Ui_more_genres
from wl_form import Ui_wl_form
from del_shelf import Ui_del_shelf_form


class MainWork(Ui_list_shelfes, QMainWindow):  # основной класс
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('books.sqlite')
        self.create_table()
        self.setupUi(self)

        self.adding_book = AddingBook(self)
        self.delete_book = DeleteBook(self)
        self.change_inf = ChangeInf(self)
        self.more_authors = AddAuthor(self)
        self.more_genre = AddGenre(self)
        self.to_wl = ToWishlist(self)
        self.to_shelf = FromWlToShelf(self)
        self.delete_shelf = DeleteShelf(self)
        self.delete_from_wl = DeleteFromWl(self)

        self.names_a = []
        self.titles_g = []
        self.sh = []

        self.params = {'id': 'id', 'Название': 'title',
                       'Автор': 'author', 'Год издания': 'year', 'Жанр': 'genre'}
        self.cB_choosepar.addItems(list(self.params))
        self.find.clicked.connect(self.find_books)

        self.ifchange.setText('Для редактирования нажмите на любую ячейку элемента')
        self.add_new_book.clicked.connect(self.show_add_form)
        self.book_table.cellClicked.connect(self.show_change_form)
        self.del_elem.clicked.connect(self.show_del_form)

        self.list_shelf.addItems(map(str, self.take_info_shelves()))
        self.add_shelf.clicked.connect(self.add_new_shelf)
        self.del_shelf.clicked.connect(self.no_shelf)
        self.list_shelf.itemClicked.connect(self.show_shelf_books)
        self.num = 0

        self.add_book.clicked.connect(self.show_wl_form)
        self.on_shelf.clicked.connect(self.show_add_wl)
        self.del_wl.clicked.connect(self.show_del_wl_form)
        self.redraw_wl()

    def create_table(self):  # создает таблицы в бд, если их нет, и заполняет таблицу с жанрами
        cur = self.con.cursor()  # "встроенными" жанрами
        request_bi = """CREATE TABLE IF NOT EXISTS books_inf(    
            id     INTEGER PRIMARY KEY UNIQUE NOT NULL,
            name   TEXT    UNIQUE NOT NULL,
            author INTEGER NOT NULL REFERENCES authors (id),
            year   INTEGER NOT NULL,
            genre  INTEGER NOT NULL REFERENCES genres (id),
            shelf  INTEGER NOT NULL);"""
        request_a = """CREATE TABLE IF NOT EXISTS authors(
            id  INTEGER PRIMARY KEY UNIQUE NOT NULL,
            name    TEXT UNIQUE NOT NULL);"""
        request_g = """CREATE TABLE IF NOT EXISTS genres(
            id    INTEGER PRIMARY KEY UNIQUE NOT NULL,
            title TEXT UNIQUE NOT NULL);"""
        request_sh = """CREATE TABLE IF NOT EXISTS shelves (
            id INTEGER PRIMARY KEY
                UNIQUE
                NOT NULL);"""
        request_wl = """CREATE TABLE IF NOT EXISTS wishlist(
            id INTEGER PRIMARY KEY UNIQUE NOT NULL,
            name TEXT NOT NULL,
            author INTEGER NOT NULL REFERENCES authors (id),
            price INTEGER NOT NULL);"""
        cur.execute(request_a)
        cur.execute(request_g)
        cur.execute(request_bi)
        cur.execute(request_sh)
        cur.execute(request_wl)
        self.con.commit()
        genres = ['детектив', 'фантастика', 'приключения', 'роман', 'научно-популярная литература',
                  'юмор', 'фэнтези', 'учебная литература', 'поэзия']
        temp = list(cur.execute("""SELECT title FROM genres"""))
        if len(temp) == 0:
            for i in genres:
                cur.execute('''INSERT INTO genres (title)  VALUES (?)''', [i])
        self.con.commit()

    def show_shelf_books(self):  # выводит книги с выбранной полки
        self.con = sqlite3.connect('books.sqlite')
        cur = self.con.cursor()
        num = self.list_shelf.currentItem().text()
        req = """SELECT b.id, b.name, a.name, b.year, g.title FROM authors as a,
         genres as g JOIN books_inf as b ON b.author = a.id and b.genre = g.id WHERE b.shelf = ?"""
        result = cur.execute(req, [num]).fetchall()
        self.list_of_books.setRowCount(len(result))
        if len(result):
            self.list_of_books.setColumnCount(len(result[0]))
        headers = ['id', 'Название', 'Автор', 'Год издания', 'Жанр']
        self.list_of_books.setHorizontalHeaderLabels(headers)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.list_of_books.setItem(i, j, QTableWidgetItem(str(val)))

    def find_books(self):  # показывает книги по параметру
        self.con = sqlite3.connect('books.sqlite')
        cur = self.con.cursor()
        need_text = self.lineEdit.text()
        need = self.params.get(self.cB_choosepar.currentText())
        res = []
        self.ifno_inf.clear()
        if need == 'id':
            req = """SELECT b.id, b.name, a.name, b.year, g.title, b.shelf FROM books_inf as b, authors as a, 
            genres as g WHERE b.author = a.id and b.genre = g.id and b.id = ?"""
            res = self.con.execute(req, [need_text]).fetchall()
        elif need == 'title':
            req = """SELECT b.id, b.name, a.name, b.year, g.title, b.shelf FROM books_inf as b, authors as a, 
            genres as g WHERE b.author = a.id and b.genre = g.id and b.name = ?"""
            res = self.con.execute(req, [need_text]).fetchall()
        elif need == 'author':
            req = """SELECT b.id, b.name, a.name, b.year, g.title, b.shelf FROM books_inf as b, authors as a, 
                        genres as g WHERE b.author = a.id and b.genre = g.id and a.name = ?"""
            res = self.con.execute(req, [need_text]).fetchall()
        elif need == 'year':
            req = """SELECT b.id, b.name, a.name, b.year, g.title, b.shelf FROM books_inf as b, authors as a, 
                        genres as g WHERE b.author = a.id and b.genre = g.id and b.year = ?"""
            res = self.con.execute(req, [int(need_text)]).fetchall()
        elif need == 'genre':
            req = """SELECT b.id, b.name, a.name, b.year, g.title, b.shelf FROM books_inf as b, authors as a, 
                        genres as g WHERE b.author = a.id and b.genre = g.id and g.title = ?"""
            res = self.con.execute(req, [need_text.lower()]).fetchall()
        if len(res) == 0:
            self.ifno_inf.setText('Ничего не найдено. Проверьте написание параметра')
        self.book_table.setRowCount(len(res))
        if len(res):
            self.book_table.setColumnCount(len(res[0]))
        headers = ['id', 'Название', "Автор", "Год издания", "Жанр", "№ Полки"]
        self.book_table.setHorizontalHeaderLabels(headers)
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.book_table.setItem(i, j, QTableWidgetItem(str(val)))

    def add_item(self, name, author, year, genre, num_shelf):  # добавление книг в бд
        cur = self.con.cursor()
        ind_author = cur.execute("""SELECT id FROM authors WHERE name = ? LIMIT 1""", [author]).fetchone()
        ind_genre = cur.execute("""SELECT id FROM genres WHERE title = ? LIMIT 1""", [genre]).fetchone()
        req = """INSERT INTO books_inf (name, author, year, genre, shelf) VALUES (?, ?, ?, ?, ?)"""
        cur.execute(req, [name, ind_author, year, ind_genre, int(*num_shelf)])
        self.con.commit()

    def show_add_form(self):  # показывает форму добавления
        self.adding_book.load_shelves()
        self.adding_book.show()

    def show_change_form(self):  # показывает форму редактирования
        self.change_inf.load_shelves()
        self.change_inf.set_info(self.book_table.item(self.book_table.currentRow(), 1).text(),
                                 self.book_table.item(self.book_table.currentRow(), 3).text())
        self.change_inf.show()

    def change_item(self, name, author, year, genre, num_shelf, oldname):  # редактирование элементов
        ind_author = self.con.execute("""SELECT id FROM authors WHERE name = ? LIMIT 1""", [author]).fetchone()
        ind_genre = self.con.execute("""SELECT id FROM genres WHERE title = ? LIMIT 1""", [genre]).fetchone()
        id = self.con.execute("""SELECT id FROM books_inf WHERE name = ?""", [oldname]).fetchone()
        req = """UPDATE books_inf SET name = ?, author = ?,
        year = ?, genre = ?, shelf = ? WHERE id = ?"""
        self.con.execute(req, [name, ind_author, year, ind_genre, num_shelf, id])
        self.con.commit()
        self.find_books()

    def show_del_form(self):  # показывает форму удаления
        self.delete_book.show()

    def delete_item(self, id):  # удаление элементов
        req = """DELETE FROM books_inf WHERE id = ?"""
        self.con.execute(req, [id])
        self.con.commit()
        self.find_books()

    def take_info_shelves(self):  # взятие инф-ции о кол-ве полок
        cur = self.con.cursor()
        self.con.row_factory = lambda cur, row: row[0]
        self.sh = self.con.execute("""SELECT * FROM shelves""").fetchall()
        return self.sh

    def shelf_to_lv(self):  # добавление полки в список на экране
        self.list_shelf.addItem(str(len(self.take_info_shelves())))

    def add_new_shelf(self):  # добавление полки в бд
        cur = self.con.cursor()
        self.con.execute("""INSERT INTO shelves (id) VALUES (?)""", [len(self.take_info_shelves()) + 1])
        self.con.commit()
        self.shelf_to_lv()
        self.adding_book.load_shelves()
        self.change_inf.load_shelves()
        self.to_shelf.load_shelves()

    def no_shelf(self):  # удаление полки
        valid = QMessageBox.question(self, 'Удаление', 'Действительно удалить последнюю полку?',
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            self.num = len(self.take_info_shelves())
            temp = self.con.execute("""SELECT name FROM books_inf WHERE shelf = ?""", [self.num]).fetchall()
            if len(temp) != 0:  # если на полке есть книги, пользователю предлагается ввести номер полки
                self.delete_shelf.show()  # для перестановки
            self.con.execute("""DELETE FROM shelves WHERE id = ?""", [self.num])
            self.con.commit()
            self.list_shelf.takeItem(self.num - 1)

    def to_another_shelf(self, num_shelf):
        cur = self.con.cursor()
        self.con.execute("""UPDATE books_inf SET shelf = ? WHERE shelf = ?""", [num_shelf, self.num])
        self.con.commit()

    def show_more_a(self):  # показывает окно добавления авторов
        self.more_authors.show()

    def show_more_g(self):  # показывает окно добавления жанров
        self.more_genre.show()

    def author_add(self, name_a):  # добавление элементов в таблицу авторов
        cur = self.con.cursor()
        req = """INSERT INTO authors (name) VALUES (?)"""
        a = self.con.execute("""SELECT name FROM authors""").fetchall()
        if name_a in a:
            QMessageBox.warning(self, 'Добавление автора', 'Этот автор уже есть в базе данных')
            return
        self.con.execute(req, [name_a])
        self.con.commit()
        self.adding_book.new_author(name_a)
        self.change_inf.new_author(name_a)
        self.to_wl.new_author(name_a)
        self.to_shelf.new_author(name_a)

    def genre_add(self, title_g):  # добавление элементов в таблицу жанров
        cur = self.con.cursor()
        req = """INSERT INTO genres (title) VALUES (?)"""
        g = self.con.execute("""SELECT title FROM genres""").fetchall()
        if title_g in g:
            QMessageBox.warning(self, 'Добавление жанра', 'Этот жанр уже есть в базе данных')
            return
        self.con.execute(req, [title_g])
        self.con.commit()
        self.adding_book.new_genre(title_g)
        self.change_inf.new_genre(title_g)
        self.to_shelf.new_genre(title_g)

    def take_info_authors(self):  # взятие инф-ции для comboBox с авторами
        self.con = sqlite3.connect('books.sqlite')
        cur = self.con.cursor()
        self.con.row_factory = lambda cur, row: row[1]
        self.names_a = self.con.execute("""SELECT * FROM authors""").fetchall()
        return self.names_a

    def take_info_genres(self):  # взятие инф-ции для comboBox с жанрами
        self.con = sqlite3.connect('books.sqlite')
        cur = self.con.cursor()
        self.con.row_factory = lambda cur, row: row[1]
        self.titles_g = self.con.execute("""SELECT * FROM genres""").fetchall()
        return self.titles_g

    def current_author(self, name):  # взятие автора книги для редактирования
        cur = self.con.cursor()
        req = """SELECT name FROM authors WHERE id = (SELECT author FROM books_inf WHERE name = ?)"""
        author = self.con.execute(req, [name]).fetchone()
        return author

    def current_genre(self, name):  # взятие жанра книги для редактирования
        cur = self.con.cursor()
        genre = self.con.execute("""SELECT title FROM genres WHERE id = 
        (SELECT genre FROM books_inf WHERE name = ?)""", [name]).fetchone()
        return genre

    def current_shelf(self, name):  # взятие № полки для редактирования
        cur = self.con.cursor()
        shelf = self.con.execute("""SELECT shelf FROM books_inf WHERE name = ?""", [name]).fetchone()
        return str(shelf)

    def show_wl_form(self):  # показывает форму добавления в wishlist
        self.to_wl.show()

    def add_to_wishlist(self, name, author, price):  # добавление в таблицу wishlist
        cur = self.con.cursor()
        ind_author = self.con.execute("""SELECT id FROM authors WHERE name = ?""", [author]).fetchone()
        req = """INSERT INTO wishlist (name, author, price) VALUES (?, ?, ?)"""
        self.con.execute(req, [name, int(ind_author), int(price)])
        self.con.commit()

    def redraw_wl(self):  # перерисовывает таблицу wishlist на экране
        self.wishlist.clear()
        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()
        req = """SELECT w.id, w.name, a.name, w.price FROM wishlist as w, authors as a 
        WHERE w.author = a.id """
        res = con.execute(req).fetchall()
        self.wishlist.setRowCount(len(res))
        if len(res):
            self.wishlist.setColumnCount(len(res[0]))
        headers = ['id', 'Название', 'Автор', 'Цена']
        self.wishlist.setHorizontalHeaderLabels(headers)
        for i, elem in enumerate(res):
            for j, value in enumerate(elem):
                self.wishlist.setItem(i, j, QTableWidgetItem(str(value)))
        req_p = """SELECT price FROM wishlist"""
        prices = map(int, self.con.execute(req_p).fetchall())
        self.all_prices.display(str(sum(prices)))  # показывает общую цену всех книг

    def show_add_wl(self):  # показывает форму добавления из wishlist в основную таблицу
        row = list([i.row() for i in self.wishlist.selectedItems()])
        if not len(row):
            QMessageBox.warning(self, 'Поставить книги на полку',
                                'Выберите ячейки с информацией о книге, которую хотите поставить на полку')
            return
        row = row[0]
        info = []
        for i in range(self.wishlist.columnCount()):
            info.append(self.wishlist.item(row, i).text())
        self.to_shelf.set_info(info[0], info[1])
        self.to_shelf.show()

    def author_for_wl(self, name):  # взятие автора книги для добавления в основную таблицу
        cur = self.con.cursor()
        req = """SELECT name FROM authors WHERE id = (SELECT author FROM wishlist WHERE name = ?)"""
        author = self.con.execute(req, [name]).fetchone()
        return author

    def del_from_wl(self, id):  # удаление из wishlist
        cur = self.con.cursor()
        for i in range(self.wishlist.rowCount()):
            if self.wishlist.item(i, 1) == QTableWidgetItem(id):
                self.wishlist.removeRow(self.wishlist.item(i, 1).row())
        self.con.execute("""DELETE FROM wishlist WHERE id = ?""", [id])
        self.con.commit()

    def show_del_wl_form(self):  # показывается форма удаления книги из wishlist
        self.delete_from_wl.show()

    def del_book_wl(self, id):  # удаление книги из wishlist
        req = """DELETE FROM wishlist WHERE id = ?"""
        self.con.execute(req, [id])
        self.con.commit()
        self.redraw_wl()


class AddingBook(QMainWindow, Ui_add_form):  # класс формы добавления
    def __init__(self, parent=None):
        super(AddingBook, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_elem)
        self.more_authors.clicked.connect(self.parent().show_more_a)
        self.more_genres.clicked.connect(self.parent().show_more_g)
        self.more_shelfes.clicked.connect(self.parent().add_new_shelf)

        self.cB_author.addItems(self.parent().take_info_authors())
        self.cB_genre.addItems(self.parent().take_info_genres())

    def load_shelves(self):  # добавление полок в comboBox
        self.cB_shelf.clear()
        self.cB_shelf.addItems(map(str, self.parent().take_info_shelves()))

    def new_author(self, text):  # добавление нового автора в comboBox
        self.cB_author.addItem(text)

    def new_genre(self, text):  # добавление нового жанра в comboBox
        self.cB_genre.addItem(text.lower())

    def add_elem(self):  # передача инф-ции основному классу для добавления книги в бд
        name = self.name_inp.text()
        author = self.cB_author.currentText()
        year = self.year_inp.text()
        genre = self.cB_genre.currentText()
        num_shelf = self.cB_shelf.currentText()
        self.parent().add_item(name, author, year, genre, num_shelf)
        self.name_inp.clear()
        self.year_inp.clear()
        self.close()


class DeleteBook(QMainWindow, Ui_del_form):  # класс формы удаления
    def __init__(self, parent=None):
        super(DeleteBook, self).__init__(parent)
        self.setupUi(self)
        self.del_btn.clicked.connect(self.del_book)

    def del_book(self):  # передача инф-ции основному классу для удаления книги из бд
        id = self.lineEdit.text()
        valid = QMessageBox.question(self, 'Удаление', 'Действительно удалить элемент с id:' + str(id),
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.parent().delete_item(id)
        self.lineEdit.clear()
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
        self.more_shelfes.clicked.connect(self.parent().add_new_shelf)

        self.cB_author.addItems(self.parent().take_info_authors())
        self.cB_genre.addItems(self.parent().take_info_genres())
        self.cB_shelf.addItems(map(str, self.parent().take_info_shelves()))

    def load_shelves(self):  # добавление полок в comboBox
        self.cB_shelf.clear()
        self.cB_shelf.addItems(map(str, self.parent().take_info_shelves()))

    def new_author(self, text):  # добавление нового автора в comboBox
        self.cB_author.addItem(text)

    def new_genre(self, text):  # добавление нового жанра в comboBox
        self.cB_genre.addItem(text)

    def set_info(self, name, year):  # установка инф-ции для изменений
        self.name = name
        self.author = self.parent().current_author(name)
        self.year = year
        self.genre = self.parent().current_genre(name)
        self.num_shelf = self.parent().current_shelf(name)
        self.name_inp.setText(name)
        self.cB_author.setCurrentText(self.parent().current_author(name))
        self.year_inp.setText(year)
        self.cB_genre.setCurrentText(self.parent().current_genre(name))
        self.cB_shelf.setCurrentText(self.parent().current_shelf(name))

    def change_info(self):  # передача инф-ции основному классу для редактирования
        oldname = self.name
        name = self.name_inp.text()
        author = self.cB_author.currentText()
        year = self.year_inp.text()
        genre = self.cB_genre.currentText()
        num_shelf = self.cB_shelf.currentText()
        self.parent().change_item(name, author, year, genre, num_shelf, oldname)
        self.name_inp.clear()
        self.year_inp.clear()
        self.close()


class AddAuthor(Ui_more_authors, QMainWindow):  # класс формы добавления авторов
    def __init__(self, parent=None):
        super(AddAuthor, self).__init__(parent)
        self.setupUi(self)
        self.save_new_a.clicked.connect(self.new_elem)

    def new_elem(self):  # передача инф-ции основному классу для добавления автора в бд
        name_a = self.author_inp.text()
        self.parent().author_add(name_a)
        self.author_inp.clear()
        self.close()


class AddGenre(Ui_more_genres, QMainWindow):  # класс формы добавления жанров
    def __init__(self, parent=None):
        super(AddGenre, self).__init__(parent)
        self.setupUi(self)
        self.save_new_g.clicked.connect(self.new_elem)

    def new_elem(self):  # передача инф-ции основному классу для добавления жанра в бд
        title_g = self.genre_inp.text().lower()
        self.parent().genre_add(title_g)
        self.genre_inp.clear()
        self.close()


class ToWishlist(QMainWindow, Ui_wl_form):  # класс формы добавления в wishlist
    def __init__(self, parent=None):
        super(ToWishlist, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_to_wl)
        self.more_authors.clicked.connect(self.parent().show_more_a)
        self.cB_author.addItems(self.parent().take_info_authors())

    def new_author(self, text):  # добавление автора в comboBox
        self.cB_author.addItem(text)

    def add_to_wl(self):  # передача инф-ции основному классу для добавления книги в wishlist
        name = self.name_inp.text()
        author = self.cB_author.currentText()
        price = self.price_inp.text()
        self.parent().add_to_wishlist(name, author, price)
        self.parent().redraw_wl()
        self.name_inp.clear()
        self.price_inp.clear()
        self.close()


class FromWlToShelf(QMainWindow, Ui_add_form):  # класс формы перенесения книги из wishlist в основную
    def __init__(self, parent=None):  # таблицу books_inf
        super(FromWlToShelf, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_book)
        self.more_authors.clicked.connect(self.parent().show_more_a)
        self.cB_author.addItems(self.parent().take_info_authors())
        self.cB_genre.addItems(self.parent().take_info_genres())
        self.cB_shelf.addItems(map(str, self.parent().take_info_shelves()))
        self.more_genres.clicked.connect(self.parent().show_more_g)
        self.more_shelfes.clicked.connect(self.parent().add_new_shelf)
        self.id = 0

    def load_shelves(self):  # добавление полок в comboBox
        self.cB_shelf.clear()
        self.cB_shelf.addItems(map(str, self.parent().take_info_shelves()))

    def new_author(self, text):  # добавление автора в comboBox
        self.cB_author.addItem(text)

    def new_genre(self, text):  # добавление жанра в comboBox
        self.cB_genre.addItem(text)

    def set_info(self, id, name):  # установка инф-ции для добавления в основную таблицу
        self.id = int(id)
        self.name_inp.setText(name)
        self.cB_author.setCurrentText(self.parent().author_for_wl(name))

    def add_book(self):  # передача инф-ции основному классу для добавления книги в основную таблицу
        name = self.name_inp.text()
        author = self.cB_author.currentText()
        year = self.year_inp.text()
        genre = self.cB_genre.currentText()
        num_shelf = self.cB_shelf.currentText()
        self.parent().add_item(name, author, year, genre, num_shelf)
        self.parent().del_from_wl(self.id)
        self.name_inp.clear()
        self.year_inp.clear()
        self.parent().redraw_wl()
        self.close()


class DeleteShelf(QMainWindow, Ui_del_shelf_form):  # класс формы удаления полки
    def __init__(self, parent=None):
        super(DeleteShelf, self).__init__(parent)
        self.setupUi(self)
        self.del_btn.clicked.connect(self.del_shelf)

    def del_shelf(self):  # передача инф-ции для удаления полки и перенесения книг с ней на выбранную
        num = self.lineEdit.text()
        self.parent().to_another_shelf(num)
        self.lineEdit.clear()
        self.close()


class DeleteFromWl(QMainWindow, Ui_del_form):   # класс удаления книги из wishlist
    def __init__(self, parent=None):
        super(DeleteFromWl, self).__init__(parent)
        self.setupUi(self)
        self.del_btn.clicked.connect(self.del_book)

    def del_book(self):
        id = self.lineEdit.text()
        valid = QMessageBox.question(self, 'Удаление', 'Действительно удалить элемент с id:' + str(id),
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.parent().del_book_wl(id)
        self.lineEdit.clear()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWork()
    mw.show()
    sys.exit(app.exec())
