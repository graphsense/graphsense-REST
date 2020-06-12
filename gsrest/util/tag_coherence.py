from difflib import SequenceMatcher


def calcTagCoherence(tags=None):

    if len(tags) == 1:
        return 1

    ratios = []
    for i, tag_i in enumerate(tags):
        for j, tag_j in enumerate(tags):
            if i == j:
                continue
            seq_match = SequenceMatcher(None, tag_i['label'], tag_j['label'])
            ratios.append(seq_match.ratio())

    if not ratios:
        return None
    return sum(ratios) / len(ratios)
