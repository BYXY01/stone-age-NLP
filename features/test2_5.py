"""V2.5: web — inject external search results into the statistics."""

import re

from arch import test
from arch.config import SEP
from arch.test2 import cooccurrence_counts, count_cooccurrence, weighted_score


def generate_no_repeat(words, ignore_words=''):
    """Like ``generate``, but never repeats a word already generated."""
    lst = list(words)
    print(' '.join(lst), end='')
    while lst[-1] != SEP:
        ranked = weighted_score(lst, test.bigram_counts, cooccurrence_counts)
        while ranked[0][0] in ignore_words or ranked[0][0] in lst:
            ranked.pop(0)
        new_word = ranked[0][0]
        lst.append(new_word)
        print(' ' + new_word, end='')
    print()
    return lst


def generate_with_reference(words, ref_data, ignore_words=''):
    """Predict using extra reference data (e.g. web search results)."""

    def process_reference():
        if type(ref_data) is type(list()):
            return test.split_words(' '.join(re.sub(r'\W', ' ', item) for item in ref_data))
        if type(ref_data) is type(str()):
            return test.split_words(ref_data)
        return []

    processed = process_reference()
    test.count_bigrams(processed)
    count_cooccurrence(processed)
    try:
        generate_no_repeat(words, ignore_words)
    except Exception:
        generate_no_repeat(words + [SEP], ignore_words)
