# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

from scipy.signal import butter, lfilter, freqz
import numpy as np
import matplotlib.pyplot as plt
import bandpass as bp


'''
def butter_bandpass(lowcut, highcut, fs, order = 5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b,a = butter(order, [low, high], btype='band')
    return b,a


def butter_bandpass_filter(data,lowcut,highcut,fs,order = 5):
    b,a = butter_bandpass(lowcut,highcut,fs,order=order)
    y = lfilter(b,a,data)
    return y


def main():
    # 샘플레이트로 신호를 읽어서, 신호를 원하는 주파수 레벨로 자른다.
    fs = 5000.0
    lowcut = 500.0
    highcut = 1250.0

    # 여러 order별로 bandpass filter가 어떻게 그려지는지 보여준다.
    plt.figure(1)
    plt.clf()
    for order in [3,6,9]:
        b,a = butter_bandpass(lowcut,highcut,fs,order = order)
        w, h = freqz(b,a,worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label = "order = %d" % order)

    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],'--', label='sqrt(0.5)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')

    # NOISE Signal 을 만들어본다.
    T = 0.5
    nsamples = T*fs
    t = np.linspace(0,T,nsamples, endpoint=False)
    a = 0.02
    f0 = 600.0
    x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
    x += a * np.cos(2 * np.pi * f0 * t + .11)
    x += 0.03 * np.cos(2 * np.pi * 2000 * t)
    plt.figure(2)
    plt.clf()
    plt.plot(t,x,label = "noisy signal")


    #BANDPASS FILTERING
    y = butter_bandpass_filter(x,lowcut,highcut,fs,order=6)
    plt.plot(t, y, label='Filtered signal (%g Hz)' % f0)
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, T, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()



if __name__ == "__main__":
    main()
'''
fs = 5000.0
T = 0.5
nsamples = T*fs
t = np.linspace(0,T,nsamples, endpoint=False)
a = 0.2
f0 = 600.0
x = np.sin(2 * np.pi * 1.2 * np.sqrt(t))
x += 0.1 * np.cos(2 * np.pi * 100 * t + 0.1)
x += a * np.cos(2 * np.pi * f0 * t + .11)
x += 0.3 * np.cos(2 * np.pi * 200 * t)

lowcut = 600.0
highcut = 1250.0

a = bp.butter_bandpass_filter(x,lowcut,highcut,fs,order = 5)
plt.plot(x)
#plt.plot(a,'r')
plt.show()
