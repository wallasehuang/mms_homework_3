
from PIL import Image
from numpy import array
import sift
from pylab import *
import os
import csv
from sklearn.cluster import KMeans
import image_retrieval_q3 as q3

def create_stop_word_list():
    kmeans = q3.kCenter_to_kmeans()

    stop_val = [0]*128
    for val in kmeans.labels_:
        stop_val[val] += 1

    index = 0
    stop_list =list()
    for val in stop_val:
        row_data =(index,val)
        stop_list.append(row_data)
        index += 1

    stop_list = sorted(stop_list,key=lambda stop_list:stop_list[1])
    stop_list = stop_list[::-1]
    print stop_list[:10]

    f=open("stop_word_list.csv","w")
    w=csv.writer(f)

    for row in stop_list[:10]:
        w.writerows([[row[0]]])
    f.close()

    print 'finish stop word list csv'

def get_stop_word_list():
    stop_word_list = list()
    f = open("stop_word_list.csv",'r')
    for index in csv.reader(f):
        stop_word_list.append(int(index[0]))
    f.close
    return stop_word_list

def create_vector_stop_word_list(DATASET_SIFT):
    kmeans = q3.kCenter_to_kmeans()
    sift_data = list()

    stop_word_list = get_stop_word_list()

    for filename in os.listdir(DATASET_SIFT):

        f = loadtxt(DATASET_SIFT+'/'+filename)

        if len(f.shape) <= 1:
            continue

        l1,d1 = sift.read_features_from_file(DATASET_SIFT+'/'+filename)

        img_vector = kmeans.predict(d1)
        x = [0]*128
        for num in img_vector:
            if not(num in stop_word_list):
                x[num] = x[num]+1
        img_row = [os.path.splitext(filename)[0]+'.jpg',','.join(str(i) for i in x)]
        sift_data.append(img_row)
        f = open("sift_with_stop_word.csv","w")
        w = csv.writer(f)
        w.writerows(sift_data)
        f.close()
    print 'finish create vector stop word list csv'

def vector_distance(arr1,arr2):
    if len(arr1) != len(arr2):
        return None
    sum,sum_arr1,sum_arr2 = 0,0,0

    for i in xrange(len(arr1)):
        sum += arr1[i]*arr2[i]
        sum_arr1 += arr1[i]**2
        sum_arr2 += arr2[i]**2

    sum_arr1 = sum_arr1**0.5
    sum_arr2 = sum_arr2**0.5

    return sum/(sum_arr1*sum_arr2)

def Q4_Visual_Words_using_stop_words(filename):
    kmeans = q3.kCenter_to_kmeans()
    stop_word_list = get_stop_word_list()
    q_img = filename
    sift.process_image(q_img,'q_img.sift')

    l1,d1 = sift.read_features_from_file('q_img.sift')
    q_img_vector = kmeans.predict(d1)

    q_vector = [0]*128
    for num in q_img_vector:
        if not(num in stop_word_list):
            q_vector[num] = q_vector[num]+1

    f = open('sift_with_stop_word.csv','r')
    rank = list()
    for row in csv.reader(f):
        distance = vector_distance(q_vector,[int(i) for i in row[1].split(',')])

        if distance == None:
            continue

        rank_data = (row[0],distance)
        rank.append(rank_data)
    f.close()

    rank = sorted(rank,key=lambda rank:rank[1])
    rank = rank[::-1]
    return rank[:10]
