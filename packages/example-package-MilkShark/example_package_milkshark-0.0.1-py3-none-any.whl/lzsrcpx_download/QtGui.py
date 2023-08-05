from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRegExp
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QRegExpValidator
# import os, MyLineEdit, ExcelPreview, WindowSelector, Utils, WorkThreads, pyperclip


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    mainW = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainW)
    mainW.show()
    mainW.setWindowTitle("♥lzsrcpx考试辅助器♥")

    sys.exit(app.exec_())