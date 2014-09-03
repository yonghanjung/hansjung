# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

# Import Computation Module
import numpy as np
from sklearn import mixture

# Import Graph Module
import matplotlib.pyplot as plt


def data_generation():
    '''
    Random Number Generator
        - 2 modes
        - Type1 : u0, sig1, 100
        - Type2 : u10, sig1, 300
    '''

    np.random.seed(1)
    type1_rand = np.random.randn(100,1)
    type2_rand = 10 + np.random.randn(300,1)
    return np.concatenate( (type1_rand,type2_rand ))


def main():
    My_randn = data_generation()
    #print My_randn

    '''
    #Check How it looks like
    #1. Plotting 2 Mode Randn RV
    plt.figure(0)
    plt.title("Plotting 2 Mode Randn RV")
    plt.plot(My_randn)
    #plt.show()

    #2. Plotting 2 Mode Hist RV
    plt.figure(1)
    plt.title("Plotting 2 Mode Randn HIST")
    plt.hist(My_randn,50)
    plt.show()
    '''


    ## GMM
    # Declare GMM in SKlearn
    g = mixture.GMM(n_components=2)
    g.fit(My_randn)

    # Extract info from GMM
    print np.round(g.weights_, 2) # weight
    print np.round(g.means_, 2) # Means
    print np.round(g.covars_,2) # Digonal Covs
    print g.predict([[0], [2], [9], [10]])  # Predict where the rv belongs (이미 우리가 뽑은 rv는 1차원이니까 1차원 던져줌)

    #print np.round(g.score([[0], [2], [9], [10], [-0.02], [1000]]), 2) # g score가 뭐지? Compute the log probabiliy
    # Score는 log probability of each data point X.
    # 즉, 0에 가까울 수록 높고, -infinity에 가까울수록 이상해진다.








if __name__ == "__main__":
    main()
