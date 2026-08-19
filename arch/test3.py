"""V3: distance-weighted prediction."""

from arch import test
from arch import test2
from arch.config import SEP

distance_stats = {}


def count_distances(tokens: list) -> None:
    """Record the min/max in-sentence distance between each pair of words."""
    sentence = []
    for word in tokens:
        if word != SEP:
            sentence.append(word)
        else:
            for cur_word in sentence:
                dic = distance_stats.setdefault(cur_word, {})
                for other in sentence:
                    if other != cur_word and other != SEP:
                        dic.setdefault(other, [float('inf'), 0])
                        dist = abs(sentence.index(other) - sentence.index(cur_word))
                        if dist < dic[other][0]:
                            dic[other][0] = dist
                        if dist > dic[other][1]:
                            dic[other][1] = dist
            sentence = []


def minmax_normalize(stats, depth) -> None:
    """Normalize each dimension to [0, 1] across all candidates."""
    for i in range(1, depth):
        values = [v[i] for v in stats.values()]
        lo, hi = min(values), max(values)
        if lo == hi:
            continue
        for v in stats.values():
            v[i] = (v[i] - lo) / (hi - lo)


def weighted_score_v3(input_words, bigram_counts, cooccurrence_counts, distance_stats):
    """V3 score: 0.5*adjacency + 0.25*co-occurrence + 0.25*(1/min distance)."""
    points = [0, 0.5, 0.25, 0.25]
    scores = {}
    for word in input_words:
        for cand, count in bigram_counts.get(word, {}).items():
            scores.setdefault(cand, [0, 0, 0, 0])[1] += count
        for cand, count in cooccurrence_counts.get(word, {}).items():
            scores.setdefault(cand, [0, 0, 0, 0])[2] += count
        for cand, dist in distance_stats.get(word, {}).items():
            scores.setdefault(cand, [0, 0, 0, 0])[3] += 1 / dist[0]
    minmax_normalize(scores, 3)
    for v in scores.values():
        v[0] = sum(v[i] * points[i] for i in range(1, 4))
    ranked = sorted(scores.items(), key=lambda d: d[1][0], reverse=True)
    return ranked[:len(ranked) // 2]


def generate_v3(words, ignore_words=''):
    """Predict a continuation using V3 distance weights, avoiding repeats."""
    lst = list(words)
    print(' '.join(lst), end='')
    while lst[-1] != SEP:
        ranked = weighted_score_v3(lst, test.bigram_counts, test2.cooccurrence_counts, distance_stats)
        while ranked[0][0] in ignore_words or ranked[0][0] in lst:
            ranked.pop(0)
        new_word = ranked[0][0]
        lst.append(new_word)
        print(' ' + new_word, end='')
    print()
    return lst
