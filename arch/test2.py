"""V2: co-occurrence statistics + weighted prediction."""

from arch import test
from arch.config import SEP

cooccurrence_counts = {}


def sort_desc(dic):
    """Sort a {key: count} dict by count, descending."""
    return sorted(dic.items(), key=lambda d: d[1], reverse=True)


def count_cooccurrence(tokens: list) -> None:
    """Count how often two words appear in the same sentence."""
    sentence = []
    for word in tokens:
        if word != SEP:
            sentence.append(word)
        else:
            for cur_word in sentence:
                dic = cooccurrence_counts.setdefault(cur_word, {})
                for other in sentence:
                    if other != cur_word and other != SEP:
                        dic[other] = dic.get(other, 0) + 1
            sentence = []


def weighted_score(input_words, bigram_counts, cooccurrence_counts):
    """V2 score: 0.5 * adjacency + 0.25 * co-occurrence."""
    adj_bonus, cooc_bonus, candidates = {}, {}, {}
    for word in input_words:
        for cand, count in cooccurrence_counts.get(word, {}).items():
            cooc_bonus[cand] = cooc_bonus.get(cand, 0) + count
            candidates.setdefault(cand, 0)
        for cand, count in bigram_counts.get(word, {}).items():
            adj_bonus[cand] = adj_bonus.get(cand, 0) + count
            candidates.setdefault(cand, 0)
    for cand in candidates:
        candidates[cand] = adj_bonus.get(cand, 0) * 0.5 + cooc_bonus.get(cand, 0) * 0.25
    ranked = sort_desc(candidates)
    return ranked[:len(ranked) // 2]


def generate(words, ignore_words=''):
    """Predict a continuation from the given words and print it, until SEP."""
    lst = list(words)
    print(' '.join(lst), end='')
    while lst[-1] != SEP:
        ranked = weighted_score(lst, test.bigram_counts, cooccurrence_counts)
        while ranked[0][0] in ignore_words:
            ranked.pop(0)
        new_word = ranked[0][0]
        lst.append(new_word)
        print(' ' + new_word, end='')
    print()
    return lst
