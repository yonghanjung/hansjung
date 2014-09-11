# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

import numpy as np
import matplotlib.pyplot as plt

def main():
    # TRAIN
    testnum, mysignal = mydata()
    fs = 75
    sec = 3
    see = 30
    train_sig = mysignal[:fs*sec]
    test_sig = mysignal[fs*sec : fs*sec + fs*see]
    window_size = 13

    SSF_train = SSF_newsignal(train_signal= train_sig, window_size= window_size)
    SSF_train = [0] * window_size + SSF_train

    plt.figure(0)
    #plt.title(str(testnum)+ "th train signal")
    plt.title(str(testnum) + "th raw signal " + str(window_size) +  " samples window")
    plt.plot(train_sig,'b')
    plt.plot(SSF_train,'r')
    #plt.show()

    ## Threshold
    adap, train_max = adaptive_thr(SSF_train,Fs=fs)
    for key in train_max:
        plt.plot(key, train_max[key],'bo')
    plt.plot(adap.keys(), adap.values(),'g')



    ## Real test
    down_thres = np.mean(train_max.values()) / 2

    mythr = {}
    for idx in range(len(SSF_train)):
        mythr.update ( { idx : down_thres   }   )
    plt.plot(mythr.keys(), mythr.values(), 'r--')

    init_window1 = train_sig[len(train_sig)-1 -window_size  : len(train_sig)-1]
    init_window2 = train_sig[len(train_sig) -2 - window_size : len(train_sig)-2]
    prev = SSF(init_window2)
    cur = SSF(init_window1)
    window = init_window1
    mypeak_test  = {}
    mypeak_SSF = {}


    for idx in range(len(test_sig)):
        window.append(test_sig[idx])
        window.pop(0)
        next = SSF(window)

        if saddle(prev,cur,next) == "peak" and cur > down_thres:
            mypeak_test.update( {   idx : test_sig[idx]       }    )
            mypeak_SSF.update( {idx - window_size: cur  }  )

        prev = cur
        cur = next

    plt.figure(1)
    SSF_test = SSF_newsignal(train_signal=test_sig, window_size= window_size)
    plt.title(str(testnum)+ "th test signal " + str(window_size) + " samples window")
    plt.plot(test_sig,'b')
    plt.plot(SSF_test,'r')
    for key in mypeak_test:
        plt.plot(key,mypeak_test[key],'bo')
    for key in mypeak_SSF:
        plt.plot(key,mypeak_SSF[key],'ro')

    mythr = {}
    for idx in range(len(test_sig)):
        mythr.update ( { idx : down_thres   }   )
    plt.plot(mythr.keys(), mythr.values(), 'r--')

    plt.show()

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


def check_cross(prev_thr, prev_sig, cur_thr, cur_sig):
    if prev_thr > prev_sig:
        if cur_thr < cur_sig:
            return True
            # 크로스포인트는 과거와 현재 사이에 찍힌다.
            # 즉, 현재포인트부터 신호를 받는게 좋다.
        else:  # cur_thr > cur_sig
            return False
    else:
        return False


def adaptive_thr(mysignal, Fs):
    mymax = {}

    # 우리가 가진 수식들.
    Vpeak = 0
    StdPPG = np.std(mysignal)
    thr_old = 0.5 * np.max(mysignal)
    thr_new = 0
    Sr = -0.3
    cur_loc = 0
    prev_loc = 0
    refract = 0.6

    # slope = -0.75
    # start = 0.2*max(mysignal)
    adap = {}
    mode = 'thr'
    cross = False


    for idx in range(len(mysignal)):

        # 모드 : sig, thr
        # thr 모드 : 직선을 타고 내려간다.
        # sig 모드 : 신호를 타고 올라간다.

        # 알고리즘
        # 시작은 thr모드
        # 기울기0, 스타트0 으로 직선을 그린다.
        # 교차인지 확인
        # 만일 교차가 아니라면 계속 thr모드로 진행
        # 교차면 sig모드 변환
        # 다음 iteration
        # sig모드이면
        # increasing 이면 타고 올라간다.
        # decreasing 이면 thr 모드 변환
        # 현재의 신호 포인트를 맥스로 저장
        # slope은 그대로
        # start는 맥스
        # 새로운 x를 잡아서 진행한다.
        # 다음 iteration

        # MODE CHECK
        if idx > 0:
            prev_thr = adap[idx-1]
            cur_thr = adap[idx-1]+ (Sr * (( Vpeak + StdPPG) / Fs))
            prev_sig = mysignal[idx - 1]
            cur_sig = mysignal[idx]
            cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig)
        else:
            pass

        if mode == 'thr':
            if cross == False:
                mode = 'thr'
                if idx == 0:
                    thr_new = thr_old + (Sr * (( Vpeak + StdPPG) / Fs))
                else:
                    thr_new = adap[idx-1] + (Sr * (( Vpeak + StdPPG) / Fs))
                #adap_it += 1
                #adap.append(thr_new)
                adap.update( {idx :thr_new }  )

            elif cross == True:
                if prev_loc != 0:
                    if idx - prev_loc < refract * Fs:
                        mode = 'thr'
                    else:
                        mode = 'sig'
                else:
                    mode = 'sig'
                adap.update( {idx : cur_sig}  )
                #adap.append(cur_sig)
                #adap_it += 1
                continue

        elif mode == 'sig':
            if cur_sig >= prev_sig:
                adap.update({idx : cur_sig})

            else:
                prev_loc = cur_loc
                cur_loc = idx-1
                new_thr = prev_sig + (Sr * (( Vpeak + StdPPG) / Fs))
                adap.update({idx : new_thr} )

                mode = 'thr'
                mymax.update({idx-1: prev_sig})
                Vpeak = prev_sig
                continue
    return adap, mymax


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

    testnum = 1
    mysignal = data_call("PPG_KW_long", testnum, 0)

    #mysignal = butter_bandpass_filter(mysignal,0.125,10,1000)
    return testnum, mysignal


if __name__ == "__main__":
    main()
