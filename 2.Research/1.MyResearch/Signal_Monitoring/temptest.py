__author__ = 'jeong-yonghan'

from data_call import data_call
mydata = data_call("PPG_KW_long",0,0)

from adaptive_peak_module import adaptive_thr
A = adaptive_thr(data = mydata)
mymax = A[1]

import matplotlib.pyplot as plt
for key in sorted(mymax):
    plt.plot(key, mymax[key], 'ro')

print A[1]
plt.plot(mydata)
plt.plot(A[0],'g')
plt.show()