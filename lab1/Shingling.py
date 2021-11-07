from CompareSet import CompareSet


class Shingling:
    def __init__(self, k):
        self.k = k

    def shingle_document(self, document):
        shingle = []
        for i in range(len(document) - self.k):
            shingle.append(document[i:i + self.k])
        shingle = list(set(shingle))
        shingle = list(map(self.hash, shingle))
        shingle.sort()
        return shingle

    def hash(self, shingle):
        return hash(shingle) % 2 ** 32


if __name__ == "__main__":
    f = open("data/225900newsML.txt", "r")
    doc = f.read()
    shing = Shingling(2)
    hashed_shing1 = shing.shingle_document(doc)

    f2 = open("data/120600newsML.txt", "r")
    doc2 = f2.read()
    hashed_shing2 = shing.shingle_document(doc2)

    compare = CompareSet()
    print(compare.jaccard_similarity(hashed_shing1, hashed_shing2))