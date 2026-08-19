"""V1 core: word splitting and base word statistics."""

import re

from arch.config import SEP, VOCAB_HEADS

bigram_counts = {}
all_tokens = set()
idx2word = {}
word2idx = {}


def split_words(text: str) -> list:
    """Split English text into words on whitespace.

    Sentence-ending punctuation (., !, ?, ;) is turned into the SEP token so
    that sentence boundaries are preserved in the statistics.
    """
    text = re.sub(r'[.!?;:]+', f' {SEP} ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.split()


def count_bigrams(tokens: list) -> None:
    """Count how often each word is immediately followed by another."""
    for i in range(1, len(tokens)):
        prev, nxt = tokens[i - 1], tokens[i]
        dic = bigram_counts.setdefault(prev, {})
        dic[nxt] = dic.get(nxt, 0) + 1


def update_vocab(new_words: list) -> None:
    """Extend the vocabulary with new tokens and rebuild the index maps."""
    all_tokens.update(new_words)
    vocab = VOCAB_HEADS + sorted(all_tokens)
    idx2word.clear()
    idx2word.update(dict(enumerate(vocab)))
    word2idx.clear()
    word2idx.update({w: i for i, w in idx2word.items()})


def load_from_file(filename: str) -> None:
    """Read a corpus file, split it into words and update statistics."""
    with open(filename, mode='r', encoding='utf-8', errors='ignore') as file:
        tokens = split_words(file.read())
    count_bigrams(tokens)
    update_vocab(tokens)
