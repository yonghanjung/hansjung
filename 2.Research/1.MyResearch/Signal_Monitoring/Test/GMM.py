# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

# Computing Module
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from Module import Wavelet as wavelet

# Operating Module
from Module.data_call import data_call
import csv


# ECG_HE.mat, ECG_MI.mat 파일을 HE.csv, MI.csv 파일로 저장하는 코드
# 한번만 실행하여 데이터를 만들어내고, 이후부터는 실행할 필요 없이 CSV 에서 데이터를 읽어오면 된다.
def Generating_WCs(Decomp, QMF_name, order):
    '''
    Intro
        - 각 신호에 대해서, 미리 정의된 L, QMF 를 바탕으로 Wavelet Coefficients를 뽑아낸다.
        - 이전 실험에서 우리는 모든 WBFs에 대해서 같은 WCs가 특징선을 잡아낸다는 것을 밝혔다.
        - 따라서, 여기서는 'db' '8' 에 대해서 실험을 실행한다.

    INPUT
        - Decomposition Level
        - QMF
        - ORDER

    OUTPUT
        - WCs 들이 적혀있는 CSV 파일
        - No return value
    '''

    qmf = wavelet.qmf(QMF_name, order)
    L = 13 - Decomp

    HE_record = []
    MI_record = []

    # ECG_HE의 각 row 별로 신호를 읽어낸다.
    for idx in range(37):
        mysignal = data_call("ECG_HE", idx, 0)
        wc = wavelet.FWT_PO(mysignal, L, qmf)
        Core_WCs = wc[128:256]
        Core_WCs.insert(0, idx)  # List의 첫번째 elements에 신호의 번호매김
        HE_record.append(Core_WCs)

    # Healthy 신호를 HE.csv 파일로 저장
    HE_csv = open('HE.csv', 'wb')
    wr = csv.writer(HE_csv, quoting=csv.QUOTE_ALL)
    for x in HE_record:
        wr.writerow(x)


    # ECG_HE의 각 row 별로 신호를 읽어낸다.
    for idx in range(208):
        mysignal = data_call("ECG_MI", idx, 0)
        wc = wavelet.FWT_PO(mysignal, L, qmf)
        Core_WCs = wc[128:256]
        Core_WCs.insert(0, idx)  # List의 첫번째 elements에 신호의 번호매김
        HE_record.append(Core_WCs)


    # ECG_MI의 각 row 별로 신호를 읽어낸다.
    for idx in range(208):
        mysignal = data_call("ECG_MI", idx, 0)
        wc = wavelet.FWT_PO(mysignal, L, qmf)
        # 0~127 (1~128) 번째까지는 Scaling coefficients (128개)
        # 128 ~ 255 (129~256) 까지는 Feature
        Core_wc = wc[128:256]
        Core_wc.insert(0, idx)
        MI_record.append(Core_wc)

    # MI 신호를 HE.csv 파일로 저장
    MI_csv = open('MI.csv', 'wb')
    wr = csv.writer(MI_csv, quoting=csv.QUOTE_ALL)
    for x in MI_record:
        wr.writerow(x)


    # CSV 파일을 읽어와서, { Record index : [x1, ..., xN] }의 딕셔너리로 저장한다.
    # Return 값은, 두 file 딕셔너리의 list 1개 (two element)
    # 즉, 각 element들은 dictionary


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


def decompose_train_test(numHEtrain, numMItrain, matrix_result):
    '''
    INPUT
        - Health Condition: 37(records) * 128(wc) 중에 몇 개를 Training 으로 쓸 것인가.
        - MI Condition : 208 (records) * 128(wc) 중에 몇 개를 Test 로 쓸 것인가.

    OUTPUT
        - 1. HE list of list : numHEtrain * 128 (wc)
        - 2. MI list of list : numMItrain * 128 (wc)
        - 3. HE list of list : (37 - numHEtrain) * 128 (wc)
        - 4. MI list of list : (208 - numMItrain) * 128
    '''

    # _, my_HEmat, _, my_MImat = build_matrix()

    A = matrix_result
    my_HEmat = A[1]
    my_MImat = A[3]

    my_HEtraining = my_HEmat[:numHEtrain]
    my_HEtest = my_HEmat[numHEtrain:]

    my_MItraining = my_MImat[:numMItrain]
    my_MItest = my_MImat[numMItrain:]

    return [my_HEtraining, my_MItraining, my_HEtest, my_MItest]


def Linear_PCA(HE_MI_train_test, numdim=2):
    '''
    개요
        - PCA: EIG value 순서대로 Linear Transform을 하여 그 순서대로 sorting

    INPUT
        - numdim : Dimension

    OUTPUT
        - 1. sklearn_HE_train_fit : numdim * numHEtrain
        - 2. sklearn_MI_train_fit : numdim * numMItrain
        - 3. sklearn_HE_test_fit : numdim * numHEtest
        - 4. sklearn_MI_test_fit : numdim * numMItest
    '''

    MyDataSet = HE_MI_train_test
    my_HEtraining = MyDataSet[0]
    my_MItraining = MyDataSet[1]
    my_HEtest = MyDataSet[2]
    my_MItest = MyDataSet[3]

    from sklearn.decomposition import PCA as sklearnPCA

    sklearn_pca = sklearnPCA(n_components=numdim)

    sklearn_HE_train_fit = sklearn_pca.fit_transform(my_HEtraining)
    sklearn_MI_train_fit = sklearn_pca.fit_transform(my_MItraining)
    sklearn_HE_test_fit = sklearn_pca.fit_transform(my_HEtest)
    sklearn_MI_test_fit = sklearn_pca.fit_transform(my_MItest)

    return [sklearn_HE_train_fit, sklearn_MI_train_fit, sklearn_HE_test_fit, sklearn_MI_test_fit]


def Kernel_PCA(HE_MI_train_test, kernel, invTran, degree, numdim=2):
    '''
    개요
        - Kernel PCA 을 적용한다.
    '''

    MyDataSet = HE_MI_train_test
    my_HEtraining = MyDataSet[0]
    my_MItraining = MyDataSet[1]
    my_HEtest = MyDataSet[2]
    my_MItest = MyDataSet[3]

    kpca = KernelPCA(kernel=kernel, fit_inverse_transform=invTran, degree=degree)
    HE_training_kpca = kpca.fit_transform(my_HEtraining)
    MI_training_kpca = kpca.fit_transform(my_MItraining)
    HE_test_kpca = kpca.fit_transform(my_HEtest)
    MI_test_kpca = kpca.fit_transform(my_MItest)

    HE_training_KPCA_2dim = [];
    MI_training_KPCA_2dim = []
    HE_test_KPCA_2dim = [];
    MI_test_KPCA_2dim = []

    for pt in HE_training_kpca:
        HE_training_KPCA_2dim.append((pt[0], pt[1]))
    for pt in MI_training_kpca:
        MI_training_KPCA_2dim.append((pt[0], pt[1]))
    for pt in HE_test_kpca:
        HE_test_KPCA_2dim.append((pt[0], pt[1]))
    for pt in MI_test_kpca:
        MI_test_KPCA_2dim.append((pt[0], pt[1]))

    return [HE_training_KPCA_2dim, MI_training_KPCA_2dim, HE_test_KPCA_2dim, MI_test_KPCA_2dim]


def Train_Test_index(numHEtrain, numMItrain):
    numHE_test = 37 - numHEtrain
    numMI_test = 208 - numMItrain

    Train_idx = [-1] * numHEtrain + [1] * numMItrain
    Test_idx = [-1] * numHE_test + [1] * numMI_test

    return [Train_idx, Test_idx]


def Each_Normalized(KPCA_list):
    A = KPCA_list
    KPCA_HE_train = A[0]
    KPCA_MI_train = A[1]
    KPCA_HE_test = A[2]
    KPCA_MI_test = A[3]

    # Train Data와 Test Data 로 구분한다.
    Train_2dim = np.array(KPCA_HE_train + KPCA_MI_train)
    Test_2dim = np.array(KPCA_HE_test + KPCA_MI_test)


    # 데이터 포인트들 중에서 가장 Maximum Value 를 구한다.
    normal_train_2dim = [];
    normal_test_2dim = []
    x_training_max = np.max(Train_2dim[:, 0])
    y_training_max = np.max(Train_2dim[:, 1])
    x_test_max = np.max(Test_2dim[:, 0])
    y_test_max = np.max(Test_2dim[:, 1])
    norm_max = max(x_training_max, y_training_max, x_test_max, y_test_max)

    # normalized Train Data, normalized Test Data 를 구한다.
    for x, y in Train_2dim:
        norm_x = 100 * (x / norm_max)
        norm_y = 100 * (y / norm_max)
        normal_train_2dim.append([norm_x, norm_y])

    for x, y in Test_2dim:
        norm_x = 100 * (x / norm_max)
        norm_y = 100 * (y / norm_max)
        normal_test_2dim.append([norm_x, norm_y])

    normal_train_2dim = np.array(normal_train_2dim)
    normal_test_2dim = np.array(normal_test_2dim)

    # Normalized HE data, Normalized MI data 를 각기 구한다.
    Normal_KPCA_HE_train = []
    Normal_KPCA_MI_train = []
    Normal_KPCA_HE_test = []
    Normal_KPCA_MI_test = []

    for row in KPCA_HE_train:
        norm_x = (row[0] / norm_max) * 100
        norm_y = (row[1] / norm_max) * 100
        Normal_KPCA_HE_train.append([norm_x, norm_y])

    for row in KPCA_MI_train:
        norm_x = (row[0] / norm_max) * 100
        norm_y = (row[1] / norm_max) * 100
        Normal_KPCA_MI_train.append([norm_x, norm_y])

    for row in KPCA_HE_test:
        norm_x = (row[0] / norm_max) * 100
        norm_y = (row[1] / norm_max) * 100
        Normal_KPCA_HE_test.append([norm_x, norm_y])

    for row in KPCA_MI_test:
        norm_x = (row[0] / norm_max) * 100
        norm_y = (row[1] / norm_max) * 100
        Normal_KPCA_MI_test.append([norm_x, norm_y])

    return [Normal_KPCA_HE_train, Normal_KPCA_MI_train, Normal_KPCA_HE_test, Normal_KPCA_MI_test]


def Test_Train_Normalized(KPCA_list):
    A = KPCA_list
    KPCA_HE_train = A[0]
    KPCA_MI_train = A[1]
    KPCA_HE_test = A[2]
    KPCA_MI_test = A[3]

    # Train Data와 Test Data 로 구분한다.
    Train_2dim = np.array(KPCA_HE_train + KPCA_MI_train)
    Test_2dim = np.array(KPCA_HE_test + KPCA_MI_test)


    # 데이터 포인트들 중에서 가장 Maximum Value 를 구한다.
    normal_train_2dim = [];
    normal_test_2dim = []
    x_training_max = np.max(Train_2dim[:, 0])
    y_training_max = np.max(Train_2dim[:, 1])
    x_test_max = np.max(Test_2dim[:, 0])
    y_test_max = np.max(Test_2dim[:, 1])
    norm_max = max(x_training_max, y_training_max, x_test_max, y_test_max)

    # normalized Train Data, normalized Test Data 를 구한다.
    for x, y in Train_2dim:
        norm_x = 100 * (x / norm_max)
        norm_y = 100 * (y / norm_max)
        normal_train_2dim.append([norm_x, norm_y])

    for x, y in Test_2dim:
        norm_x = 100 * (x / norm_max)
        norm_y = 100 * (y / norm_max)
        normal_test_2dim.append([norm_x, norm_y])

    normal_train_2dim = np.array(normal_train_2dim)
    normal_test_2dim = np.array(normal_test_2dim)

    return [normal_train_2dim, normal_test_2dim]


def check_up(point, xxline, slope, intercept):
    # point = [p,q]

    for idx in range(len(xxline)):
        if xxline[idx] <= point[0]:
            if xxline[idx + 1] >= point[0]:
                prev_x = xxline[idx]
                cur_x = xxline[idx + 1]
                break

    if point[1] >= slope * point[0] + intercept:
        return True
    else:
        return False


def main():
    '''
    0. 기본 세팅. 데이터를 불러들여서, Training / Test로 자른다.
    '''

    # Best WCs가 들어가있는 Wavelet Coefficients를 CSV로 읽어온다.
    ECG_from_csv = read_csv("HE.csv", "MI.csv")

    # HE, MI 별로 읽어온 다음에 list of list 형태로 저장한다. (MATRIX 형태)
    HE_MI_matrix = build_matrix(ECG_from_csv)

    # HE, MI list of list 를 각기 Train, Test set으로 나눈다.
    # HE Train 24 // Test 13
    # MI Train 150 // MI test 58
    HE_MI_train_test = decompose_train_test(24, 150, HE_MI_matrix)

    '''
    1. Linear PCA 결과는 나쁘고 Kernel PCA는 좋다는 것을 보여준다. (눈으로 보기에)
    '''

    # Linear PCA 결과가 나쁘다는 것을 보여준다.
    plt.figure(0)
    plt.title("Linear PCA")
    A = Linear_PCA(HE_MI_train_test)
    PCA_HE_train = A[0]
    PCA_MI_train = A[1]
    for pt in PCA_HE_train:
        plt.plot(pt[0], pt[1], 'bo')
    for pt in PCA_MI_train:
        plt.plot(pt[0], pt[1], 'ro')


    # Kernel PCA 결과가 좋다는 것을 보여준다.
    plt.figure(1)
    plt.title("Kernel PCA")
    A = Kernel_PCA(HE_MI_train_test, 'poly', True, 3)
    KPCA_HE_train = A[0]
    KPCA_MI_train = A[1]
    for row in KPCA_HE_train:
        plt.plot(row[0], row[1], 'bo')
    for row in KPCA_MI_train:
        plt.plot(row[0], row[1], 'ro')
    # plt.show()

    '''
    2. Kernel PCA 에서 나온 숫자들이 너무 크니, 이 숫자들을 normalize한다.
    '''

    KernelPCA_matrix = Kernel_PCA(HE_MI_train_test, 'poly', True, 3)
    Each_normal = Each_Normalized(KernelPCA_matrix)
    Normal_KPCA_HE_train = Each_normal[0]
    Normal_KPCA_MI_train = Each_normal[1]
    Normal_KPCA_HE_test = Each_normal[2]
    Normal_KPCA_MI_test = Each_normal[3]

    Test_Train_Normal = Test_Train_Normalized(KernelPCA_matrix)
    Normal_Train_2dim = Test_Train_Normal[0]
    Normal_Test_2dim = Test_Train_Normal[1]


    '''
    3. SVM Training
    '''

    # TEST, Train Class 를 부른다.
    Training_class = [1] * 24 + [-1] * 150
    Test_class = [1] * 13 + [-1] * 58

    # SVM 함수를 정의하고 Training
    #clf = svm.SVC(kernel="sigmoid")
    clf = svm.SVC(kernel = "linear")
    clf.fit(Normal_Train_2dim, Training_class)


    ''' Linear SVM
    '''
    # SVM 함수의 기울기를 구한다.
    w = clf.coef_[0]
    #a = w[0] / w[1]
    a = - w[0] / w[1]
    xx = np.linspace(-100, 100)

    # SVM 함수로 Line을 그려낸다.
    yy = a * xx - (clf.intercept_[0])

    plt.figure(2)
    plt.title("SVM Training Result")

    for row in Normal_KPCA_HE_train:
        plt.plot(row[0], row[1], 'bo')
    for row in Normal_KPCA_MI_train:
        plt.plot(row[0], row[1], 'ro')

    plt.plot(xx, yy, 'r-')

    '''
    5. Performance 계산하기
    '''
    plt.figure(3)
    plt.title("SVM TEST RESULT")
    plt.plot(xx, yy, 'r--')

    for test_point in Normal_KPCA_HE_test:
        plt.plot(test_point[0], test_point[1], 'bo')
    for test_point in Normal_KPCA_MI_test:
        plt.plot(test_point[0], test_point[1], 'ro')

    for test_point in Normal_KPCA_HE_train:
        plt.plot(test_point[0], test_point[1], 'go')
        #print test_point[0], test_point[1]
    for test_point in Normal_KPCA_MI_train:
        plt.plot(test_point[0], test_point[1], 'yo')
        #print test_point[0], test_point[1]


    MyGuess = []
    for test_point in Normal_Test_2dim:
        A =  clf.predict(test_point)
        MyGuess.append(A[0])

    #print MyGuess
    #print Test_class
    #print sum(x == y for x, y in zip(MyGuess, Test_class))




    '''
    for test_point in Normal_Test_2dim:
        if check_up(test_point, xx, a, - (clf.intercept_[0])) == True:
            ## test_point = MI
            MyGuess.append(-1)
        else:
            MyGuess.append(1)




    print len(Normal_KPCA_HE_test)
    print MyGuess
    print Test_class
    print sum(x == y for x, y in zip(MyGuess, Test_class))
    '''

    plt.show()



if __name__ == "__main__":
    main()