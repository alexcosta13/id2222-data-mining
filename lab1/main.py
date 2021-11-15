import argparse
from os import listdir
from time import time

from CompareSet import CompareSet
from CompareSignatures import CompareSignatures
from LSH import LSH
from MinHashing import MinHashing
from Shingling import Shingling


def jaccard_similarity(args):
    start = time()
    shingles = Shingling(args.k_shingle)
    compare_set = CompareSet()
    files = [f for f in listdir(args.data_dir)][: args.n_documents]
    hashed_sets = []
    for file in files:
        f = open(args.data_dir + file, "r")
        doc = f.read()
        hashed_shing = shingles.shingle_document(doc)
        hashed_sets.append(hashed_shing)
    ground_truth = {}
    for i in range(args.n_documents):
        for j in range(i + 1, args.n_documents):
            j_sim = compare_set.jaccard_similarity(hashed_sets[i], hashed_sets[j])
            if j_sim > args.similarity_threshold:
                ground_truth[(i, j)] = j_sim
    end = time()
    return ground_truth, end - start


def signature_comparison(args):
    start = time()
    shingles = Shingling(args.k_shingle)
    minhash = MinHashing(args.hash_signatures)
    compare_sign = CompareSignatures()
    files = [f for f in listdir(args.data_dir)][: args.n_documents]
    sign_matrix = []

    for file in files:
        f = open(args.data_dir + file, "r")
        doc = f.read()
        hashed_shing = shingles.shingle_document(doc)
        col_doc = minhash.compute_signature(hashed_shing)
        sign_matrix.append(col_doc)

    labels = {}
    for i in range(args.n_documents):
        for j in range(i + 1, args.n_documents):
            j_sim = compare_sign.compare(sign_matrix[i], sign_matrix[j])
            if j_sim > args.similarity_threshold:
                labels[(i, j)] = j_sim
    end = time()
    return labels, end - start


def lsh_comparison(args):
    start = time()
    shingles = Shingling(args.k_shingle)
    minhash = MinHashing(args.hash_signatures)
    compare_sign = CompareSignatures()
    lsh = LSH(args.lsh_bands)
    files = [f for f in listdir(args.data_dir)][: args.n_documents]
    sign_matrix = []

    for file in files:
        f = open(args.data_dir + file, "r")
        doc = f.read()
        hashed_shing = shingles.shingle_document(doc)
        col_doc = minhash.compute_signature(hashed_shing)
        sign_matrix.append(col_doc)
    candidate_pairs = lsh.find_candidates(sign_matrix)

    labels = {}
    for pair in candidate_pairs:
        i, j = pair
        j_sim = compare_sign.compare(sign_matrix[i], sign_matrix[j])
        if j_sim > args.similarity_threshold:
            labels[(i, j)] = j_sim

    end = time()
    return labels, end - start, len(candidate_pairs)


def k_experiment(args):
    for k in range(5, 15, 2):
        start = time()
        shingles = Shingling(k)
        compare_set = CompareSet()
        files = [f for f in listdir(args.data_dir)][: args.n_documents]
        hashed_sets = []
        for file in files:
            f = open(args.data_dir + file, "r")
            doc = f.read()
            hashed_shing = shingles.shingle_document(doc)
            hashed_sets.append(hashed_shing)
        sims = []
        for i in range(args.n_documents):
            for j in range(i + 1, args.n_documents):
                j_sim = compare_set.jaccard_similarity(hashed_sets[i], hashed_sets[j])
                sims.append(j_sim)
        end = time()
        print(
            f"{k}-shingles; mean similarity of {sum(sims)/len(sims)}; time: {end-start}"
        )


def n_experiment(args):
    for n in range(10, 101, 10):
        start = time()
        shingles = Shingling(args.k_shingle)
        minhash = MinHashing(n)
        compare_set = CompareSet()
        compare_sign = CompareSignatures()
        files = [f for f in listdir(args.data_dir)][: args.n_documents]
        hashed_sets = []
        sign_matrix = []

        for file in files:
            f = open(args.data_dir + file, "r")
            doc = f.read()
            hashed_shing = shingles.shingle_document(doc)
            hashed_sets.append(hashed_shing)
            col_doc = minhash.compute_signature(hashed_shing)
            sign_matrix.append(col_doc)

        error = []
        for i in range(args.n_documents):
            for j in range(i + 1, args.n_documents):
                j_sim = compare_set.jaccard_similarity(hashed_sets[i], hashed_sets[j])
                sign_sim = compare_sign.compare(sign_matrix[i], sign_matrix[j])
                error.append(abs(j_sim - sign_sim))
        end = time()
        print(
            f"{n} hash signatures; mean absolute difference between Jaccard similarity "
            f"and singature similarity: {sum(error)/len(error)}; time: {end-start}"
        )


def main():
    parser = argparse.ArgumentParser(description="INSERT DESCRIPTION.")
    parser.add_argument(
        "--k_shingle",
        type=int,
        default=9,
        help="size of the shingles (default: 9)",
    )
    parser.add_argument(
        "--hash_signatures",
        type=int,
        default=100,
        help="number of hash signatures (default: 100)",
    )
    parser.add_argument(
        "--n_documents",
        type=int,
        default=10,
        help="number of documents to compare from the given directory (default: 10)",
    )
    parser.add_argument(
        "--lsh_bands",
        type=int,
        default=20,
        help="number of bands used in LSH. Needs to be divisor of hash_signatures (default: 20)",
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        default="data/",
        help='input data directory (default: "data/")',
    )
    parser.add_argument(
        "--similarity_threshold",
        type=float,
        default=0.75,
        help="similarity threshold (default: 0.75)",
    )
    parser.add_argument(
        "--k_experiment", dest="k_experiment", default=False, action="store_true"
    )
    parser.add_argument(
        "--n_experiment", dest="n_experiment", default=False, action="store_true"
    )

    args = parser.parse_args()

    if args.k_experiment:
        k_experiment(args)
    elif args.n_experiment:
        n_experiment(args)
    else:
        gt, jaccard_time = jaccard_similarity(args)
        print(
            f"List of similar documents (>{args.similarity_threshold}) using Jaccard similarity:"
            f"\nPairs of documents analysed: {int(args.n_documents*(args.n_documents-1)/2)}"
            f"\n{gt}\ntime: {jaccard_time}\n"
        )
        sign_labels, signatures_time = signature_comparison(args)
        print(
            f"List of similar documents (>{args.similarity_threshold}) comparing signatures:"
            f"\nPairs of documents analysed: {int(args.n_documents*(args.n_documents-1)/2)}"
            f"\n{sign_labels}\ntime: {signatures_time}\n"
        )
        lsh_labels, lsh_time, analysed_pairs = lsh_comparison(args)
        print(
            f"List of similar documents (>{args.similarity_threshold}) applying LSH:"
            f"\nPairs of documents analysed: {analysed_pairs}"
            f"\n{lsh_labels}\ntime: {lsh_time}\n"
        )


if __name__ == "__main__":
    main()
