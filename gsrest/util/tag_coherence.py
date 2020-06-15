from difflib import SequenceMatcher


def compute_tag_coherence(tags=None):
    if not tags:
        return None

    labels = set()
    labelCount = dict()
    for tag in tags:
        label = tag['label']
        labels.add(label)
        if label not in labelCount:
            labelCount[label] = 0
        labelCount[label] += 1

    if len(labels) == 1:
        return 1

    ratios = []
    for i, label_i in enumerate(labels):
        for j, label_j in enumerate(labels):
            if i == j:
                continue
            seq_match = SequenceMatcher(None, label_i, label_j)
            ratios.append(seq_match.ratio())

    if not ratios:
        return None

    e = 0
    for c in labelCount.values():
        e += c * c - c

    return (e + sum(ratios)) / (e + len(ratios))
