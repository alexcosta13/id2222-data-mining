import argparse
from time import time

from apriori import Apriori


def support(args):
    with open('data/T10I4D100K.dat') as f:
        lines = f.read().splitlines()

    baskets = []
    for line in lines:
        line = line.strip()
        baskets.append(list(map(int, line.split(' '))))

    apriori = Apriori()
    count = apriori.aprori_algorithm(baskets, args.support)
    print(count)

    rules = apriori.generate_association_rules(count, args.confidence)
    print(rules)


def main():
    parser = argparse.ArgumentParser(description="INSERT DESCRIPTION.")
    parser.add_argument(
        "--support", "-s",
        type=int,
        default=1000,
        help="support (default: 1000)",
    )
    parser.add_argument(
        "--confidence", "-c",
        type=float,
        default=0.5,
        help="confidence (default: 0.5)",
    )

    args = parser.parse_args()

    support(args)


if __name__ == "__main__":
    main()
