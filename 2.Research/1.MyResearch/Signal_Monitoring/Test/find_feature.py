# -*- coding: UTF-8 -*-
from data_call import data_call

__author__ = 'jeong-yonghan'


class TEST(object):
    def __init__(self, test_data, test_qmf, test_L):
        self.test_data = test_data
        self.test_qmf = test_qmf
        self.test_L = test_L



def main():
    # Call My Data
    from data_call_test import data_call
    mysignal = data_call("ECG_HE", 1, 0) # ECG HE 0 ~ 30


    # DWT
    import Wavelet as wavelet
    from numpy.ma import log2

    ## Candidate for L
    L = [x for x in range(1, int(log2(len(mysignal)) )+1 )]
    ## Candidate for QMF
    qmflist = {
        'haar': [0],
        'db': [4, 6, 8, 10, 12, 14, 16, 18, 20],
        'coif': [1, 2, 3, 4, 5],
        'symmlet': [4, 5, 6, 7, 8, 9, 10]
    }

    ## 실험설계
    import matplotlib.pyplot as plt
    # 0. 특징신호선을 정의
        # 뾰족뾰족이
    # 1. 기존의 Signal 을 Plotting
    # 2. L 을 하나하나 늘려가면서 특징신호선이 어떻게 죽는지 확인한다.
    # 3. haar부터 시작한다.
    # 4. 특징신호선이 살았다 죽었다를 어떻게 메져링하지?

    ### 1. 기존의 신호를 plotting한다.
    plt.figure(0)
    plt.plot(mysignal)
    plt.title('Original Signal')

    ### 2. 각 QMF 에서 뾰족이가 어디서 사라지는지 확인한다.
    #### 2-1. QMF 를 정의한다.
    qmfname = "haar"
    qmfpar = 0
    remove_level = 0
    qmf = wavelet.qmf(qmfname, qmfpar)

    #### 2-2. DWT가 제대로 안 정의되는 param을 잘라버린다.
    if remove_level > 0:
        for idx in range(1,remove_level+1):
            L.remove(idx)
    print L

    # Plot
    it = 0
    for idx in L:
        wc = wavelet.FWT_PO(mysignal,idx,qmf)
        wc_cut = wavelet.cutwavelet(wc,idx)
        ## 2**idx 이후의 coef는 다 잘라버리고 Approximating하겠다는 뜻이다.
        ## 즉, idx가 13까지 정의될 때, idx = 12면 1차 분해
        ## L에서 1이 짤렸으면, 12차 분해는 고려하지 않겠다는 뜻이다.
        recons = wavelet.IWT_PO(wc_cut,idx,qmf)
        decomp_lvl = L[len(L)-1] - idx
        print " L = idx : " ,idx, " decomp: ", decomp_lvl

        # Plotting
        if it % 3 == 0:
            plt.figure()
        plt.subplot(3,1,(it % 3) + 1)
        plt.plot(recons)
        plt.title(str(decomp_lvl) + " th recons")
        it += 1
   # plt.show()




if __name__ == "__main__":
    main()