#Log Plotter V1.0#
import tkinter as tk
from tkinter import filedialog
from asyncore import read
from time import time
import matplotlib.pyplot as plt
import regex as re
import numpy as np


def read_document(path):
    with open(path, "r") as f:
        lines = f.readlines()
    return lines

def create_touple_list(list1, list2):
    if len(list1) != len(list2):
        print("Lists don not have same amount of values")
        return
    touple_list = list()
    counter = 0
    for value in list1:
        touple = (value,list2[counter])
        touple_list.append(touple)
        counter+= 1

    return touple_list

def read_value_into_list(value_string, log):
    value_list = list()
    timestamp_list = list()
    my_regex = value_string + '";"[0-9]+"'
    for line in log:
        
        value = re.findall(my_regex, line)
        if len(value) != 1: #skip lines that do not contain the value string
            continue

        value = str(value).split(";")[1][1:-3]
        value_list.append(value)

        timestamp = re.findall('[0-9]{13,14};', line)
        timestamp = str(timestamp)[2:-3]
        print(timestamp)
        timestamp_list.append(timestamp)
    
    return create_touple_list(timestamp_list, value_list)

def plot_diagram(touple_list):
    fig, ax = plt.subplots()
    plt.scatter(*zip(*touple_list))
    plt.xticks(rotation=90)
    ax.invert_xaxis()
    plt.show()

def search_value(log):
    value_string = input("Enter value name to plot: ")

    touple_list = read_value_into_list(value_string, log)
    plot_diagram(touple_list)



    
def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()    
    log = read_document(file_path)
    search_value(log)

if __name__ == "__main__":
    main()
