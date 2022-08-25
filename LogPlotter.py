#Log Plotter V1.0#
import tkinter as tk
from tkinter import filedialog
from asyncore import read
from time import time
import matplotlib.pyplot as plt
import regex as re
from PyQt6 import QtWidgets, uic
import sys

class LogPlotter:

    def __init__(self) -> None:
        self.diagram_type = "bar"
        self.file_path = ""
        self.log = None
        self.variable_string = ""

    def set_diagram_type_scatter(self):
        self.diagram_type = "scatter"
    
    def set_diagram_type_bar(self):
        self.diagram_type = "bar"

    def read_document(self, path):
        with open(path, "r") as f:
            lines = f.readlines()
        return lines

    def create_touple_list(self, list1, list2):
        if len(list1) != len(list2):
            print("Lists do not have same amount of values")
            return
        touple_list = list()
        counter = 0
        for value in list1:
            touple = (value,list2[counter])
            touple_list.append(touple)
            counter+= 1

        return touple_list

    def read_value_into_list(self, value_string):
        value_list = list()
        timestamp_list = list()
        my_regex = value_string + '";"[0-9]+"'
        for line in self.log:
        
            value = re.findall(my_regex, line)
            if len(value) != 1: #skip lines that do not contain the value string
                continue

            value = str(value).split(";")[1][1:-3]
            value_list.append(int(value))

            timestamp = re.findall('[0-9]{13,14};', line)
            timestamp = str(timestamp)[11:-3]
            print(timestamp)
            timestamp_list.append(int(timestamp))

        tuple_list = self.create_touple_list(timestamp_list,value_list)
        return tuple_list

    def plot_diagram(self, touple_list, value_string):
        fig, ax = plt.subplots()
        y_val = [int(value[1]) for value in touple_list]
        print(y_val)
        x_val = [int(value[0]) for value in touple_list]
        print(x_val)

        if self.diagram_type == "scatter":
            plt.scatter(x_val,y_val)
        if self.diagram_type == "bar":
            plt.bar(x_val, y_val)
        
        plt.xticks(rotation=90)
        ## define diagram arguments
        plt.ylabel(value_string)
        plt.xlabel("timestamp")
        plt.show()

    def search_value(self):
        value_string = self.variable_string

        touple_list = self.read_value_into_list(value_string)
        self.plot_diagram(touple_list, value_string)

    def get_log_file(self):
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename() 
        self.log = self.read_document(self.file_path)
        

    def exit_program(self):
        exit()
    
    def init_plot(self):
        if self.log == None:
            return
        self.search_value()

class Ui(QtWidgets.QMainWindow):
            def __init__(self, logplotter: LogPlotter):
                self.plotter = logplotter
                super(Ui, self).__init__()
                uic.loadUi('LogPlot_UI.ui', self)
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
