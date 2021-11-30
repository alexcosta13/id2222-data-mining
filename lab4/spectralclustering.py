import numpy as np
from scipy.sparse import csr_matrix
from sklearn.cluster import KMeans

class SpectralClustering:
    def __init__(self):
        pass

    def get_affinity_matrix(self, edges):
        list_nodes_u = [u - 1 for u, v in edges]
        list_nodes_v = [v - 1 for u, v in edges]
        max_node = max(max(list_nodes_u, list_nodes_v))
        ones = np.ones(len(list_nodes_u))
        return csr_matrix((ones, (list_nodes_u, list_nodes_v)),
                          shape=(max_node + 1, max_node + 1)).todense()

    def get_diagonal(self, affinity_matrix):
        diag_values = np.sum(affinity_matrix, axis=1)
        diag_values = np.array(diag_values).squeeze()
        return np.diag(diag_values)

    def get_laplacian(self, diagonal_matrix, affinity_matrix):
        inv = np.linalg.inv(np.sqrt(diagonal_matrix))
        return inv @ affinity_matrix @ inv

    def find_largest_eigenvectors(self, laplacian_matrix, k):
        # eigh only works for real symmetric matrix
        _, eigenvectors = np.linalg.eigh(laplacian_matrix)
        return eigenvectors[:, -k:]

    def normalize_x(self, x_matrix):
        denom = (np.sqrt(np.sum(np.square(x_matrix), axis=1))).reshape(-1,1)
        return x_matrix / denom

    def k_means(self, list_points, k):
        kmeans = KMeans(n_clusters=k).fit(list_points)
        labels = kmeans.labels_
        print(labels)