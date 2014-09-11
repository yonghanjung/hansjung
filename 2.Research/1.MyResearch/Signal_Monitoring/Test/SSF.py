# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'


import numpy as np
import matplotlib.pyplot as plt


def main():
    testnum, mysignal = mydata()
    Fs = 75
    Sec = 3
    train_sig = mysignal[:Fs * Sec]
    new_train_sig = SSF_newsignal(train_sig,window_size=10)
    print len(train_sig), len(new_train_sig)
    test_sig = mysignal[Fs*Sec:]

    plt.figure(0)
    plt.title("Raw Train signal and Train SSF signal")
    plt.plot(train_sig,'b')
    plt.plot([0] * 10 +  new_train_sig,'r')

    window_size = 10
    new_sig = SSF_newsignal(test_sig, window_size)


    mypeak = {}
    prev = new_sig[0]
    cur = new_sig[1]
    next = new_sig[2]
    #print len(new_sig), len(train_sig)

    for idx in range(3,len(new_sig)):
        #print prev, cur, next, saddle(prev,cur,next)
        if saddle(prev,cur,next) == "peak" and idx > window_size and new_sig[idx] > np.mean(new_train_sig):
            #mypeak.update( { idx + window_size : new_sig[idx-1]} )
            mypeak.update( { idx + window_size - 2  : cur } )

        prev = cur
        cur = next
        next = new_sig[idx]

    plt.figure(1)
    plt.title("Test signal and SSF test signal")
    plt.plot(test_sig,'b')
    plt.plot([0] * window_size + new_sig,'r')


    for key in mypeak:
        plt.plot( key, mypeak[key], 'ro'   )

    print mypeak
    plt.show()


def saddle(prev,cur,next):
    # prev는 Thres의 마지막 포인트
    # cur은 들어오는 신호
    # next는 바로 다음에 들어오는 신호
    if prev < cur:
        if next <= cur:
            return "peak"
        else:
            return "inc"
    else:
        return "dec"



def SSF_newsignal(train_signal, window_size):
    rem_size = len(train_signal)
    train_signal = train_signal + [0] * window_size
    new_sig = []
    for idx in range(rem_size):
        temp = train_signal[idx : idx + window_size]
        new_sig.append(SSF(temp))
    return new_sig



def SSF(window):
    diff_window = list_difference(window)
    modi = []

    for x in diff_window:
        if x > 0:
            modi.append(x)
        else:
            modi.append(0)

    #return sum(x for x in modi)
    return sum(x for x in modi)


def list_difference(mylist):
    return [y-x for y, x in  zip(mylist[1:] , mylist[:-1] )    ]


def mydata():
    from Module.data_call import data_call
    from Module.bandpass import butter_bandpass_filter

    testnum = 2
    mysignal = data_call("PPG_KW_long", testnum, 0)

    #mysignal = butter_bandpass_filter(mysignal,0.125,10,1000)
    return testnum, mysignal



if __name__ == "__main__":
    main()
