__author__ = 'jeong-yonghan'
from compiler.ast import flatten
import Wavelet as wavelet
import Data as data
import matplotlib.pyplot as plt
import General
import scipy.io
import bandpass as bp

__author__ = 'jeong-yonghan'


def main():
    '''
    #For the case of PPG
    mysignal = scipy.io.loadmat("Data/mynewdata2")
    mysignal = mysignal['mysignal2']
    #mysignal = mysignal[:8192]
    '''

    '''
    # For the case of ECG_HE #
    mysignal = scipy.io.loadmat("Data/ECG_HE.mat")
    mysignal = mysignal['ECG_HE']
    mysignal = mysignal[15]
    mysignal = data.array_to_list(mysignal)
    '''

    #"""
    # For the case of ECG_MI #
    mysignal = scipy.io.loadmat("Data/ECG_MI.mat")
    mysignal = mysignal['ECG_MI']
    mysignal = mysignal[3]
    mysignal = data.array_to_list(mysignal)
    #"""

    '''
    #For the case of PPG KIWOOK
    mysignal = scipy.io.loadmat("Data/mytest.mat")
    mysignal = mysignal['var']
    mysignal = mysignal[0]
    mysignal = data.array_to_list(mysignal)
    mysignal = mysignal[:2**8]
    mysignal = flatten(mysignal)
    '''

    print len(mysignal)
    qmf = wavelet.qmf('db',2)

    L = 4

    #'''
    # Wavelet Decomposition
    wc = wavelet.FWT_PO(mysignal,L,qmf)
    wc1 = wc
    wc2 = wc


    # Trend
    wc_trend = wavelet.cutwavelet(wc1,L)
    trend = wavelet.IWT_PO(wc_trend,L,qmf)

    # Noise
    wc_noise = wavelet.cutscale(wc2,L)
    noise = wavelet.IWT_PO(wc_noise,L,qmf)

    # More modificaiton
    noise_abs = [abs(it) for it in noise]
    noise_sq = [it ** 2 for it in noise]


    # Plotting
    plt.figure(0)
    p1, = plt.plot(mysignal, 'b')
    #plt.legend([p1],["original signal"])

    plt.figure(1)
    p2, = plt.plot(trend, 'g--')
    #plt.legend([p2], ["trend"])

    plt.figure(2)
    p3, = plt.plot(noise_abs, 'r')
    #plt.legend([p3],["noise"])

    plt.legend([p1,p2,p3], ["original", "trend", "noise"])

    plt.show()

if __name__ == "__main__":
    main()
