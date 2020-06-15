from difflib import SequenceMatcher


def compute_tag_coherence(tags=None):
    labels = set()
    for tag in tags:
        labels.add(tag['label'])

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

    return sum(ratios) / len(ratios)
