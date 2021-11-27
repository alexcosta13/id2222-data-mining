import argparse
import time

import matplotlib.pyplot as plt

from triestbase import TriestBase
from triestimpr import TriestImpr

M = 2000


def triest(args, edges):
    start = time.time()

    tb = TriestImpr(args.M) if args.impr else TriestBase(args.M)
    for edge in edges:
        tb.process_sample(edge)

    print(f"Number of edges: {len(edges)}\n"
          f"Estimated number of triangles: {tb.get_triangle_count()}\n"
          f"Reservoir size: {args.M}\tTime: {time.time() - start}s")


def m_experiment(args, edges):
    xs, ys = [], []
    for m in [1000 * i for i in range(1, 10)]:
        tb = TriestImpr(args.M) if args.impr else TriestBase(args.M)
        for edge in edges:
            tb.process_sample(edge)
        xs.append(m)
        ys.append(tb.get_triangle_count())

    plt.plot(xs, ys)
    plt.show()


def variance_experiment(edges):
    pass


def main():
    with open("data/facebook.txt") as f:
        lines = f.read().splitlines()

    edges = []
    for line in lines:
        line = line.strip()
        edges.append(tuple(map(int, line.split(" "))))

    parser = argparse.ArgumentParser(description="INSERT DESCRIPTION.")
    parser.add_argument(
        "-M",
        type=int,
        default=1000,
        help="M (default: 1000, min: 6)",
    )
    parser.add_argument(
        "--impr", "--improved", "-I",
        dest="impr",
        default=False,
        action="store_true",
        help="run triest-impr algorithm",
    )
    parser.add_argument(
        "--m_experiment",
        dest="m_experiment",
        default=False,
        action="store_true",
        help="run M experiment",
    )
    parser.add_argument(
        "--v_experiment",
        dest="v_experiment",
        default=False,
        action="store_true",
        help="run variance experiment",
    )
    args = parser.parse_args()

    if args.m_experiment:
        m_experiment(args, edges)
    elif args.v_experiment:
        variance_experiment(edges)
    else:
        triest(args, edges)


if __name__ == "__main__":
    main()
