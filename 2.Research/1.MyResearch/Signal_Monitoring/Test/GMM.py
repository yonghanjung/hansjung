# -*- coding: utf-8 -*-

__author__ = 'jeong-yonghan'


def main():
    import numpy as np
    import matplotlib.pyplot as plt
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

        myHE = {}; myMI = {}
        with open('HE.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                first = row[0]
                row.pop(0)
                myHE.update({first: row})

        with open('MI.csv','rb') as f:
            reader = csv.reader(f)
            for row in reader:
                first = row[0]
                row.pop(0)
                myMI.update({first: row})
        return myHE, myMI

    def build_matrix():
        myHE, myMI = read_csv()
        my_HEmat = []; my_HEkey = []
        my_MImat = []; my_MIkey = []
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

    def training_test():
        _, my_HEmat, _, my_MImat = build_matrix()
        my_HEtraining = my_HEmat[:24]
        my_HEtest = my_HEmat[25:]

        my_MItraining = my_MImat[:69]
        my_MItest = my_MImat[70:]

        return my_HEtraining, my_HEtest, my_MItraining, my_MItest

    # Linear PCA
    def reducing_dim():
        my_HEtraining, my_HEtest, my_MItraining, my_MItest = training_test()
        from sklearn.decomposition import PCA as sklearnPCA
        sklearn_pca = sklearnPCA(n_components=2)

        sklearn_HE_fit = sklearn_pca.fit_transform(my_HEtraining)
        sklearn_MI_fit = sklearn_pca.fit_transform(my_MItraining)

        return sklearn_HE_fit, sklearn_MI_fit

    def try_kpca():
        my_HEtraining, my_HEtest, my_MItraining, my_MItest = training_test()
        from sklearn.decomposition import PCA, KernelPCA
        kpca = KernelPCA(kernel= 'poly', fit_inverse_transform= True, degree=2)
        HE_kpca = kpca.fit_transform(my_HEtraining)
        MI_kpca = kpca.fit_transform(my_MItraining)

        return HE_kpca, MI_kpca


    A,B = try_kpca()
    #A,B = reducing_dim()

    for idx in range(len(A)):
        plt.plot(A[idx][0], A[idx][1],'ro')
    for idx in range(len(B)):
        plt.plot(B[idx][0], B[idx][1],'bo')
    plt.show()

if __name__ == "__main__":
    main()