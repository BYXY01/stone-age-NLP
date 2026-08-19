"""V2.1 demo: the electronic parrot — interactive, learns from every utterance."""

from arch import test
from arch.test2 import count_cooccurrence
from features.test2_1 import generate_with_memory

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

# Start testing: the parrot learns whatever you tell it
while input_words := test.split_words(input("Enter text: ")):
    generate_with_memory(input_words, 'a an the of and to in is was were be been it its i I you he she her him his my your our their we they them us me am as at by for on with from that this not but or so then have has had do does did will would can could may')
