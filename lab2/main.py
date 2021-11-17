from apriori import Apriori


def main():
    with open('data/T10I4D100K.dat') as f:
        lines = f.read().splitlines()

    baskets = []
    for line in lines:
        line = line.strip()
        baskets.append(list(map(int, line.split(' '))))

    apriori = Apriori()
    print(apriori.aprori_algorithm(baskets, 0.005))


if __name__ == "__main__":
    main()
