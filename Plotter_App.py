#Log Plotter V1.0#
import tkinter as tk
from tkinter import filedialog
from asyncore import read
from time import time
import matplotlib.pyplot as plt
import regex as re
from PyQt6 import QtWidgets, uic
import sys
import os
from Plotter import LogPlotter

class Ui(QtWidgets.QMainWindow):
            def __init__(self, logplotter: LogPlotter):
                self.plotter = logplotter
                super(Ui, self).__init__()
                path_to_ui = os.path.join('V:\ENT-PRJ\SOFTWARE\Python\LogPlot\LogPlot.ui')
                uic.loadUi(path_to_ui, self)
                #init buttons for python
                self.scatter_button = self.findChild(QtWidgets.QPushButton, "ScatterButton")
                self.bar_button = self.findChild(QtWidgets.QPushButton, "pushButton_4")
                self.exit_button = self.findChild(QtWidgets.QPushButton, "pushButton")
                self.plot_button = self.findChild(QtWidgets.QPushButton, "pushButton_2")
                self.data_file_button = self.findChild(QtWidgets.QPushButton, "pushButton_5")
                self.path_edit = self.findChild(QtWidgets.QLineEdit, "lineEdit")
                self.variable_edit = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")
                self.button_group = QtWidgets.QButtonGroup()
                self.button_group.addButton(self.bar_button)
                self.button_group.addButton(self.scatter_button)
                
                #define functions
                self.scatter_button.clicked.connect(self.plotter.set_diagram_type_scatter)
                self.bar_button.clicked.connect(self.plotter.set_diagram_type_bar)
                self.exit_button.clicked.connect(self.plotter.exit_program)
                self.plot_button.clicked.connect(self.plotter.init_plot)
                self.plot_button.clicked.connect(self.set_variable_string)
                self.data_file_button.clicked.connect(self.plotter.get_log_file)
                self.data_file_button.clicked.connect(self.show_file_path)
                
                self.show()

            def show_file_path(self):
                path = self.plotter.file_path
                self.path_edit.setText(path)
            
            def set_variable_string(self):
                self.plotter.variable_string = self.variable_edit.text()
            
            


def main():
    app = QtWidgets.QApplication(sys.argv)
    
    application = LogPlotter()
    window = Ui(application)
    app.exec()
    


if __name__ == "__main__":
    main()
