import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from del_form2 import Ui_del_form
from add_form import Ui_add_form
from personal_library import Ui_list_shelfes


class MainWork(Ui_list_shelfes, QMainWindow):  # основной класс
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.row_shelfes = 0
        self.shelf = 1

    def initUi(self):
        self.add_shelf.clicked.connect(self.new_shelf)
        self.del_shelf.clicked.connect(self.no_shelf)

    def new_shelf(self):
        self.table_shelfes.setItem(self.row_shelfes, 0, self.shelf)   # исправить
        self.row_shelfes += 1
        self.shelf += 1

    def no_shelf(self):
        pass


class AddingBook(QWidget, Ui_add_form):  # класс формы добавления
    def __init__(self, parent=None):
        super(AddingBook, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_book)

    def add_book(self):
        name = self.name_inp.text()
        author = self.author_inp.text()
        year = self.year_inp.text()
        genre = self.genre_inp.text()
        num_shelf = self.schelf_inp.text()
        self.parent().add_item(name, author, year, genre, num_shelf)
        self.close()


class DeleteBook(QWidget, Ui_del_form):  # класс формы удаления
    def __init__(self, parent=None):
        super(DeleteBook, self).__init__(parent)
        self.setupUi(self)
        self.del_btn.clicked.connect(self.del_book)

    def del_book(self):
        id = self.lineEdit.text()
        valid = QMessageBox.question(self, 'Вопрос', 'Действительно удалить элемент с id:' + str(id),
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.parent().delete_item(id)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWork()
    mw.show()
    sys.exit(app.exec())
