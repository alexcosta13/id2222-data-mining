import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from spectralclustering import SpectralClustering


def draw_graph(graph_name, labels=None):
    graph = nx.Graph()
    filename = "data/" + graph_name + ".dat"
    edge_list = nx.read_edgelist(
        filename, delimiter=",", nodetype=int, data=(("weight", int),)
    )
    graph.add_nodes_from(sorted(edge_list.nodes.keys()))
    graph.add_edges_from(edge_list.edges)
    title = f"{graph_name}" if labels is None else f"Classified {graph_name}"
    plt.title(title)
    nx.draw(graph, node_size=30, node_color=labels, edge_color="grey")
    plt.show()


def show_plots(data):
    draw_graph(data["graph"])
    draw_graph(data["graph"], data["labels"])
    if data["affinity"] is not None:
        plt.spy(data["affinity"])
        plt.title("Affinity matrix")
        plt.show()
    if data["eigenvalues"] is not None:
        plt.plot(
            range(1, len(data["eigenvalues"]) + 1), sorted(data["eigenvalues"])[::-1]
        )
        plt.title("Sorted eigenvalues")
        plt.show()
    if data["fiedler_vector"] is not None:
        plt.plot(data["fiedler_vector"])
        plt.title("Fiedler vector")
        plt.show()


def main():
    for graph in ["example1", "example2"]:
        filename = "data/" + graph + ".dat"
        with open(filename) as f:
            lines = f.read().splitlines()

        edges = []
        for line in lines:
            line = line.strip()
            edges.append(tuple(map(int, line.split(",")))[:2])

        spectral_clustering = SpectralClustering()
        affinity_matrix = spectral_clustering.get_affinity_matrix(edges)
        diagonal_matrix = spectral_clustering.get_diagonal(affinity_matrix)
        laplacian = spectral_clustering.get_laplacian(diagonal_matrix, affinity_matrix)
        (
            laplacian_eigenvalues,
            laplacian_eigenvectors,
        ) = spectral_clustering.find_eigenvectors(laplacian)
        K = spectral_clustering.optimal_k(laplacian_eigenvalues)
        x_matrix = laplacian_eigenvectors[:, -K:]
        norm_x = spectral_clustering.normalize_x(x_matrix)
        labels = spectral_clustering.k_means(norm_x, K)

        (
            u_laplacian_eigenvalues,
            u_laplacian_eigenvectors,
        ) = spectral_clustering.find_eigenvectors(diagonal_matrix - affinity_matrix)
        fiedler_vector = spectral_clustering.get_fiedler_vector(
            u_laplacian_eigenvalues, u_laplacian_eigenvectors
        )
        fiedler_vector = np.sort(np.array(fiedler_vector).squeeze())

        data = {
            "graph": graph,
            "labels": labels,
            "affinity": affinity_matrix,
            "eigenvalues": laplacian_eigenvalues,
            "fiedler_vector": fiedler_vector,
        }

        show_plots(data)


if __name__ == "__main__":
    main()
