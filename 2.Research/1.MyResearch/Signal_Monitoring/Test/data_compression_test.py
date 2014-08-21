# -*- coding: utf-8 -*-

def main():
    def only_comment():
        # 현재 계산한 measure
            # 1. Compression rate : ( #(after-non-zero) / # (before-non-zero))
            # 2. MSE
        pass

    def mydata(datanum, data_length):
        from data_call_test import data_call

        mysignal = data_call("PPG", datanum, data_length)
        return mysignal

    def test_gen_csv():
        qmf_cand = {'haar': [0],
                    'db': [4, 6, 8, 10, 12, 14, 16, 18, 20],
                    'beylkin': [0],
                    'coif': [1, 2, 3, 4, 5],
                    'symmlet': [4, 5, 6, 7, 8, 9, 10]}

        wavelet_param = [3, 4, 5, 6, 7, 8, 9]
        datanum = [1, 2, 3, 4]
        datalength = 2 ** 10

        my_result = {}

        import Wavelet as wv
        import csv

        with open('test.csv', 'wb') as test_file:
            file_writer = csv.writer(test_file)
            file_writer.writerow(["QMF NAME", "L", "Before zero", "After Zero", "Compression Rate", "MSE"])
            for data in datanum:
                temp_data = mydata(data, datalength)  # 데이터를 불러내자.
                for idx, key in enumerate(qmf_cand):
                    for order in qmf_cand[key]:
                        qmfname = key + str(order)
                        qmf = wv.qmf(key, order)  # QMF 건설이 끝났다.
                        for L in wavelet_param:
                            mse = 0
                            try:
                                wc = wv.FWT_PO(temp_data, L, qmf)
                                _, wc_compressed = wv.WaveShrink(wc, 'visu', L, qmf)
                                recons_compressed = wv.IWT_PO(wc_compressed, L, qmf)

                                before_zero = sum(x == 0.0 for x in wc)
                                after_zero = sum(x == 0.0 for x in wc_compressed)
                                for idx in range(len(temp_data)):
                                    temp = temp_data[idx] - recons_compressed[idx]
                                    mse += (temp ** 2)
                                compression_rate = float((len(temp_data) - after_zero)) / float(len(temp_data))
                                file_writer.writerow([qmfname, L, before_zero, after_zero, compression_rate, mse])
                            except:
                                print "error! at " + qmfname, " with ", L

    def read_csv():
        import csv
        import matplotlib.pyplot as plt

        with open("test.csv", 'r') as f:
            data = [row for row in csv.reader(f.read().splitlines())]
        return data


    def ranking(A):
        import operator
        kk = list(enumerate(A))
        temp = {}; final_temp = {}
        it_rank = 1
        my_rank = []

        for x,y in kk:
            temp.update({x:y})

        sorted_temp = sorted(temp.iteritems(), key=operator.itemgetter(1))
        for x,y in sorted_temp:
            final_temp.update({y:it_rank})
            it_rank +=1

        for x in A:
            my_rank.append(final_temp[x])

        return my_rank


    mycsv = read_csv()
    MSE = []
    Compression_rate = []
    it = 0
    for row in mycsv:
        if it > 0:
            MSE.append(row[5])
            Compression_rate.append(row[4])
        it += 1
    MSE = [float(x) for x in MSE]
    rank_MSE = ranking(MSE)

    Compression_rate = [float(x) for x in Compression_rate]
    rank_comp = ranking(Compression_rate)
    rank_sum = [x+y for x,y in zip(rank_MSE,rank_comp)]

    import csv
    with open("rank.csv", 'wb') as f:
        rank_write = csv.writer(f)
        #rank_write.writerow(mycsv[0])

        for x,y in list(enumerate(sorted(rank_sum))):
            loc = rank_sum.index(y)
            mycsv[loc].insert(0,x+1)
            mycsv[loc].append(y)
            rank_write.writerow(mycsv[loc])
            print mycsv[loc]
            # value is the sum of rank
            # We can compute rank_sum.index(rank_value)
            # The result of that is location index of that rank








if __name__ == "__main__":
    main()