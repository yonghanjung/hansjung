from compiler.ast import flatten
import operator
import scipy.io
import Wavelet as wavelet
import numpy as np

__author__ = 'jeong-yonghan'


class data_compress(object):
    qmflist = {
        'haar': [0],
        'db': [4, 6, 8, 10, 12, 14, 16, 18, 20],
        'coif': [1, 2, 3, 4, 5],
        'symmlet': [4, 5, 6, 7, 8, 9, 10]
    }


def main():
    '''
    #For the case of PPG
    mysignal = scipy.io.loadmat("../Data/mynewsignal")
    mysignal = mysignal['mysignal']
    mysignal = mysignal[0] #temp for mynewsignal
    #mysignal = np.array(mysignal).tolist()
    print len(mysignal)
    mysignal = mysignal[:2 ** 14]
    '''

    mysignal = scipy.io.loadmat("../Data/mynewdata3")
    mysignal = mysignal['mysignal3']
    mysignal = np.array(mysignal).tolist()
    mysignal = flatten(mysignal)
    mysignal = mysignal[:2 ** 14]


    # Initial Check
    print len(mysignal)
    L = 8

    # TEST
    comp = data_compress()
    qmflist = comp.qmflist
    myqmf = {}

    for idx, qmfname in enumerate(qmflist):
        qmfpar_list = qmflist[qmfname]
        for par in qmfpar_list:
            myqmf.update({qmfname + str(par): wavelet.qmf(qmfname, par)})
    print myqmf

    wc_orig_zero = {}
    wc_denoised_zero = {}
    MSE = {}

    for idx, qmfname in enumerate(myqmf):
        qmf = myqmf[qmfname]
        wc = wavelet.FWT_PO(mysignal, L, qmf)
        xh, wc_denoised = wavelet.WaveShrink(mysignal, 'visu', L, qmf)
        wc_orig_zero.update({qmfname: sum(1 for it in wc if it == 0.0)})
        wc_denoised_zero.update({qmfname: sum(1 for it in wc_denoised if it == 0.0)})
        MSE.update({qmfname : sum((a-b)**2 for a,b in zip(mysignal,xh) )})

    print sorted(wc_orig_zero.iteritems(), key=operator.itemgetter(1), reverse=True)
    print sorted(wc_denoised_zero.iteritems(), key=operator.itemgetter(1), reverse=True)
    print sorted(MSE.iteritems(), key=operator.itemgetter(1))



if __name__ == "__main__":
    main()
