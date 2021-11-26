from triestbase import TriestBase
from triestimpr import TriestImpr

M = 2000


def main():
    with open("data/facebook.txt") as f:
        lines = f.read().splitlines()

    edges = []
    for line in lines:
        line = line.strip()
        edges.append(tuple(map(int, line.split(" "))))

    print("Number of edges:", len(edges))

    tb = TriestBase(M)
    tb = TriestImpr(M)
    for edge in edges:
        tb.process_sample(edge)

    print("Total number of triangles:", tb.get_triangle_count())


if __name__ == "__main__":
    main()
