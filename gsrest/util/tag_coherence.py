from difflib import SequenceMatcher
import time

def calcTagCoherence(tags = []):
    if(len(tags) == 1): return 1
    ratios = []
    for i in range(0, len(tags)):
        for j in range(0, len(tags)):
            if i == j: continue
            ratios.append(SequenceMatcher(None, tags[i]['label'], tags[j]['label']).ratio())
    if not ratios: return None
    return sum(ratios) / len(ratios)
