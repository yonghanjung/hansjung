# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

import csv
from sklearn.decomposition import KernelPCA

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

def build_matrix(read_csv_dict_list):
    myHE = read_csv_dict_list[0]
    myMI = read_csv_dict_list[1]
    my_HEmat = [];
    my_HEkey = []
    my_MImat = [];
    my_MIkey = []
    for idx, key in enumerate(myHE):
        test = myHE[key]
        test = [float(x) for x in test]
        my_HEmat.append(test)
        my_HEkey.append(int(key))

    for idx, key in enumerate(myMI):
        test = myMI[key]
        test = [float(x) for x in test]
        my_MImat.append(test)
        my_MIkey.append(int(key))

    return [my_HEkey, my_HEmat, my_MIkey, my_MImat]




def main():
    filename1 = "HE.csv"
    filename2 = "MI.csv"

    Readed_CSV = read_csv(filename1, filename2)
    HE_MI_matrix = build_matrix(Readed_CSV)

    HE_mat = HE_MI_matrix[1]
    MI_mat = HE_MI_matrix[3]

    # 37 : HE + 208 : MI // dim : 128
    TOTAL_MAT = HE_mat + MI_mat

    kpca = KernelPCA(kernel="poly", fit_inverse_transform=True, degree=3)
    DUZI = kpca.fit(TOTAL_MAT)
    print DUZI.lambdas_
    print len(DUZI.lambdas_)








if __name__ == "__main__":
    main()
