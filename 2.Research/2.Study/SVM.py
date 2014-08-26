__author__ = 'jeong-yonghan'


import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

def create_data():
    num = 1000
    dim = 2
    np.random.seed(0)
    X = np.r_[1000000 * np.random.randn(num, dim) - [2, 2], 1000000 * np.random.randn(num, dim) + [2, 2]]
    Y = [-1] * num + [1] * num
    return [X,Y]

Mydata = create_data()
X = Mydata[0]
y = Mydata[1]

print X
print y
clf = svm.SVC(kernel = "linear")
print clf.fit(X,y)

