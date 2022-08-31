# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QFile

        
from ui import Ui_MainWindow

class Window():
    def __init__(self,ui):
        self.ui = ui
        self.Page1BulkConverter()

        self.ui.BtnBrows_Page1.clicked.connect(self.change_txt)

        self.ui.BtnBulkConverter.clicked.connect(self.Page1BulkConverter)
        self.ui.BtnSecond.clicked.connect(self.Page2Second)
        

    def change_txt(self):
        self.ui.LineEditPath.setText("What?!!!")
    
    def Page1BulkConverter(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.label_title_bar_top.setText("Bulk Converter")

    def Page2Second(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.label_title_bar_top.setText("Second")



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(win)
    win.show()
    my_instance = Window(ui)
    
    sys.exit(app.exec_())