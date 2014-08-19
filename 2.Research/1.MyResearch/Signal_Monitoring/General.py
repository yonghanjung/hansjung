__author__ = 'jeong-yonghan'

def zeros(n):
    return [0] * n


def sign(x):
    n = len(x)
    y = zeros(n)
    for i in range(n):
        if x[i] > 0 :
            y[i] = 1
        elif x[i] == 0:
            y[i] = 0
        else:
            y[i] = -1
    return y


def zerocount(x):
    return sum(y == 0.0 for y in x)


def dotproduct(A,B):
    return [x*y for x,y in zip(A,B)]