# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'del_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_del_form(object):
    def setupUi(self, del_form):
        del_form.setObjectName("del_form")
        del_form.resize(243, 206)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(del_form.sizePolicy().hasHeightForWidth())
        del_form.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 245, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 245, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 245, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 245, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        del_form.setPalette(palette)
        self.lineEdit = QtWidgets.QLineEdit(del_form)
        self.lineEdit.setGeometry(QtCore.QRect(40, 80, 151, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(del_form)
        self.label.setGeometry(QtCore.QRect(40, 20, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setToolTipDuration(-1)
        self.label.setObjectName("label")
        self.del_btn = QtWidgets.QPushButton(del_form)
        self.del_btn.setGeometry(QtCore.QRect(40, 140, 151, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.del_btn.setFont(font)
        self.del_btn.setAutoRepeatInterval(100)
        self.del_btn.setObjectName("del_btn")

        self.retranslateUi(del_form)
        QtCore.QMetaObject.connectSlotsByName(del_form)

    def retranslateUi(self, del_form):
        _translate = QtCore.QCoreApplication.translate
        del_form.setWindowTitle(_translate("del_form", "Удаление элемента"))
        self.label.setText(_translate("del_form", "Введите id элемента"))
        self.del_btn.setText(_translate("del_form", "Удалить элемент"))
