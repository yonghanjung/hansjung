__author__ = 'jeong-yonghan'

import matplotlib.pyplot as plt
import numpy as np
import Module.Wavelet as wavelet

def mydata():
    from Module.data_call import data_call
    from Module.bandpass import butter_bandpass_filter

    testnum = 0
    mysignal = data_call("PPG_KW_long", testnum, 0)

    return testnum, mysignal


def conv(a,b, option = 'full'):
    lena = len(a)
    lenb = len(b)
    length = lena + lenb - 1

    a = a + [0] * (length-lena)
    b = b + [0] * (length - lenb)


    y = [0] * length

    for myiter in range(length):
        mysum = 0
        for idx in range(myiter+1):
            mysum += a[idx] * b[myiter - idx]
        y[myiter] = mysum

    if option == 'full':
        return y


    elif option == 'same':
        leny = len(y)
        tempnum = leny - lena
        if tempnum  % 2 == 0:
            tempb = tempnum/2
            tempa = tempnum - tempb
        else:
            tempb = tempnum/2
            tempa = tempnum - tempb
        for idx in range(tempa):
            y.pop(0)
        for idx in range(tempb):
            y.pop()
        return y




def main():
    testnum, mysignal = mydata()
    Fs = 75
    Sec = 5
    mysignal = mysignal[:Fs*Sec]

    plt.figure(0)
    plt.title("raw signal")
    plt.plot(mysignal,'b')


    bl = []
    for idx in range(31):
        if idx == 0:
            bl.append(1)
        elif idx == 15:
            bl.append(-2)
        elif idx == 30:
            bl.append(1)
        else:
            bl.append(0)
    al = [1, -2, 1]
    temp = [1] + [0]* 12

    hl = wavelet.myfilter(bl,al,temp)
    ppg_l = conv(mysignal,hl,'same')
    ppg_l = [x / 100 for x in ppg_l]



    plt.figure(1)
    plt.title("low-pass filtered")
    plt.plot(ppg_l)
    plt.show()

    print len(ppg_l), len(mysignal)





if __name__ == "__main__":
    main()



