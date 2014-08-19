from compiler.ast import flatten
import operator
import Wavelet as wavelet
import Data as data
import matplotlib.pyplot as plt
import General
import scipy.io
import bandpass as bp

__author__ = 'jeong-yonghan'

class data_compress(object):
    qmflist = {
        'haar' : [0],
        'db' : [4,6,8,10,12],
        'coif' : [1,2,3,4,5],
        'symmlet' : [4,5,6,7,8]
    }




def main():
    #'''
    #For the case of PPG
    mysignal = scipy.io.loadmat("Data/mynewdata2")
    mysignal = mysignal['mysignal2']
    mysignal = mysignal[:2**17]
    #'''

    '''
    # For the case of ECG_HE #
    mysignal = scipy.io.loadmat("Data/ECG_HE.mat")
    mysignal = mysignal['ECG_HE']
    mysignal = mysignal[15]
    mysignal = data.array_to_list(mysignal)
    '''

    """
    # For the case of ECG_MI #
    mysignal = scipy.io.loadmat("Data/ECG_MI.mat")
    mysignal = mysignal['ECG_MI']
    mysignal = mysignal[3]
    mysignal = data.array_to_list(mysignal)
    """

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
    #qmf = wavelet.qmf('db',4)

    L = 6

    '''
    # Wavelet Decomposition
    wc = wavelet.FWT_PO(mysignal,L,qmf)
    '''

    '''
    # Debugging
    #print wavelet.mirror_filt(qmf)
    #print wavelet.lshift(mysignal)
    #print len(wavelet.DownDyadHi(mysignal,qmf))
    '''

    #'''
    # TEST
    comp = data_compress()
    qmflist = comp.qmflist
    myqmf = {}

    for idx, qmfname in enumerate(qmflist):
        qmfpar_list = qmflist[qmfname]
        for par in qmfpar_list:
            myqmf.update({ qmfname + str(par) : wavelet.qmf(qmfname, par)} )
    #print myqmf

    wc_orig_zero = {}
    wc_denoised_zero = {}

    for idx, qmfname in enumerate(myqmf):
        qmf = myqmf[qmfname]
        wc = wavelet.FWT_PO(mysignal,L,qmf)
        _, wc_denoised = wavelet.WaveShrink(mysignal,'visu', L, qmf)
        wc_orig_zero.update( {qmfname : sum(1 for it in wc if it == 0.0)  }  )
        wc_denoised_zero.update( {qmfname : sum(1 for it in wc_denoised if it == 0.0)  }  )


    print sorted(wc_orig_zero.iteritems(), key=operator.itemgetter(1), reverse = True)
    print sorted(wc_denoised_zero.iteritems(), key=operator.itemgetter(1), reverse= True)



    '''
    # Wavelet Shrinkage
    denosed_signal, wc_denoised = wavelet.WaveShrink(mysignal, 'visu', L,qmf)

    wc_zero  = sum(1 for it in wc if it == 0.0)
    wc_denoised_zero = sum(1 for it in wc_denoised if it == 0.0)
    print wc_zero, wc_denoised_zero
    '''

    '''
    # Plotting
    plt.figure(0)
    plt.plot(mysignal,'b')

    plt.figure(1)
    plt.plot(denosed_signal,'g')
    #plt.plot(wc_denoised,'r')
    plt.show()
    '''

if __name__ == "__main__":
    main()
