from PIL import Image
from matplotlib.pyplot import imshow
import numpy as np
import os
import csv

def color_histogram(DATASET):

    file_data = []
    color_histogram_data = list()

    for filename in os.listdir(DATASET):
        img = Image.open(DATASET+'/'+filename)
        img_row = [filename,','.join(str(i) for i in img.histogram())]
        color_histogram_data.append(img_row)

    f = open("color_histogram.csv","w")
    w = csv.writer(f)
    w.writerows(color_histogram_data)
    f.close()
    print 'finish color histogram csv'

def euclidean(arr1,arr2):
    if len(arr1) != len(arr2):
        return None
    sum = 0
    for i in xrange(len(arr1)):
        sum += (arr1[i]-arr2[i])**2
    return sum**0.5

def Q1_ColorHistogram(filename):

    q_img = Image.open(filename)
    q_histogram = q_img.histogram()

    f = open('color_histogram.csv','r')

    rank = list()
    for row in csv.reader(f):
        distance = euclidean(q_histogram,[int(i) for i in row[1].split(',')])
        if distance == None:
            continue
        rank_row = (row[0],distance)
        rank.append(rank_row)
    f.close()

    # return rank
    rank = sorted(rank,key=lambda rank:rank[1])
    return rank[0:10]




