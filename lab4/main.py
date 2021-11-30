from spectralclustering import SpectralClustering

def main():
    with open("data/example1.dat") as f:
        lines = f.read().splitlines()

    edges = []
    for line in lines:
        line = line.strip()
        edges.append(tuple(map(int, line.split(","))))

    spectral_clust = SpectralClustering()
    affinity_matrix = spectral_clust.get_affinity_matrix(edges)
    diagonal_matrix = spectral_clust.get_diagonal(affinity_matrix)
    laplacian = spectral_clust.get_laplacian(diagonal_matrix, affinity_matrix)
    x_matrix = spectral_clust.find_largest_eigenvectors(laplacian,10)
    norm_x = spectral_clust.normalize_x(x_matrix)
    spectral_clust.k_means(norm_x, 10)


if __name__ == "__main__":
    main()
