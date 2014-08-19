__author__ = 'jeong-yonghan'

import scipy.io
import matplotlib.pyplot as plt
import numpy as np

def mat_read(filename):
    mymat = scipy.io.loadmat("Data/"+filename)
    mymat = mymat[filename]
    return np.array(mymat).tolist()

def visual(i, data, option):
    plt.figure(i)
    plt.plot(data, option)

def show():
    plt.show()

def array_to_list(array):
    return np.array(array).tolist()