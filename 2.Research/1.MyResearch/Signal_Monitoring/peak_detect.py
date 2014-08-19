# -*- coding: utf-8 -*-

__author__ = 'jeong-yonghan'

'''
Code for detecting peaks
'''

import matplotlib.pyplot as plt


class peak_detect(object):
    def __init__(self, mysignal, start, slope):
        self.mysignal = mysignal
        self.start = start
        self.slope = slope
        self.length = len(mysignal)
        self.where_cross = {}
        self.mynewthr = []
        self.my_peak = {}
        self.mymode = ""
        self.my_thr = []
        self.new_start = self.start


    def thr_line(self):
        for idx in range(self.length):
            self.my_thr.append(self.start + idx * self.slope)
        return self.my_thr


    def peak_detect(self):
        self.mythr = self.thr_line()
        def check_cross(thr_prev, thr_now, sig_prev, sig_now):
            if thr_prev > sig_prev:
                if thr_now <= sig_now:
                    return True
                else:
                    return False
            else:
                return False
        self.check_cross = check_cross
        # Initializing
        it_count = 0
        self.it_count = it_count
        prev_thr = 0
        prev_sig = 0
        self.prev_thr = prev_thr
        self.prev_sig = prev_sig

        # Picking up the cross point
        for thr_it, sig_it in zip(self.mythr, self.mysignal):
            cur_thr = thr_it
            cur_sig = sig_it

            if self.check_cross(self.prev_thr, cur_thr, self.prev_sig, cur_sig):
                self.where_cross.update({self.it_count: cur_thr})
                self.mymode = 'sig'

            if self.mymode == "sig":
                if cur_sig > self.prev_sig:
                    self.mynewthr.append(cur_sig)
                else:
                    self.mymode = "thr"
                    self.start = cur_sig
                    self.new_start = self.start
                    self.mynewthr.append(self.start + self.it_count * self.slope)
                    self.my_peak.update({self.it_count: self.prev_sig})
            else:
                if len(self.my_peak.keys())-1 >= 0:
                    self.mynewthr.append( self.my_peak[ self.my_peak.keys()[len(self.my_peak.keys())-1]] + self.it_count * self.slope)
                    print self.my_peak
                else :
                    self.mynewthr.append(self.new_start + self.it_count * self.slope)
            self.prev_thr = cur_thr
            self.prev_sig = cur_sig
            self.it_count += 1
        return self.mynewthr, self.my_peak



def main():
    # Call My Data
    from data_call import data_call

    mysignal = data_call("PPG_KW", 1, 0)

    # Setting for Threshold #
    start = 150
    slope = -0.1

    # Start Algorithm #
    mypeak = peak_detect(mysignal, start, slope)
    mynewthr, my_peak = mypeak.peak_detect()

    for key in sorted(my_peak):
        plt.plot(key, my_peak[key],'ro')

    plt.plot(mysignal)
    plt.plot(mynewthr)

    plt.show()


if __name__ == "__main__":
    main()