from math import *
import time
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import font as tkFont

def transform_array(array):
    res = []
    size = floor(sqrt(len(array)))
    for i in range(size):
        res.append([])
        for j in range(size):
            res[i].append(array[j + size * i])
    return np.array(res)
            

def visualizer(path):
    fen = Tk()
    
    global i
    i = 0
    labels = []
    def burst_mode(j):
        while (j < len(path)):
            for label in labels:
                label.destroy()
            labels.clear()
            test = transform_array(path[j]).tolist()
            for index, row in enumerate(test):
                for index1, colum in enumerate(row):
                    e = Label(fen, text=colum, font=helv80, borderwidth=2, relief="ridge", width=(10//len(row)))
                    e.grid(row=index, column=index1)
                    labels.append(e)
            j += 1
            global i
            i += 1
            fen.update()
    
    def change_i(value):
        if value == 0:
            burst_mode(0)
        else:
            global i
            i += value
            if i < 0:
                i = 0
            elif i >= len(path):
                i = len(path) - 1
            for label in labels:
                label.destroy()
            labels.clear()
            if i != len(path):
                test = transform_array(path[i]).tolist()
                for index, row in enumerate(test):
                    for index1, colum in enumerate(row):
                        e = Label(fen, text=colum, font=helv80, borderwidth=2, relief="ridge", width=(10//len(row)))
                        e.grid(row=index, column=index1)
                        labels.append(e)
                fen.update()

    test = transform_array(path[i]).tolist()


    #canvas = tk.Canvas(fen,width=1000,height=1000)

    helv80 = tkFont.Font(family='Helvetica', size=80)

    fen.rowconfigure((0, 0), weight=0)
    fen.columnconfigure((0, 0), weight=0)

    for index, row in enumerate(test):
        for index1, colum in enumerate(row):
            e = Label(fen, text=colum, font=helv80, borderwidth=2, relief="ridge", width=(10//len(row)))
            e.grid(row=index, column=index1)

    next_button = Button(fen, text="next >", command=lambda *args: change_i(1))
    burst_button = Button(fen, text="Burst", command=lambda *args: change_i(0))
    prev_button = Button(fen, text="< prev", command=lambda *args: change_i(-1))
    next_button.grid(row=len(test) + 1, column=ceil(len(test) / 2), columnspan=len(test) // 2)
    burst_button.grid(row=len(test) + 1, column=ceil(len(test) / 2) - 1, columnspan=len(test) // 2)
    prev_button.grid(row=len(test) + 1, column=0, columnspan=len(test) // 2)
    
    
    fen.mainloop()