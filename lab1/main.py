from os import listdir
from time import time

from CompareSet import CompareSet
from CompareSignatures import CompareSignatures
from LSH import LSH
from MinHashing import MinHashing
from Shingling import Shingling

K = 10
N = 50
N_DOCUMENTS = 10
B = 5
R = 2
DIR = "other_data/"


def main():
    shing = Shingling(K)
    minhash = MinHashing(N)
    compare_sign = CompareSignatures()
    threshold = (1 / B) ** (1 / R)
    lsh = LSH(threshold, B, R, N_DOCUMENTS)
    files = [f for f in listdir(DIR)][:N_DOCUMENTS]
    sign_matrix = []

    for file in files:
        f = open(DIR + file, "r")
        doc = f.read()
        hashed_shing = shing.shingle_document(doc)
        col_doc = minhash.compute_signature(hashed_shing)
        sign_matrix.append(col_doc)
    candidate_pairs = lsh.find_candidates(sign_matrix)

    total_documents = 0
    for pair in candidate_pairs:
        i, j = pair
        if (compare_sign.compare(sign_matrix[i], sign_matrix[j])) > threshold:
            total_documents += 1
            print(f"Document {i} and Document {j} are very similar :) ")

    print(
        f"There are {total_documents} pairs of similar documents. We had {len(candidate_pairs)} candidate pairs."
    )


def jaccard_similarity():
    start = time()
    shing = Shingling(K)
    compare_set = CompareSet()
    files = [f for f in listdir(DIR)][:N_DOCUMENTS]
    hashed_sets = []
    for file in files:
        f = open(DIR + file, "r")
        doc = f.read()
        hashed_shing = shing.shingle_document(doc)
        hashed_sets.append(hashed_shing)
    ground_truth = {}
    for i in range(N_DOCUMENTS):
        for j in range(i + 1, N_DOCUMENTS):
            j_sim = compare_set.jaccard_similarity(hashed_sets[i], hashed_sets[j])
            ground_truth[(i, j)] = j_sim
    end = time()
    return ground_truth, end - start


def signature_comparison():
    start = time()
    shing = Shingling(K)
    minhash = MinHashing(N)
    compare_sign = CompareSignatures()
    files = [f for f in listdir(DIR)][:N_DOCUMENTS]
    sign_matrix = []

    for file in files:
        f = open(DIR + file, "r")
        doc = f.read()
        hashed_shing = shing.shingle_document(doc)
        col_doc = minhash.compute_signature(hashed_shing)
        sign_matrix.append(col_doc)

    labels = {}
    for i in range(N_DOCUMENTS):
        for j in range(i + 1, N_DOCUMENTS):
            j_sim = compare_sign.compare(sign_matrix[i], sign_matrix[j])
            labels[(i, j)] = j_sim
    end = time()
    return labels, end - start


def lsh_comparison():
    start = time()
    shing = Shingling(K)
    minhash = MinHashing(N)
    compare_sign = CompareSignatures()
    threshold = (1 / B) ** (1 / R)
    lsh = LSH(threshold, B, R, N_DOCUMENTS)
    files = [f for f in listdir(DIR)][:N_DOCUMENTS]
    sign_matrix = []

    for file in files:
        f = open(DIR + file, "r")
        doc = f.read()
        hashed_shing = shing.shingle_document(doc)
        col_doc = minhash.compute_signature(hashed_shing)
        sign_matrix.append(col_doc)
    candidate_pairs = lsh.find_candidates(sign_matrix)

    labels = {}
    for pair in candidate_pairs:
        i, j = pair
        if (compare_sign.compare(sign_matrix[i], sign_matrix[j])) > threshold:
            j_sim = compare_sign.compare(sign_matrix[i], sign_matrix[j])
            labels[(i, j)] = j_sim

    end = time()
    return labels, end - start


if __name__ == "__main__":
    gt, jaccard_time = jaccard_similarity()
    print(jaccard_time)
    sign_labels, signatures_time = signature_comparison()
    print(len(sign_labels), signatures_time)
    lsh_labels, lsh_time = lsh_comparison()
    print(len(lsh_labels), lsh_time)
