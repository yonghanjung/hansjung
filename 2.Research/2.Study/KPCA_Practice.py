__author__ = 'jeong-yonghan'

def main():
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA, KernelPCA
    from sklearn.datasets import make_circles

    def circle_data():
        np.random.seed(0)
        X,y = make_circles(n_samples= 400, factor=.3, noise=.05)
        return X,y

    def MyPCA():
        X,y = circle_data()
        kpca = KernelPCA(kernel='rbf', fit_inverse_transform=True, gamma= 10)
        X_kpca = kpca.fit_transform(X)
        pca = PCA()
        x_pca = pca.fit_transform(X)
        return X_kpca

    def original_plotting():
        X,y = circle_data()

        plt.figure()
        plt.subplot(1, 2, 1, aspect='equal')
        plt.title("Original space")
        reds = y == 0
        blues = y == 1

        plt.plot(X[reds, 0], X[reds, 1], "ro")
        plt.plot(X[blues, 0], X[blues, 1], "bo")

        plt.xlabel("$x_1$")
        plt.ylabel("$x_2$")

    def kpca_plotting():
        X,y = circle_data()
        X_kpca = MyPCA()
        original_plotting()

        plt.subplot(1,2,2, aspect = 'equal')
        reds = y == 0
        blues = y == 1

        plt.plot(X_kpca[reds, 0], X_kpca[reds, 1], "ro")
        plt.plot(X_kpca[blues, 0], X_kpca[blues, 1], "bo")
        plt.title("Projection by KPCA")
        plt.xlabel("1st principal component in space induced by $\phi$")
        plt.ylabel("2nd component")

    kpca_plotting()
    plt.show()





if __name__ == "__main__":
    main()