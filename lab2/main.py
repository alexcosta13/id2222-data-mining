import argparse
import json
from time import time

from apriori import Apriori


def support(args, baskets):
    apriori = Apriori()
    count = apriori.aprori_algorithm(baskets, args.support)
    print(count)

    rules = apriori.generate_association_rules(count, args.confidence)
    print(rules)


def support_experiment(args, baskets):
    # Test a priori algorithm for different support values
    apriori = Apriori()

    for s in [0.01, 0.0075, 0.005, 0.0025]:
        start = time()
        count = apriori.aprori_algorithm(baskets, s)
        end = time()
        items = count.keys()
        length = len([item for item in items if len(item) == 1])

        print(f"A priori algorithm with support {s} took {end-start}s.")

        i = 1
        while length > 0:
            print(f"There are {length} frequent items of length {i} (support {s}).")
            i += 1
            length = len([item for item in items if len(item) == i])


def confidence_experiment(args, baskets):
    # Test associations for different support values and confidence values.
    apriori = Apriori()

    for s in [0.01, 0.009, 0.008]:
        count = apriori.aprori_algorithm(baskets, s)

        for c in [0.9, 0.8, 0.7]:
            rules = apriori.generate_association_rules(count, c)
            print(
                f"Generating associations rules with support {s} and confidence {c} yields {len(rules)} rules:"
            )
            print(json.dumps(rules, indent=2))


def main():
    with open("data/T10I4D100K.dat") as f:
        lines = f.read().splitlines()

    baskets = []
    for line in lines:
        line = line.strip()
        baskets.append(list(map(int, line.split(" "))))

    parser = argparse.ArgumentParser(description="INSERT DESCRIPTION.")
    parser.add_argument(
        "--support",
        "-s",
        type=float,
        default=0.01,
        help="support (default: 0.01)",
    )
    parser.add_argument(
        "--confidence",
        "-c",
        type=float,
        default=0.5,
        help="confidence (default: 0.5)",
    )
    parser.add_argument(
        "--s_experiment", dest="s_experiment", default=False, action="store_true"
    )
    parser.add_argument(
        "--c_experiment", dest="c_experiment", default=False, action="store_true"
    )

    args = parser.parse_args()

    if args.s_experiment:
        support_experiment(args, baskets)
    elif args.c_experiment:
        confidence_experiment(args, baskets)
    else:
        support(args, baskets)


if __name__ == "__main__":
    main()
