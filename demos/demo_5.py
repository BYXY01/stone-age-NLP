"""
SPDX-License-Identifier: WTFPL

V2.5 demo: the online parrot — injects live web search results.
Runs in both modes: importnb on the notebooks, or the extracted classic/ packages.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for _ in range(6):
    if (ROOT / "extract_to_classic.py").exists() or (ROOT / ".git").is_dir():
        break
    ROOT = ROOT.parent

if (ROOT / "classic").is_dir():
    sys.path.insert(0, str(ROOT / "classic"))
    from core import test
    from core.test2 import count_cooccurrence
    from func.test2_5 import generate_with_reference
    from func import get_google_result2
else:
    from importnb import Notebook

    with Notebook():
        import core.core as core
        import features.func2 as features
    from features.get_google_result2 import GoogleSearcherChrome
    test = core
    count_cooccurrence = core.count_cooccurrence
    generate_with_reference = features.generate_with_reference

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

# Initialize the searcher
searcher = GoogleSearcherChrome(headless=True)

# Start testing: search the web, learn it, then answer
while input_str := input("Enter text: "):
    input_words = test.split_words(input_str)
    web_results = searcher.search(input_str)
    summaries = [res['summary'] for res in web_results]
    generate_with_reference(input_words, summaries, 'a an the of and to in is was were be been it its i I you he she her him his my your our their we they them us me am as at by for on with from that this not but or so then have has had do does did will would can could may')