from nltk.corpus import wordnet as wn
import queue


def filter(comparison_object, candidates):
    hypernyms_comparison_object = get_all_hypernyms(comparison_object)
    filtered_candidates = []
    for candidate in candidates:
        candidate_hypernyms = get_all_hypernyms(candidate[0])
        if not set(hypernyms_comparison_object).isdisjoint(candidate_hypernyms):
            filtered_candidates.append(candidate)

    return [c[0] for c in filtered_candidates]


def get_all_hypernyms(comparison_object):
    q = queue.Queue()

    for ss in wn.synsets(comparison_object):
        for hypernym in ss.hypernyms():
            q.put(hypernym)

    hypernyms = []
    while not q.empty():
        hypernym = q.get()
        hypernyms.append(hypernym)
        for hypernym in hypernym.hypernyms():
            q.put(hypernym)

    return hypernyms