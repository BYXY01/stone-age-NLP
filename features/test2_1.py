"""V2.1: memory — every user utterance updates the statistics on the fly."""

from arch import test
from arch.test2 import count_cooccurrence, generate


def generate_with_memory(words, ignore_words=''):
    """Predict after feeding the current utterance into the statistics (learns as it goes)."""
    test.count_bigrams(words)
    count_cooccurrence(words)
    generate(words, ignore_words)
