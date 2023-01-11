from collections import Counter
from difflib import SequenceMatcher


def compute_tag_coherence(labels=None):
    if not labels:
        return None

    label_set = set()
    label_count = Counter()
    for label in labels:
        label_set.add(label)
        label_count[label] += 1

    if len(label_set) == 1:
        return 1

    ratios = []
    for i, label_i in enumerate(label_set):
        for j, label_j in enumerate(label_set):
            if i == j:
                continue
            seq_match = SequenceMatcher(None, label_i, label_j)
            ratios.append(seq_match.ratio())

    if not ratios:
        return None

    e = 0
    for count in label_count.values():
        e += count**2 - count

    return (e + sum(ratios)) / (e + len(ratios))
