# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

import csv
import numpy as np

# CSV 파일을 읽어오기
def train_data():
    train = []
    csv_file = open("../Data/train_data.csv","rb")
    reader = csv.reader(csv_file)
    for x in reader:
        train.append(x)
    return np.array(train)

def train_idx():
    trainidx = []
    csv_file = open("../Data/train_idx.csv","rb")
    reader = csv.reader(csv_file)
    for x in reader:
        trainidx.append(x)
    return np.array(trainidx)

def test_data():
    test = []
    csv_file = open("../Data/test_data.csv","rb")
    reader = csv.reader(csv_file)
    for x in reader:
        test.append(x)
    return np.array(test)


def main():
    train = train_data()
    trainidx = train_idx()
    test = test_data()

    print len(train[0]), len(train)
    print len(trainidx)
    print len(test[0]), len(test)

if __name__ == "__main__":
    main()
