
from PIL import Image
from numpy import array
import sift
from pylab import *
import os
import csv
from sklearn.cluster import KMeans


def img_to_sift(DATASET,DATASET_SIFT):
    for filename in os.listdir(DATASET):
        sift.process_image(DATASET +'/'+ filename,DATASET_SIFT+'/'+os.path.splitext(filename)[0]+'.sift')
    print 'finish img to sift'

def sift_to_arr(DATASET_SIFT):
    arr = list()
    for filename in os.listdir(DATASET_SIFT):
        #print filename

        f = loadtxt(DATASET_SIFT+'/'+filename)

        if len(f.shape) <= 1:
            continue

        l1,d1 = sift.read_features_from_file(DATASET_SIFT+'/'+filename)
        for row in d1:
            arr.append(row)

    print 'finish sift to arr'
    return arr

def arr_to_kmeans():
    arr = sift_to_arr('dataset_sift')
    kmeans = KMeans(n_clusters=128, random_state=0).fit(arr)
    print 'finish kmeans'

    k_center =  kmeans.cluster_centers_
    f=open("kmean_center.csv","w")
    w =csv.writer(f)

    for center in k_center:
        w.writerows([center])

    f.close()
    print 'finish kmeans cluster center csv'

def kCenter_to_kmeans():
    f = open('kmean_center.csv','r')
    k_center = list()
    for row in csv.reader(f):
        data_arr = [float(i) for i in row]
        k_center.append(data_arr)
    f.close()
    k_center = np.array(k_center)

    kmeans = KMeans(n_clusters=128, random_state=0,init=k_center,n_init=1).fit(k_center)

    return kmeans

def img_to_vector(DATASET_SIFT):
    kmeans = kCenter_to_kmeans()
    sift_data = list()

    for filename in os.listdir(DATASET_SIFT):

        f = loadtxt(DATASET_SIFT+'/'+filename)

        if len(f.shape) <= 1:
            continue

        l1,d1 = sift.read_features_from_file(DATASET_SIFT+'/'+filename)

        img_vector = kmeans.predict(d1)
        x = [0]*128
        for num in img_vector:
            x[num] = x[num]+1
        img_row = [os.path.splitext(filename)[0]+'.jpg',','.join(str(i) for i in x)]
        sift_data.append(img_row)
        f = open("sift.csv","w")
        w = csv.writer(f)
        w.writerows(sift_data)
        f.close()
    print 'finish img to vector'

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

def Q3_SIFT_Visual_Words(filename):
    kmeans = kCenter_to_kmeans()

    q_img =filename
    sift.process_image(q_img,'q_img.sift')

    l1,d1 = sift.read_features_from_file('q_img.sift')
    q_img_kmeans = kmeans.predict(d1)

    q_img_vector = [0]*128
    for num in q_img_kmeans:
        q_img_vector[num] = q_img_vector[num]+1

    f = open('sift.csv','r')
    rank = list()
    for row in csv.reader(f):
        distance = vector_distance(q_img_vector,[int(i) for i in row[1].split(',')])

        if distance == None:
            continue

        rank_data = (row[0],distance)
        rank.append(rank_data)
    f.close()

    rank = sorted(rank,key=lambda rank:rank[1])
    rank = rank[::-1]
    return rank[:10]
