# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

from matplotlib.pyplot import *
from numpy import *

def main():
    t = linspace(-5,5,300) # redefine this here for convenience
    fig = figure()
    fs=5.0
    ax = fig.add_subplot(111) # create axis hand
    ax.plot(t,sinc(fs * t))
    ax.grid()
    show()



if __name__ == "__main__":
    main()
