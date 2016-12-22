#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pylab import *

import pickle

from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog
from ttk import Frame, Button, Label, Style
import image_retrieval_q1 as q1
import image_retrieval_q2 as q2
import image_retrieval_q3 as q3
import image_retrieval_q4 as q4

from random import randint


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()


    def initUI(self):

        self.parent.title("HW3")

        self.pack(fill=BOTH, expand=1)

        Button(self, text = "Select File", command = openFile).grid(row=0, column=0, pady=5)
        self.fileName = StringVar()
        Label(self, textvariable=self.fileName).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

        Label(self, text = "Select Mode: ").grid(row=1, column=0, pady=5)
        mode = StringVar(self)
        mode.set("Q1-ColorHistogram")
        om = OptionMenu(self, mode, "Q1-ColorHistogram", "Q2-ColorLayout", "Q3-SIFT Visual Words", "Q4-Visual Words using stop words")
        om.grid(row=1, column=1, pady=5, sticky=W)

        Button(self, text = "SEARCH", command = lambda: startSearching(self.fileName.get(),mode.get())).grid(row=3, column=0, pady=5)

        # self.images = []
        # for i in range(10):
        #     self.images.append(Label(self))
        #     self.images[i].grid(row=i/5+4, column=i%5, pady=50)

def result (rank,filename):
    size = 128,128
    img = Image.open(filename)
    img.thumbnail(size,Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    search_img = Label(app,image = img)
    search_img.image = img
    search_img.pack()
    search_img.place(x=440,y=20)


    for i in range(10):
        img = Image.open('./dataset/'+rank[i][0])
        img.thumbnail(size,Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        result_img = Label(app,image = img)
        result_img.image = img
        result_img.pack()
        if(i<=4):
            result_img.place(x =10+(i*120),y=160)
        else:
            result_img.place(x =10+((i-5)*120),y=310)

        # result_img.grid(row=i/5+4, column=i%5,pady =5,padx = 5)

def openFile ():
    fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
    app.fileName.set(fileName)

def startSearching (fileName, mode):
    rank = list()
    if(mode =='Q1-ColorHistogram'):
        rank = q1.Q1_ColorHistogram(fileName)
        result(rank,fileName)


    if(mode =='Q2-ColorLayout'):
        rank = q2.Q2_ColorLayout(fileName)
        result(rank,fileName)

    if(mode =='Q3-SIFT Visual Words'):
        rank = q3.Q3_SIFT_Visual_Words(fileName)
        result(rank,fileNmae)

    if(mode =='Q4-Visual Words using stop words'):
        rank = q4.Q4_Visual_Words_using_stop_words(fileName)
        result(rank,fileName)

    print mode

if __name__ == '__main__':
    root = Tk()
    size = 220, 220

    app = Example(root)
    root.geometry("620x450")
    root.mainloop()


