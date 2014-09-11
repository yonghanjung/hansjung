# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.mixture import GMM
from sklearn.decomposition import FastICA
from sklearn.svm import LinearSVC
from sklearn.ensemble import ExtraTreesClassifier

import csv

def read_csv(filename1, filename2):
    '''
    Intro
        - CSV 파일을 읽어와서, { Record index : [x1, ..., xN] }의 딕셔너리로 저장한다.

    Input
        - filename1 : 'HE.csv'
        - filename2 : 'MI.csv'

    Output
        - List 1개
            - 0 : filename1 dictionary
            - 1 : filename2 dictionary
    '''

    HE_read = {}
    MI_read = {}

    # HE.csv를 읽어와서, { Record 번호 : [x1, x2, ... ] } 의 Dictionary 형태로 저장한다.
    with open(filename1, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            first = row[0]
            row.pop(0)
            row = [float(x) for x in row]
            HE_read.update({int(first): row})

    with open(filename2, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            first = row[0]
            row.pop(0)
            row = [float(x) for x in row]
            MI_read.update({int(first): row})
    return [HE_read, MI_read]


def main():
    filename1 = "HE.csv"
    filename2 = "MI.csv"

    csv_data = read_csv(filename1=filename1, filename2=filename2)
    csv_data = np.array(csv_data)
    total_matrix = []
    matrix_key = []

    train_mat = []
    test_mat = []


    for x in csv_data:
        for idx in x:
            matrix_key.append(idx)
            total_matrix.append(x[idx])

    total_matrix = np.array(total_matrix)
    print total_matrix.shape
    y = [1] * 37 + [-1] * 208

    print total_matrix[0]


    kpca = KernelPCA(n_components=2, kernel='rbf')
    A = kpca.fit_transform(total_matrix)

    '''
    for x in total_matrix[:37]:
        plt.plot(x,'b')
    for x in total_matrix[37:]:
        plt.plot(x,'r')
    '''

    for idx in A[:37]:
        plt.plot(idx[0], idx[1], 'bo')
    for idx in A[37:]:
        plt.plot(idx[0], idx[1], 'ro')


    plt.show()


    # 나이브 베이지안
    # 128 --> 2 ?
    # GMM X

    # DIM Reduction

    # Classifier?

    # Kernel 을 실제로 만들어서 해야 하나?
    #



if __name__ == "__main__":
    main()
