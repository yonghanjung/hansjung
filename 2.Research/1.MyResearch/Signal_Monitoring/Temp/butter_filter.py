# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'


import numpy as np
import matplotlib.pyplot as plt




def main():
    testnum, mysignal = mydata()
    Fs = 75
    Sec = 5

    plt.figure(0)
    plt.title(str(testnum) + "th Raw PPG Signal")
    plt.plot(mysignal[:Fs * Sec],'b')


    ### SSF
    win_size =  1000
    window = []
    SSF = {}

    for idx in range(len(mysignal )):
        if idx > 30:
            window  = mysignal[idx - 30 : idx]

        SSF_val = sum(list_difference(window))
        SSF.update( {idx   : SSF_val}   )


    #plt.figure(1)
    #plt.title(str(testnum) + "th Filtered Signal")
    plt.plot(SSF.values()[:Fs * Sec],'r')

    print len(mysignal), len(SSF.values())
    plt.show()

def list_difference(mylist):
    return [y-x for y, x in  zip(mylist[1:] , mylist[:-1] )    ]



# DATA IMPORT
def mydata():
    from Module.data_call import data_call
    from Module.bandpass import butter_bandpass_filter

    testnum = 1
    mysignal = data_call("PPG_KW_long", testnum, 0)

    #mysignal = butter_bandpass_filter(mysignal,0.125,10,1000)
    return testnum, mysignal





if __name__ == "__main__":
    main()
