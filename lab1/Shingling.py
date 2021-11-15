import string


class Shingling:
    def __init__(self, k):
        self.k = k

    def shingle_document(self, document):
        document = document.translate(str.maketrans("", "", string.punctuation))

        shingle = []
        for i in range(len(document) - self.k + 1):
            shingle.append(document[i : i + self.k])
        shingle = list(set(shingle))
        shingle = list(map(self.hash, shingle))
        shingle.sort()
        return shingle

    def hash(self, shingle):
        return hash(shingle) % 4294971673
