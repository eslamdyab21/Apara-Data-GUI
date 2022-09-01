# This Python file uses the following encoding: utf-8
#import imp
import os
from pathlib import Path
import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QObject, QThread, pyqtSignal

import scripts.Bulk_Converter_to_CSV as Bulk_Converter_to_CSV
import scripts.Xlsx_to_Csv as Xlsx_to_Csv
import scripts.Large_File_Splitter as Large_File_Splitter


from ui import Ui_MainWindow




# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self,Page3_LargeFileSplitter_fname, LabelStatus_Page3_LargeFileSplitter):
        """Long-running task."""
        Large_File_Splitter.DirctoryPathToLargeFilesToSplit(Page3_LargeFileSplitter_fname, LabelStatus_Page3_LargeFileSplitter, QApplication)
        LabelStatus_Page3_LargeFileSplitter.setText("Done")
        
        self.finished.emit()



class Window(QMainWindow):
    def __init__(self,ui):
        QMainWindow.__init__(self)
        self.ui = ui
        self.Page1_BulckConverter_fname = ''
        self.Page2_XlsxToSCV_fname = ''
        self.Page3_LargeFileSplitter_fname = ''
        self.SetPage1BulkConverter()

        ############################PAGE1-BULCK_CONERTER##########################
        self.ui.BtnBulkConverter.clicked.connect(self.SetPage1BulkConverter)
        self.ui.BtnBrows_Page1_BulckConverter.clicked.connect(self.Page1_BulckConverter_BrowsFolders)
        self.ui.BtnConvert_Page1_BulckConverter.clicked.connect(self.Page1_BulckConverter_CallScript)
        ##########################################################################


        ############################PAGE2-XLSX_CONERTER##########################
        self.ui.BtnXlsxToCSV.clicked.connect(self.SetPage2XlsxToCSV)
        self.ui.BtnBrows_Page2_XlsxToSCV.clicked.connect(self.Page2_XlsxToSCV_BrowsFolders)
        self.ui.BtnConvert_Page2_XlsxToSCV.clicked.connect(self.Page2_XlsxToSCV_CallScript)
        ##########################################################################
        


        ############################PAGE3-LARGE-SPLITER##########################
        self.ui.BtnLargeFileSplitter.clicked.connect(self.SetPage3LargeFileSplitter)
        self.ui.BtnBrows_Page3_LargeFileSplitter.clicked.connect(self.Page3_LargeFileSplitter_BrowsFolders)
        self.ui.BtnConvert_Page3_LargeFileSplitter.clicked.connect(self.Page3_LargeFileSplitter_CallScript)
        ##########################################################################
        


    
    ############################PAGE1-BULCK_CONERTER##########################
    def SetPage1BulkConverter(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.label_title_bar_top.setText("Bulk Converter")

    def Page1_BulckConverter_BrowsFolders(self):
        self.Page1_BulckConverter_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", "/home/")
        self.ui.LineEditPath_Page1.setText(self.Page1_BulckConverter_fname)

    def Page1_BulckConverter_CallScript(self):
        self.ui.LabelStatus_Page1_BulkConvert.setText("Wait......")
        QApplication.processEvents()
        status = Bulk_Converter_to_CSV.DirctoryPathToXlxsFiles(self.Page1_BulckConverter_fname)
        print(status)
        self.ui.LabelStatus_Page1_BulkConvert.setText("Done")
    ##########################################################################




    ############################PAGE2-XLSX_CONERTER##########################
    def SetPage2XlsxToCSV(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.label_title_bar_top.setText("Xlsx Converter")

    def Page2_XlsxToSCV_BrowsFolders(self):
        self.Page2_XlsxToSCV_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", "/home/")
        self.ui.LineEditPath_Page2.setText(self.Page2_XlsxToSCV_fname)

    def Page2_XlsxToSCV_CallScript(self):
        self.ui.LabelStatus_Page2_XlsxToCSV.setText("Wait......")
        QApplication.processEvents()
        status = Xlsx_to_Csv.DirctoryPathToXlxsFiles(self.Page2_XlsxToSCV_fname)
        self.ui.LabelStatus_Page2_XlsxToCSV.setText("Done")
    ##########################################################################



    ############################PAGE3-LARGE-SPLITER##########################
    def SetPage3LargeFileSplitter(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.label_title_bar_top.setText("Large Files Splitter")

    def Page3_LargeFileSplitter_BrowsFolders(self):
        self.Page3_LargeFileSplitter_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", "/home/")
        self.ui.LineEditPath_Page3.setText(self.Page3_LargeFileSplitter_fname)

    def Page3_LargeFileSplitter_CallScript(self):
        self.ui.LabelStatus_Page3_LargeFileSplitter.setText("Wait......")
        QApplication.processEvents()

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run(self.Page3_LargeFileSplitter_fname, self.ui.LabelStatus_Page3_LargeFileSplitter))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.ui.BtnConvert_Page3_LargeFileSplitter.setEnabled(False)
        self.thread.finished.connect(lambda: self.ui.BtnConvert_Page3_LargeFileSplitter.setEnabled(True))
        #self.thread.finished.connect(lambda: self.stepLabel.setText("Long-Running Step: 0"))

        
    ##########################################################################


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(win)
    win.show()
    my_instance = Window(ui)
    
    sys.exit(app.exec_())