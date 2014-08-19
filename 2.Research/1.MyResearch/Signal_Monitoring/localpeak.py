import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import Wavelet as wavelet


class randomsignal:
    mysignal = scipy.io.loadmat('Data/mynewdata4.mat')
    mysignal = mysignal['mysignal4']
    #mysignal = mysignal[0]
    mysignal = list(mysignal)
    mysignal = [float(x) for x in mysignal]
    mysignal = mysignal[:8192]
    #mysignal = [1, 2, 3, 2, 1, 2, 3,1,2,3,1,2,3,1,2,3,1,2,3]

    qmf = wavelet.qmf('symmlet',8);

    L = 8
    mywc = wavelet.FWT_PO(mysignal,L,qmf);
    #mywc = wavelet.WaveShrink(mywc,'visu',L,qmf);
    mywc = wavelet.cutwavelet(mywc,L)
    #print mywc
    myrecons = wavelet.IWT_PO(mywc,L,qmf);




class peakdetect (randomsignal):
    mypeak = {}
    lookForMax = True
    myresult = []
    myindex = []
    distancetemp = []
    interval_thres = 250

    def peakdetector(self):
        #mysignal = self.mysignal
        mysignal = self.myrecons
        mymean = np.mean(mysignal)  + np.std(mysignal)
        #mymean = 4

        mypeak = self.mypeak
        lookForMax = self.lookForMax
        interval_thres = self.interval_thres

        if len(mysignal) > 1:
            for index in range(0, len(mysignal) - 2):
                currentpoint = mysignal[index]
                nextpoint = mysignal[index + 1]
                if lookForMax is True:
                    if currentpoint > nextpoint:
                        # Implemented by here 
                        lookForMax = False
                        if (currentpoint > mymean and len(mypeak) < 2) or \
                            (currentpoint > mymean and (index + 1) - mypeak.keys()[len(mypeak) - 1] > interval_thres):
                            mypeak.update({index + 1: currentpoint})

                else:
                    if currentpoint < nextpoint:
                        lookForMax = True

            currentpoint = mysignal[len(mysignal) - 1]
            prevpoint = mysignal[len(mysignal) - 2]

            if currentpoint > prevpoint and currentpoint > mymean:
                mypeak.update({len(mysignal): currentpoint})
                # if (mypeak.keys()[len(mypeak) - 1] -
                # mypeak.keys()[len(mypeak) - 2] <= interval_thres):

        else:
            mypeak.update({1: mysignal[0]})

        myresult = self.myresult
        myindex = self.myindex
        for key, value in mypeak.items():
            myindex.append(key)
            myresult.append(value)

        return myindex, myresult, mypeak


def main():

    mysignal = randomsignal()
    mysignal = mysignal.myrecons


    qmf = wavelet.qmf('symmlet',8);

    L = 8
    mywc = wavelet.FWT_PO(mysignal,L,qmf);
    #mywc = wavelet.WaveShrink(mywc,'visu',L,qmf);
    mywc = wavelet.cutwavelet(mywc,L)
    #print mywc
    myrecons = wavelet.IWT_PO(mywc,L,qmf);
    print len(myrecons), len(mysignal)

    peakpeak = peakdetect()
    myindex, mypeak, mydict = peakpeak.peakdetector()

    index = [x for x in range(len(mysignal))]
    #print mydict;


    plt.figure(0)
    plt.plot(index, mysignal)
    plt.plot(myindex, mypeak, 'ro')

    plt.figure(1)
    plt.plot(index, myrecons)
    plt.show()


if __name__ == "__main__":
    main()
