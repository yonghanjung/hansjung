# -*- coding: utf-8 -*-

__author__ = 'jeong-yonghan'

'''
작업플로우
1. Peak을 계산해서
2. HRV 계산

'''


def main():
    def RR_loc():
        from data_call import data_call

        mysignal = data_call("PPG_KW", 1, 0)

        from peak_detect import adaptive_thr

        initial_info = [100, -0.75]
        A = adaptive_thr(data=mysignal, initial_info=initial_info)
        peak_data = A[1]  # {Peak loc : Peak info}
        temp_peak = {}
        for x, y in enumerate(peak_data):
            time_data = float(y) / float(75)
            temp_peak.update({time_data: peak_data[y]})
        MyRR_loc = sorted(temp_peak)
        RR_interval = [j - i for i, j in zip(MyRR_loc[:-1], MyRR_loc[1:])]
        return [MyRR_loc, RR_interval]

    def chunks(l, n):  # l = lists // n = # of chunks
        if n < 1:
            n = 1
        return [l[i:i + n] for i in range(0, len(l), n)]

    def meanNN(RR_interval, howmany):
        import numpy as np
        splited_RR_interval = chunks(RR_interval, howmany)
        MymeanNN = []
        for x in splited_RR_interval:
            MymeanNN.append(np.mean(x))

        return MymeanNN

    def stdNN(RR_interval, howmany):
        import numpy as np
        splited_RR_interval = chunks(RR_interval, howmany)
        MystdNN = []
        for x in splited_RR_interval:
            MystdNN.append(np.std(x))

        return MystdNN

    def RMSNN(RR_interval, howmany):
        import numpy as np
        splited_RR_interval = chunks(RR_interval,howmany)
        myRMSNN = []
        for x in splited_RR_interval:
            myRMSNN.append(np.RMS)


if __name__ == "__main__":
    main()
