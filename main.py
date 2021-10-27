import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from del_form import Ui_del_form
from add_form import  Ui_add_form
from personal_library import Ui_list_shelfes


class MainWork(Ui_list_shelfes, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWork()
    mw.show()
    sys.exit(app.exec())