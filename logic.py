# This Python file uses the following encoding: utf-8
#import imp
import imp
from operator import imod
import os
from pathlib import Path
import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve

import scripts.Bulk_Converter_to_CSV as Bulk_Converter_to_CSV
import scripts.Xlsx_to_Csv as Xlsx_to_Csv
import scripts.Large_File_Splitter as Large_File_Splitter
import scripts.merge_small_files_under_1mb as merge_small_files_under_1mb
import scripts.Extract_Geos as Extract_Geos
import scripts.Merge_Geos as Merge_Geos
import scripts.Validate_Emails_Spam as Validate_Emails_Spam
import scripts.MX_Domain_Validator as MX_Domain_Validator
import scripts.Numbers_Extractor as Numbers_Extractor
import scripts.TxtTOcsv as TxtTOcsv
import scripts.url_checker as url_checker
import scripts.email_domain_search as email_domain_search

from ui import Ui_MainWindow



defult_style = "QPushButton {\n""    border: 2px solid rgb(52, 59, 72);\n""    /*border-radius: 5px;    */\n""    background-color: rgb(52, 59, 72);\n""}\n""QPushButton:hover {\n""    background-color: rgb(57, 65, 80);\n""    border: 2px solid rgb(61, 70, 86);\n""}\n""QPushButton:pressed {    \n""    background-color: rgb(35, 40, 49);\n""    border: 2px solid rgb(43, 50, 61);\n""}"
pressed_style = "QPushButton {\n""    border: 0px solid rgb(52, 59, 72);\n""    /*border-radius: 5px;    */\n""    background-color: rgb(80,80,90);\n""}"
current_directory = os.getcwd()



class UIFunctions():
    ## ==> GLOBALS
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

    def __init__(self,ui):
        self.ui = ui
    

    def toggleMenu(self, maxWidth):
        # GET WIDTH
        width = self.ui.frame_left_menu.width()
        maxExtend = maxWidth
        standard = 150

        # SET MAX WIDTH
        if width == standard:
            widthExtended = 0
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()



# Create a worker class
class Worker1(QThread):
    update_plainTextEdit_Page3 = pyqtSignal(str)

    def __init__(self,Page3_LargeFileSplitter_fname):
        QThread.__init__(self)
        self.Page3_LargeFileSplitter_fname = Page3_LargeFileSplitter_fname

    def run(self):
        """Long-running task."""
        val = Large_File_Splitter.DirctoryPathToLargeFilesToSplit(self.Page3_LargeFileSplitter_fname)        
        
        for value in val:
            self.update_plainTextEdit_Page3.emit(value)
            #print(value)



# Create a worker2 class
class Worker2(QThread):
    update_plainTextEdit_Page6 = pyqtSignal(str)

    def __init__(self,MX_or_Emails, Page6_Validation_fname):
        QThread.__init__(self)
        self.MX_or_Emails = MX_or_Emails
        self.Page6_Validation_fname = Page6_Validation_fname
        

    def run(self):
        """Long-running task."""
        if(self.MX_or_Emails) == 0:
            val = Validate_Emails_Spam.DirctoryPathToValidation(self.Page6_Validation_fname)
        elif(self.MX_or_Emails == 1):
            val = MX_Domain_Validator.DirctoryPathToValidation(self.Page6_Validation_fname)

        for value in val:
            self.update_plainTextEdit_Page6.emit(value)
            print(value)

    
# Create a Worker3_extract_numbers class
class Worker3_extract_numbers(QThread):
    update_plainTextEdit_Page7 = pyqtSignal(str)

    def __init__(self , Page7_Validation_fname):
        QThread.__init__(self)
        self.Page7_Validation_fname = Page7_Validation_fname
        

    def run(self):
        """Long-running task."""
        val = Numbers_Extractor.DirctoryPathToNumbersExtract(self.Page7_Validation_fname)

        for value in val:
            self.update_plainTextEdit_Page7.emit(value)
            #print(value)


# Create a Worker4_geos class
class Worker4_geos(QThread):
    update_plainTextEdit_Page5 = pyqtSignal(str)

    def __init__(self , Extract_or_Merge, Page5_Geos_fname):
        QThread.__init__(self)
        self.Extract_or_Merge = Extract_or_Merge
        self.Page5_Geos_fname = Page5_Geos_fname
        

    def run(self):
        """Long-running task."""
        if self.Extract_or_Merge == 0:
            val = Extract_Geos.DirctoryPathToGeo(self.Page5_Geos_fname)
        elif self.Extract_or_Merge == 1:
            val = Merge_Geos.DirctoryPathToGeo(self.Page5_Geos_fname)

        for value in val:
            self.update_plainTextEdit_Page5.emit(value)
            #print(value)


# Create a Worker5_textTocsv class
class Worker5_textTocsv(QThread):
    update_plainTextEdit_Page8 = pyqtSignal(str)

    def __init__(self , Page8_TextToCsv_fname):
        QThread.__init__(self)
        self.Page8_TextToCsv_fname = Page8_TextToCsv_fname
        

    def run(self):
        """Long-running task."""
        val = TxtTOcsv.DirctoryPathToTextToCsv(self.Page8_TextToCsv_fname)

        for value in val:
            self.update_plainTextEdit_Page8.emit(value)
            #print(value)




# Create a Worker6_urlChecker class
class Worker6_urlChecker(QThread):
    update_plainTextEdit_Page9 = pyqtSignal(str)

    def __init__(self , Page8_urlChecker_url):
        QThread.__init__(self)
        self.Page8_urlChecker_url = Page8_urlChecker_url
        

    def run(self):
        """Long-running task."""
        val = url_checker.UrlToCheck(self.Page8_urlChecker_url)

        for value in val:
            self.update_plainTextEdit_Page9.emit(value)
            self.update_plainTextEdit_Page9.emit('------------------------------------------------------------------------------------------------')
            #print(value)



# Create a Worker7_EmailDomainSearch class
class Worker7_EmailDomainSearch(QThread):
    update_plainTextEdit_Page10 = pyqtSignal(str)

    def __init__(self , Page10_EmailDomainSearch_fname, EmailOrDomain):
        QThread.__init__(self)
        self.Page10_EmailDomainSearch_fname = Page10_EmailDomainSearch_fname
        self.EmailOrDomain = EmailOrDomain
        

    def run(self):
        """Long-running task."""
        val = email_domain_search.DirctoryPathToEmailDomainSearch(self.Page10_EmailDomainSearch_fname, self.EmailOrDomain)

        for value in val:
            self.update_plainTextEdit_Page10.emit(value)
            #print(value)


class Window(QMainWindow):
    def __init__(self,ui):
        QMainWindow.__init__(self)
        self.ui = ui
        self.Page1_BulckConverter_fname = ''
        self.Page2_XlsxToSCV_fname = ''
        self.Page3_LargeFileSplitter_fname = ''
        self.Page4_MergeSmall_fname = ''
        self.Page4_MergeSmall_small_file_max_size_kb = 1000
        self.Page4_MergeSmall_merged_file_max_size_mb = 49
        self.Page5_Geos_fname = ''
        self.SetPage1BulkConverter()
        UIFunctions.toggleMenu(self, 220)



        ############################SIDE-BAR-ANNIMATION##########################
        self.ui.btn_toggle_menu.clicked.connect(self.SideBar)
        ##########################################################################



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
        

        ############################PAGE4-MERGE-SMALL#############################
        self.ui.BtnMergeSmallFiles.clicked.connect(self.SetPage4MergeSmallFiles)
        self.ui.BtnBrows_Page4_MergeSmall.clicked.connect(self.Page4_MergeSmall_BrowsFolders)
        self.ui.BtnMerge_Page4_MergeSmall.clicked.connect(self.Page4_MergeSmall_CallScript)
        ##########################################################################


        ############################PAGE5-GEOS###################################
        self.ui.BtnGeos.clicked.connect(self.SetPage5Geos)
        self.ui.BtnBrows_Page5_Geos.clicked.connect(self.Page5_Geos_BrowsFolders)
        self.ui.BtnExtractGeos_Page5.clicked.connect(self.Page5_ExtractGeo_CallScript)
        self.ui.BtnMergeGeos_Page5.clicked.connect(self.Page5_MergeGeo_CallScript)
        ##########################################################################

        ############################PAGE6-Validation##############################
        self.ui.BtnEmailValidation.clicked.connect(self.SetPage6Validation)
        self.ui.BtnBrows_Page6_Validation.clicked.connect(self.Page6_Validation_BrowsFolders)
        self.ui.BtnValidateEmailSpam_Page6.clicked.connect(self.Page6_ValidateEmailSpam_CallScript)
        self.ui.BtnValidateMxDomain_Page6.clicked.connect(self.Page6_ValidateMxDomain_CallScript)
        ##########################################################################

        ############################PAGE7-Number-Extractor########################
        self.ui.BtnExtractNumbers.clicked.connect(self.SetPageExtractNumbers)
        self.ui.BtnBrows_Page7_ExtractNumbers.clicked.connect(self.Page7_ExtractNumbers_BrowsFolders)
        self.ui.BtnConvert_Page7_ExtractNumbers.clicked.connect(self.Page7_ExtractNumbers_CallScript)
        ##########################################################################

        ############################PAGE8-Text-To-Csv#############################
        self.ui.BtnTextToCsv.clicked.connect(self.SetPageTextToCsv)
        self.ui.BtnBrows_Page8_TextToCsv.clicked.connect(self.Page8_TextToCsv_BrowsFolders)
        self.ui.BtnConvert_Page8_TextToCsv.clicked.connect(self.Page8_TextToCsv_CallScript)
        ##########################################################################

        ############################PAGE9-Url-Check###############################
        self.ui.BtnUrlChecker.clicked.connect(self.SetPageUrlChecker)
        self.ui.BtnConvert_Page9_UrlCheck.clicked.connect(self.Page9_UrlCheck_CallScript)
        ##########################################################################


        #########################PAGE10-Email-Domain-Search#######################
        self.ui.BtnEmailDomainSearch.clicked.connect(self.SetPage10EmailDomainSearch)
        self.ui.BtnBrows_Page10_EmailDomailSearch.clicked.connect(self.Page10_EmailDomailSearch_BrowsFolders)
        self.ui.BtnConvert_Page10_EmailDomainSearch.clicked.connect(self.Page10_EmailDomainSearch_CallScript)
        ##########################################################################

    

    def BtnPressed(self,lst):
        if lst[0] == 1:
            self.ui.BtnBulkConverter.setStyleSheet(defult_style)
        if lst[1] == 1:
            self.ui.BtnXlsxToCSV.setStyleSheet(defult_style)
        if lst[2] == 1:
            self.ui.BtnLargeFileSplitter.setStyleSheet(defult_style)
        if lst[3] == 1:
            self.ui.BtnMergeSmallFiles.setStyleSheet(defult_style)
        if lst[4] == 1:
            self.ui.BtnGeos.setStyleSheet(defult_style)
        if lst[5] == 1:
            self.ui.BtnEmailValidation.setStyleSheet(defult_style)
        if lst[6] == 1:
            self.ui.BtnExtractNumbers.setStyleSheet(defult_style)
        if lst[7] == 1:
            self.ui.BtnTextToCsv.setStyleSheet(defult_style)
        if lst[8] == 1:
            self.ui.BtnUrlChecker.setStyleSheet(defult_style)
        if lst[9] == 1:
            self.ui.BtnEmailDomainSearch.setStyleSheet(defult_style)


        #if lst[5] == 1:
        #    self.ui.BtnBulkConverter.setStyleSheet(self.defult)

        self.ui.BtnBulkConverter.setEnabled(lst[0])
        self.ui.BtnXlsxToCSV.setEnabled(lst[1])
        self.ui.BtnLargeFileSplitter.setEnabled(lst[2])
        self.ui.BtnMergeSmallFiles.setEnabled(lst[3])
        self.ui.BtnGeos.setEnabled(lst[4])
        self.ui.BtnEmailValidation.setEnabled(lst[5])
        self.ui.BtnExtractNumbers.setEnabled(lst[6])
        self.ui.BtnTextToCsv.setEnabled(lst[7])
        self.ui.BtnUrlChecker.setEnabled(lst[8])
        self.ui.BtnEmailDomainSearch.setEnabled(lst[9])





    ############################SIDE-BAR-ANNIMATION##########################
    def SideBar(self):
        UIFunctions.toggleMenu(self, 220)
    ##########################################################################



    ############################PAGE1-BULCK_CONERTER##########################
    def SetPage1BulkConverter(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.label_title_bar_top.setText("Bulk Converter")
        self.ui.BtnBulkConverter.setStyleSheet(pressed_style)
        self.BtnPressed([0,1,1,1,1,1,1,1,1,1])

    def Page1_BulckConverter_BrowsFolders(self):
        self.Page1_BulckConverter_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
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
        self.ui.BtnXlsxToCSV.setStyleSheet(pressed_style)
        self.BtnPressed([1,0,1,1,1,1,1,1,1,1])

    def Page2_XlsxToSCV_BrowsFolders(self):
        self.Page2_XlsxToSCV_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
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
        self.ui.BtnLargeFileSplitter.setStyleSheet(pressed_style)
        self.BtnPressed([1,1,0,1,1,1,1,1,1,1])

    def Page3_LargeFileSplitter_BrowsFolders(self):
        self.Page3_LargeFileSplitter_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
        self.ui.LineEditPath_Page3.setText(self.Page3_LargeFileSplitter_fname)

    def Page3_LargeFileSplitter_CallScript(self):
        self.ui.plainTextEdit_Page3.clear()
        self.ui.plainTextEdit_Page3.appendPlainText("Wait......")
        QApplication.processEvents()

        #Create a QThread object
        self.worker1 = Worker1(self.Page3_LargeFileSplitter_fname)

        self.worker1.start()

        self.worker1.finished.connect(self.evt_worker1_thread_finished)
        self.worker1.update_plainTextEdit_Page3.connect(self.evt_update_plainTextEdit_Page3)

    def evt_worker1_thread_finished(self):
        self.ui.plainTextEdit_Page3.appendPlainText("Done")

    def evt_update_plainTextEdit_Page3(self, value):
        self.ui.plainTextEdit_Page3.appendPlainText(value)
    ##########################################################################




    ############################PAGE4-MERGE-SMALL#############################
    def SetPage4MergeSmallFiles(self):
        
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.label_title_bar_top.setText("Merge Small Files")
        self.ui.BtnMergeSmallFiles.setStyleSheet(pressed_style)
        self.BtnPressed([1,1,1,0,1,1,1,1,1,1])

    def Page4_MergeSmall_BrowsFolders(self):
        self.Page4_MergeSmall_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
        self.ui.LineEditPath_Page4.setText(self.Page4_MergeSmall_fname)

    def Page4_MergeSmall_CallScript(self):
        self.ui.plainTextEdit_Page4.clear()
        self.ui.plainTextEdit_Page4.appendPlainText("Wait......")
        QApplication.processEvents()
        self.Page4_MergeSmall_small_file_max_size_kb = int(self.ui.LineEdit_Page4_SmallFileMaxSize.text())
        self.Page4_MergeSmall_merged_file_max_size_mb = float(self.ui.LineEdit_Page4_MergedFileMaxSize.text())
        merge_small_files_under_1mb.DirctoryPathToMergeSmallFiles(self.Page4_MergeSmall_fname, self.Page4_MergeSmall_small_file_max_size_kb, self.Page4_MergeSmall_merged_file_max_size_mb, self.ui.plainTextEdit_Page4, QApplication)
        self.ui.plainTextEdit_Page4.appendPlainText("Done")
    ##########################################################################





    ############################PAGE5-GEOS###################################
    def SetPage5Geos(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.label_title_bar_top.setText("Geos Extractor and Merger")
        self.ui.BtnGeos.setStyleSheet(pressed_style)
        self.BtnPressed([1,1,1,1,0,1,1,1,1,1])

    def Page5_Geos_BrowsFolders(self):
        self.Page5_Geos_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
        self.ui.LineEditPath_Page5.setText(self.Page5_Geos_fname)

    def Page5_ExtractGeo_CallScript(self):

        #Create a QThread object
        self.ui.plainTextEdit_Page5.clear()
        self.worker4_geos = Worker4_geos(0,self.Page5_Geos_fname)

        self.worker4_geos.start()

        self.ui.plainTextEdit_Page5.appendPlainText("Wait......")
        QApplication.processEvents()

        self.worker4_geos.finished.connect(self.evt_worker4_geos_thread_finished)
        self.worker4_geos.update_plainTextEdit_Page5.connect(self.evt_update_plainTextEdit_Page5)


    def Page5_MergeGeo_CallScript(self):
         #Create a QThread object
        self.ui.plainTextEdit_Page5.clear()
        self.worker4_geos = Worker4_geos(1,self.Page5_Geos_fname)

        self.worker4_geos.start()

        self.ui.plainTextEdit_Page5.appendPlainText("Wait......")
        QApplication.processEvents()

        self.worker4_geos.finished.connect(self.evt_worker4_geos_thread_finished)
        self.worker4_geos.update_plainTextEdit_Page5.connect(self.evt_update_plainTextEdit_Page5)

    
    def evt_worker4_geos_thread_finished(self):
        self.ui.plainTextEdit_Page5.appendPlainText("Done")

    def evt_update_plainTextEdit_Page5(self, value):
        self.ui.plainTextEdit_Page5.appendPlainText(value)
    ##########################################################################




    ############################PAGE6-Validation##############################
    def SetPage6Validation(self):
        self.ui.stackedWidget.setCurrentIndex(6)
        self.ui.label_title_bar_top.setText("Email Validation")
        self.ui.BtnEmailValidation.setStyleSheet(pressed_style)
        self.BtnPressed([1,1,1,1,1,0,1,1,1,1])

    def Page6_Validation_BrowsFolders(self):
        self.Page6_Validation_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
        self.ui.LineEditPath_Page6.setText(self.Page6_Validation_fname)

    def Page6_ValidateEmailSpam_CallScript(self):
        self.ui.plainTextEdit_Page6.clear()
        #Create a QThread object
        self.worker2 = Worker2(0, self.Page6_Validation_fname)

        self.worker2.start()

        self.worker2.finished.connect(self.evt_worker2_thread_finished)
        self.worker2.update_plainTextEdit_Page6.connect(self.evt_update_plainTextEdit_Page6)
    
    def Page6_ValidateMxDomain_CallScript(self):
        self.ui.plainTextEdit_Page6.clear()
        QApplication.processEvents()
        #Create a QThread object
        self.worker2 = Worker2(1, self.Page6_Validation_fname)

        self.worker2.start()

        self.worker2.finished.connect(self.evt_worker2_thread_finished)
        self.worker2.update_plainTextEdit_Page6.connect(self.evt_update_plainTextEdit_Page6)

    def evt_worker2_thread_finished(self):
        self.ui.plainTextEdit_Page6.appendPlainText("Done")

    def evt_update_plainTextEdit_Page6(self, value):
        self.ui.plainTextEdit_Page6.appendPlainText(value)
    ##########################################################################





    ############################PAGE7-Number-Extractor#########@##############
    def SetPageExtractNumbers(self):
        self.ui.stackedWidget.setCurrentIndex(7)
        self.ui.label_title_bar_top.setText("Extract Numbers")
        self.ui.BtnExtractNumbers.setStyleSheet(pressed_style)
        self.BtnPressed([1,1,1,1,1,1,0,1,1,1])

    def Page7_ExtractNumbers_BrowsFolders(self):
        self.Page7_Validation_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
        self.ui.LineEditPath_Page7.setText(self.Page7_Validation_fname)

    def Page7_ExtractNumbers_CallScript(self):
        self.ui.plainTextEdit_Page7.clear()
        QApplication.processEvents()

        #Create a QThread object
        self.worker3_extract_numbers = Worker3_extract_numbers(self.Page7_Validation_fname)

        self.worker3_extract_numbers.start()

        self.worker3_extract_numbers.finished.connect(self.evt_worker3_extract_numbers_thread_finished)
        self.worker3_extract_numbers.update_plainTextEdit_Page7.connect(self.evt_update_plainTextEdit_Page7)

    def evt_worker3_extract_numbers_thread_finished(self):
        self.ui.plainTextEdit_Page7.appendPlainText("Done")

    def evt_update_plainTextEdit_Page7(self, value):
        self.ui.plainTextEdit_Page7.appendPlainText(value)
    ##########################################################################



    ############################PAGE8-Text-To-Csv#############################
        # self.ui.BtnTextToCsv.clicked.connect(self.SetPageTextToCsv)
        # self.ui.BtnBrows_Page8_TextToCsv.clicked.connect(self.Page8_TextToCsv_BrowsFolders)
        # self.ui.BtnConvert_Page8_TextToCsv.clicked.connect(self.Page8_TextToCsv_CallScript)
    ##########################################################################
    ############################PAGE8-Text-To-Csv#############################
    def SetPageTextToCsv(self):
        self.ui.stackedWidget.setCurrentIndex(8)
        self.ui.label_title_bar_top.setText("Text To CSV")
        self.ui.BtnTextToCsv.setStyleSheet(pressed_style)
        self.BtnPressed([1,1,1,1,1,1,1,0,1,1])
    
    def Page8_TextToCsv_BrowsFolders(self):
        self.Page8_TextToCsv_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
        self.ui.LineEditPath_Page8.setText(self.Page8_TextToCsv_fname)

    def Page8_TextToCsv_CallScript(self):
        self.ui.plainTextEdit_Page8.clear()
        QApplication.processEvents()

        #Create a QThread object
        self.worker5_textTocsv = Worker5_textTocsv(self.Page8_TextToCsv_fname)

        self.worker5_textTocsv.start()

        self.worker5_textTocsv.finished.connect(self.evt_Worker5_textTocsv_thread_finished)
        self.worker5_textTocsv.update_plainTextEdit_Page8.connect(self.evt_update_plainTextEdit_Page8)

    def evt_Worker5_textTocsv_thread_finished(self):
        self.ui.plainTextEdit_Page8.appendPlainText("Done")

    def evt_update_plainTextEdit_Page8(self, value):
        self.ui.plainTextEdit_Page8.appendPlainText(value)
    ##########################################################################



    ############################PAGE9-Url-Check###############################
        # self.ui.BtnUrlChecker.clicked.connect(self.SetPageUrlChecker)
        # self.ui.BtnConvert_Page9_UrlCheck.clicked.connect(self.Page9_UrlCheck_CallScript)
    ##########################################################################
    ############################PAGE9-Url-Check###############################
    def SetPageUrlChecker(self):
        self.ui.stackedWidget.setCurrentIndex(9)
        self.ui.label_title_bar_top.setText("URL Checker")
        self.ui.BtnUrlChecker.setStyleSheet(pressed_style)
        self.BtnPressed([1,1,1,1,1,1,1,1,0,1])


    def Page9_UrlCheck_CallScript(self):
        self.ui.plainTextEdit_Page9.clear()
        QApplication.processEvents()

        #Create a QThread object
        self.worker6_urlChecker = Worker6_urlChecker(self.ui.LineEditPath_Page9_Url.text())

        self.worker6_urlChecker.start()

        self.worker6_urlChecker.finished.connect(self.evt_Worker6_urlChecker_thread_finished)
        self.worker6_urlChecker.update_plainTextEdit_Page9.connect(self.evt_update_plainTextEdit_Page9)

    def evt_Worker6_urlChecker_thread_finished(self):
        self.ui.plainTextEdit_Page9.appendPlainText("Done")

    def evt_update_plainTextEdit_Page9(self, value):
        self.ui.plainTextEdit_Page9.appendPlainText(value)

    ##########################################################################



    #########################PAGE10-Email-Domain-Search#######################
        # self.ui.BtnEmailDomainSearch.clicked.connect(self.SetPage10EmailDomainSearch)
        # self.ui.BtnBrows_Page10_EmailDomailSearch.clicked.connect(self.Page10_EmailDomailSearch_BrowsFolders)
        # self.ui.BtnConvert_Page10_EmailDomainSearch.clicked.connect(self.Page10_EmailDomainSearch_CallScript)
    ##########################################################################
    #########################PAGE10-Email-Domain-Search#######################
    def SetPage10EmailDomainSearch(self):
        self.ui.stackedWidget.setCurrentIndex(10)
        self.ui.label_title_bar_top.setText("Email/Domain Search")
        self.ui.BtnEmailDomainSearch.setStyleSheet(pressed_style)
        self.BtnPressed([1,1,1,1,1,1,1,1,1,0])

    def Page10_EmailDomailSearch_BrowsFolders(self):
        self.Page10_EmailDomainSearch_fname = QFileDialog.getExistingDirectory(self, "Chosse folder", current_directory)
        self.ui.LineEditPath_Page10.setText(self.Page10_EmailDomainSearch_fname)

    def Page10_EmailDomainSearch_CallScript(self):
        self.ui.plainTextEdit_Page10.clear()
        QApplication.processEvents()

        #Create a QThread object
        self.worker7_EmailDomainSearch = Worker7_EmailDomainSearch(self.Page10_EmailDomainSearch_fname, self.ui.LineEditPath_Page10_EmailDomain.text())

        self.worker7_EmailDomainSearch.start()

        self.worker7_EmailDomainSearch.finished.connect(self.evt_Worker7_EmailDomainSearch_thread_finished)
        self.worker7_EmailDomainSearch.update_plainTextEdit_Page10.connect(self.evt_update_plainTextEdit_Page10)

    def evt_Worker7_EmailDomainSearch_thread_finished(self):
        self.ui.plainTextEdit_Page10.appendPlainText("Done")

    def evt_update_plainTextEdit_Page10(self, value):
        self.ui.plainTextEdit_Page10.appendPlainText(value)
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