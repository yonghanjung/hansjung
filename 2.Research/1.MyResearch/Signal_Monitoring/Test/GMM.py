# -*- coding: utf-8 -*-


__author__ = 'jeong-yonghan'
from sklearn import svm

def main():
    '''
    알고리즘
        # 레벨0 : 8192 = 2^13
        # 레벨1 : 4192 = 2^12 / 4192
        # 레벨2 : 2048 = 2^11 / 4192 + 2048
        # 레벨3 : 1024 = 2^10/ 4192 + 2048 + 1024
        # 레벨4 : 512  = 2^9 / 4192 + 2048 + 1024 + 512
        # 레벨5 : 256 = 2^8 / 4192 + 2048 + 1024 + 256
        # 레벨6 : 128 = 2^7 / 4192 + 2048 + 1024 + 256 + 128

        idx = L = 7일 때 (DEC 6) , 이걸로 자르면, 즉, 2^7 = 128개로는 표현이 안돼
        idx = L = 8일 때 (DEC 5) , 이걸로 자르면, 즉 2^8= 256개로는 표현이 돼
        L = 8 --> 7 (DEC 5-->6) 은 256개의 scailing coefficients에 대해서 DWT를 하는 것.

    결론
        L = 7 (Decomposition Level 6) 일 때, 128 ~ 256번째 포인트들이 핵심 Feature
    '''

    import numpy as np
    import matplotlib.pyplot as plt
    from compiler.ast import flatten


    # # GENERATE FEATURES
    # Extract the best WC
    def gen_feature():
        import Wavelet as wavelet

        qmf = wavelet.qmf('db', 8)
        L = 7

        from data_call_test import data_call
        import csv

        HE_format = []
        MI_format = []
        HE_Feature = {}
        MI_Feature = {}

        for idx in range(37):
            mysignal = data_call("ECG_HE", idx, 0)
            wc = wavelet.FWT_PO(mysignal, L, qmf)
            # 0~127 (1~128) 번째까지는 Scaling coefficients (128개)
            # 128 ~ 255 (129~256) 까지는 Feature
            core_wc = wc[128:256]
            core_wc.insert(0, idx)
            HE_format.append(core_wc)

        HEcsv = open('HE.csv', 'wb')
        wr = csv.writer(HEcsv, quoting=csv.QUOTE_ALL)
        for x in HE_format:
            wr.writerow(x)

        for idx in range(208):
            mysignal = data_call("ECG_MI", idx, 0)
            wc = wavelet.FWT_PO(mysignal, L, qmf)
            # 0~127 (1~128) 번째까지는 Scaling coefficients (128개)
            # 128 ~ 255 (129~256) 까지는 Feature
            core_wc = wc[128:256]
            core_wc.insert(0, idx)
            MI_format.append(core_wc)

        MIcsv = open('MI.csv', 'wb')
        wr = csv.writer(MIcsv, quoting=csv.QUOTE_ALL)
        for x in MI_format:
            wr.writerow(x)

    def read_csv():
        import csv

        myHE = {};
        myMI = {}
        with open('HE.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                first = row[0]
                row.pop(0)
                myHE.update({first: row})

        with open('MI.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                first = row[0]
                row.pop(0)
                myMI.update({first: row})
        return myHE, myMI

    def build_matrix():
        myHE, myMI = read_csv()
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

        return my_HEkey, my_HEmat, my_MIkey, my_MImat

    # --------------------------------------------------------------------------------------------------#
    # 여기까지는 그냥 데이터 읽어오는 거라서 NEVER Touch #

    def training_test(numHEtrain, numMItrain):
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

        _, my_HEmat, _, my_MImat = build_matrix()
        my_HEtraining = my_HEmat[:numHEtrain]
        my_HEtest = my_HEmat[numHEtrain:]

        my_MItraining = my_MImat[:numMItrain]
        my_MItest = my_MImat[numMItrain:]

        return [my_HEtraining, my_MItraining, my_HEtest, my_MItest]


    # Linear PCA
    def reducing_dim(numdim):
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

        MyDataSet = training_test(25, 150)
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

    def try_kpca(kernel, invTran, degree):
        '''
        개요
            - Kernel PCA 을 적용한다.
        '''

        MyDataSet = training_test(24, 150)
        my_HEtraining = MyDataSet[0]
        my_MItraining = MyDataSet[1]
        my_HEtest = MyDataSet[2]
        my_MItest = MyDataSet[3]

        from sklearn.decomposition import PCA, KernelPCA

        kpca = KernelPCA(kernel=kernel, fit_inverse_transform=invTran, degree=degree)
        HE_training_kpca = kpca.fit_transform(my_HEtraining)
        MI_training_kpca = kpca.fit_transform(my_MItraining)
        HE_test_kpca = kpca.fit_transform(my_HEtest)
        MI_test_kpca = kpca.fit_transform(my_MItest)

        return [HE_training_kpca, MI_training_kpca, HE_test_kpca, MI_test_kpca]

    A = try_kpca('poly', True, 3)
    HE_train_kpca = A[0]
    MI_train_kpca = A[1]
    HE_test_kpca = A[2]
    MI_test_kpca = A[3]

    HE_train_2dim = []
    for HE_train in HE_train_kpca:
        HE_train_2dim.append([HE_train[0], HE_train[1]])

    MI_train_2dim = []
    for MI_train in MI_train_kpca:
        MI_train_2dim.append([MI_train[0], MI_train[1]])

    HE_test_2dim = []
    for HE_test in HE_test_kpca:
        HE_test_2dim.append([HE_test[0], HE_test[1]])

    MI_test_2dim = []
    for MI_test in MI_test_kpca:
        MI_test_2dim.append([MI_test[0], MI_test[1]])

    Test_2dim = np.array(HE_test_2dim + MI_test_2dim)

    Train_2dim = np.array(HE_train_2dim + MI_train_2dim)

    Training_class = [-1] * 24 + [1] * 150
    Test_class = [-1] * 13 + [1] * 58


    # clf = svm.SVC(kernel = "linear")
    normal_train_2dim = []; normal_test_2dim = []
    x_training_max = np.max(Train_2dim[:,0])
    y_training_max = np.max(Train_2dim[:,1])

    x_test_max = np.max(Test_2dim[:,0])
    y_test_max = np.max(Test_2dim[:,1])

    norm_max = max(x_training_max,y_training_max, x_test_max, y_test_max)

    for x,y in Train_2dim:
        norm_x = 100* (x / norm_max)
        norm_y = 100* (y / norm_max)
        normal_train_2dim.append([norm_x, norm_y])

    for x,y in Test_2dim:
        norm_x = 100 * (x / norm_max)
        norm_y = 100 * (y / norm_max)
        normal_test_2dim.append([norm_x, norm_y])

    normal_train_2dim = np.array(normal_train_2dim)
    normal_test_2dim = np.array(normal_test_2dim)

    '''
    for point in normal_train_2dim:
        plt.plot(point[0], point[1],'bo')
    plt.show()
    '''

    '''
    0826 - 여기까지 normalizing이 완료되었다.
    '''

    clf = svm.SVC(kernel = "linear")
    clf.fit(normal_train_2dim, Training_class)
    w = clf.coef_[0]

    a = -w[0] / w[1]
    #print a
    xx = np.linspace(-100,100)
    #print xx
    yy = a * xx - (clf.intercept_[0])
    #print w[1]


    b = clf.support_vectors_[0]
    yy_down = a * xx + (b[1] - a * b[0])
    b = clf.support_vectors_[-1]
    yy_up = a * xx + (b[1] - a * b[0])

    yy = [(x+y)/2 for x,y in zip(yy_down, yy_up)]


    plt.plot(xx, yy, 'r-')
    plt.plot(xx, yy_down, 'b--')
    plt.plot(xx, yy_up, 'g--')
    plt.plot(b,'ro')

    plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],s=80, facecolors='none')
    plt.scatter(normal_train_2dim[:, 0], normal_train_2dim[:, 1], c=Training_class, cmap=plt.cm.Paired)

    #plt.scatter(normal_test_2dim[:,0], normal_test_2dim[:,1], c=Test_class, cmap = plt.cm.Paired)
    for idx in range(13):
        plt.plot(normal_test_2dim[idx][0], normal_test_2dim[idx][1],'yo')

    for idx in range(13,71):
        plt.plot(normal_test_2dim[idx][0], normal_test_2dim[idx][1],'go')


    plt.axis('tight')
    plt.show()


    print yy






if __name__ == "__main__":
    main()