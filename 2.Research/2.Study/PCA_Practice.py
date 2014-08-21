__author__ = 'jeong-yonghan'


# # PCA Practice
def random_gen():
    import numpy as np

    np.random.seed(234234782384239784)
    mu_vec1 = np.array([0, 0, 0])
    cov_mat1 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    class1_sample = np.random.multivariate_normal(mu_vec1, cov_mat1, 20).T
    assert class1_sample.shape == (3, 20), "The matrix has not the dimensions 3x20"

    mu_vec2 = np.array([1, 1, 1])
    cov_mat2 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    class2_sample = np.random.multivariate_normal(mu_vec2, cov_mat2, 20).T
    assert class1_sample.shape == (3, 20), "The matrix has not the dimensions 3x20"

    return class1_sample, class2_sample


def plotting():
    class1_sample, class2_sample = random_gen()

    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d import proj3d

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    plt.rcParams['legend.fontsize'] = 10
    ax.plot(class1_sample[0, :], class1_sample[1, :], class1_sample[2, :], 'o', markersize=8, color='blue', alpha=0.5,
            label='class1')
    ax.plot(class2_sample[0, :], class2_sample[1, :], class2_sample[2, :], '^', markersize=8, alpha=0.5, color='red',
            label='class2')

    plt.title('Samples for class 1 and class 2')
    ax.legend(loc='upper right')
    plt.show()


def myPCA():
    import numpy as np
    def mean_computing():
        class1_sample, class2_sample = random_gen()
        all_samples = np.concatenate((class1_sample, class2_sample), axis=1)
        assert all_samples.shape == (3, 40), "The matrix has not the dimensions 3x40"

        mean_x = np.mean(all_samples[0, :])
        mean_y = np.mean(all_samples[1, :])
        mean_z = np.mean(all_samples[2, :])

        mean_vector = np.array([[mean_x], [mean_y], [mean_z]])
        return mean_vector

    def cov_computing():
        # First, in COV embedded matrix
        class1_sample, class2_sample = random_gen()
        mean_vector = mean_computing()

        all_samples = np.concatenate((class1_sample,class2_sample), axis = 1)
        cov_mat = np.cov([all_samples[0,:],all_samples[1,:],all_samples[2,:]])

        # Second, in Scatter Matrix (Manual Computation)
        scatter_matrix = np.zeros((3,3))
        for i in range(all_samples.shape[1]):
            scatter_matrix += (all_samples[:,i].reshape(3,1)- mean_vector).dot((all_samples[:,i].reshape(3,1) - mean_vector).T)
        return cov_mat, scatter_matrix

    def eig_compute():
        cov_mat, scatter_matrix = cov_computing()

        eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)
        eig_val_sc, eig_vec_sc = np.linalg.eig(scatter_matrix)

        for i in range(len(eig_val_cov)):
            eigvec_sc = eig_vec_sc[:,i].reshape(1,3).T
            eigvec_cov = eig_vec_cov[:,i].reshape(1,3).T
            assert eigvec_sc.all() == eigvec_cov.all(), 'Eigenvectors are not identical'

            print('Eigenvector {}: \n{}'.format(i+1, eigvec_sc))
            print('Eigenvalue {} from scatter matrix: {}'.format(i+1, eig_val_sc[i]))
            print('Eigenvalue {} from covariance matrix: {}'.format(i+1, eig_val_cov[i]))
            print('Scaling factor: ', eig_val_sc[i]/eig_val_cov[i])
            print(40 * '-')

        for i in range(len(eig_val_sc)):
            eigv = eig_vec_sc[:,i].reshape(1,3).T
            np.testing.assert_array_almost_equal(scatter_matrix.dot(eigv),eig_val_sc[i] * eigv, decimal=6,err_msg='', verbose=True)

        return eig_val_cov, eig_vec_cov, eig_val_sc, eig_vec_sc

    def eig_visual():
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d
        from matplotlib.patches import FancyArrowPatch

        class Arrow3D(FancyArrowPatch):
            def __init__(self, xs, ys, zs, *args, **kwargs):
                FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
                self._verts3d = xs, ys, zs

            def draw(self, renderer):
                xs3d, ys3d, zs3d = self._verts3d
                xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
                self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
                FancyArrowPatch.draw(self, renderer)


        class1_sample, class2_sample = random_gen()
        all_samples = np.concatenate((class1_sample,class2_sample), axis = 1)
        eig_val_cov, eig_vec_cov, eig_val_sc, eig_vec_sc = eig_compute()

        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111, projection='3d')

        mean_x = np.mean(all_samples[0, :])
        mean_y = np.mean(all_samples[1, :])
        mean_z = np.mean(all_samples[2, :])

        ax.plot(all_samples[0,:], all_samples[1,:],all_samples[2,:], 'o', markersize=8, color='green', alpha=0.2)
        ax.plot([mean_x], [mean_y], [mean_z], 'o',markersize=10, color='red', alpha=0.5)

        for v in eig_vec_sc.T:
            a = Arrow3D([mean_x, v[0]], [mean_y, v[1]],[mean_z, v[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
            ax.add_artist(a)
        ax.set_xlabel('x_values')
        ax.set_ylabel('y_values')
        ax.set_zlabel('z_values')

        plt.title('Eigenvectors')

        plt.show()

    def reduce_pair():
        eig_val_cov, eig_vec_cov, eig_val_sc, eig_vec_sc = eig_compute()
        eig_pairs = [(np.abs(eig_val_sc[i]), eig_vec_sc[:,i]) for i in range(len(eig_val_sc))]
        eig_pairs.sort()
        eig_pairs.reverse()

        matrix_w = np.hstack((eig_pairs[0][1].reshape(3,1), eig_pairs[1][1].reshape(3,1)))
        return matrix_w


    def transform():
        class1_sample, class2_sample = random_gen()
        all_samples = np.concatenate((class1_sample,class2_sample), axis = 1)
        matrix_w = reduce_pair()
        transformed = matrix_w.T.dot(all_samples)
        assert transformed.shape == (2,40), "The matrix is not 2x40 dimensional."


def sklearn_practice():
    from sklearn.decomposition import PCA as sklearnPCA
    import numpy as np

    class1_sample, class2_sample = random_gen()
    all_samples = np.concatenate((class1_sample, class2_sample), axis=1)

    sklearn_pca = sklearnPCA(n_components=2)
    sklearn_transf = sklearn_pca.fit_transform(all_samples.T)

    return sklearn_transf

import numpy as np
A,B = random_gen()
print A
print "-" * 100
print B
print "-" * 100
C = np.concatenate((A,B) , axis = 1)
print C.T
print ""
print sklearn_practice()


    ## THING TO DO NOW
        # 1. understand 'reshape'
        # 2. understand 'dot