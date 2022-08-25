import matplotlib.pyplot as plt
import regex as re
import tkinter as tk
from tkinter import filedialog

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
