"""V2 demo: weighted prediction on public-domain English novels (Project Gutenberg)."""

from arch import test
from arch.test2 import count_cooccurrence, generate
from arch.test_func import get_path, predict_by_loop, predict_next, predict_next_rand

CORPUS_FILES = [
    'data/a_tale_of_two_cities.txt',
    'data/jane_eyre.txt',
    'data/romeo_and_juliet.txt',
]

# Load data
for filename in CORPUS_FILES:
    test.load_from_file(filename)
    with open(filename, mode='r', encoding='utf-8', errors='ignore') as file:
        tokens = test.split_words(file.read())
    count_cooccurrence(tokens)

IGNORE_WORDS = 'a an the of and to in is was were be been it its i I you he she her him his my your our their we they them us me am as at by for on with from that this not but or so then have has had do does did will would can could may'

# Start testing
predict_next(test.bigram_counts, input("Enter a word: "))
predict_next_rand(test.bigram_counts, input("Enter a word: "))

start, end = input("Start word: "), input("End word: ")
all_nodes = predict_by_loop(test.bigram_counts, start, end, 500)
get_path(all_nodes, start, end, -1)

_ = generate(test.split_words(input("Enter text: ")), IGNORE_WORDS)
