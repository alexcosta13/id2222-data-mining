import string


class Shingling:
    def __init__(self, k):
        """
        :param k: size of the shingles
        """
        self.k = k

    def shingle_document(self, document):
        """
        Transforms an input document of arbitrary lenght into a set of integers, which are
        the document's k-singles hashed.
        :param document: input document
        :return: set of integers corresponding to its hashed k-shingles
        """
        document = document.translate(str.maketrans("", "", string.punctuation))

        shingle = []
        for i in range(len(document) - self.k + 1):
            shingle.append(document[i : i + self.k])
        shingle = list(set(shingle))
        shingle = list(map(self.hash, shingle))
        shingle.sort()
        return shingle

    def hash(self, shingle):
        """
        Own implementation of a hash value to get smaller hashes than the regular Python implementation
        :param shingle: integer to be hashed
        :return: hashed value
        """
        return hash(shingle) % 4294971673
