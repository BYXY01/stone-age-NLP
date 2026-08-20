# 🪨 Stone Age NLP

[![python](https://img.shields.io/badge/python-3.10-blue)]()
[![Status](https://img.shields.io/badge/status-experimental-orange)]()
[![Version](https://img.shields.io/badge/version-4-blue)]()

> **A thought experiment born out of a late-night curiosity in 2024, that grew into a retro statistical language model**

---

## 📖 What is this?

This project is a **minimal, purely statistical NLP experiment**. No PyTorch, no Transformer, no deep learning framework of any kind — just **plain whitespace word splitting** + Python dictionaries + simple probability math, trying to answer one question:

> **"How far can we push language prediction and generation using pure statistics, without large models?"**

The answer: not very far, but surprisingly it produced an **"electronic parrot"**.

### 🧠 Design philosophy: lightweight probabilism

No hard-coded rules (symbolism), no opaque black boxes (deep learning). Just the lightest statistics carrying the most dynamic probabilities.

- No rules are defined; we only **count**.
- "Pairwise co-occurrence" statistics are the Stone Age cousin of the Attention mechanism.

---

## 🧬 Evolution timeline

| Time | Version | Event | Codename |
|------|----------|------|------|
| 2024, some late night | — | Inspired by a popular-science video, wrote a character-level prototype | 🔥 Spark |
| 2025.11.19 | **V1** | Introduced word splitting, upgraded from characters to words | The chaotic word picker |
| 2025.11.20 | **V2** | Pairwise co-occurrence + mixed weights `0.5×adjacency + 0.25×co-occurrence` | The sage with connections |
| 2025.12.03 | **V2.1** | Real-time memory — accidentally creating the **electronic parrot** | 🦜 **Electronic parrot** |
| 2025.12.09 | **V2.5** | Google search injection | The parrot that looks things up |
| 2025.12.03 | — | Discussed the "electronic parrot" phenomenon with classmates | — |
| 2025.12.08 | — | DeepMind released Evo-Memory; the core idea matched by coincidence | — |
| 2026.07 | — | Archived and organized, repository created | — |
| 2026.07.29 | **V3** | Word distance weights (1 / minimum distance) | The mathematical actuary |
| 2026.08.19 | **V4** | Graph-structure dictionary tree (nodes + cache + customizable builder) | The architect of language |

> Version numbers are a little wordplay: `2.1` = architecture 2 + **one** — a **one-track mind** (memory); `2.5` = architecture 2 + **five** ≈ **hive** — a **hive mind** (the web's collective knowledge).

---

## 🦜 V2.1 "An electronic parrot from the Stone Age"

Originally just a small "live-update statistics" feature, it unexpectedly produced an emergent phenomenon:

> Tell it "hello world" many times, then say "hello" — it answers "hello world" instead of "how are you".

It isn't learning; it is **rewriting its own statistical weights in real time**. You teach it, it remembers. **It is dumb, but it remembers.**

## ⚙️ How does it work?

**Statistics phase**: load a long text corpus → `split_words` (whitespace splitting) → build three dictionaries:

- `bigram_counts`: **adjacency** statistics between words (who usually follows whom)
- `cooccurrence_counts`: **same-sentence co-occurrence** statistics (who is close to whom)
- `distance_stats`: **distance** statistics (how far apart, stored as `[min distance, max distance]`)

**V2 prediction**: `Score(w) = 0.5 × adjacency + 0.25 × co-occurrence`

**V3 prediction**: `Score(w) = 0.5 × adjacency + 0.25 × co-occurrence + 0.25 × (1 / min distance)`

**V4 refactor**: switched to a graph-structure dictionary tree (`WordNode` + `_links` adjacency list), with three cache levels (0 no cache / 1 lazy load / 2 full cache), undirected B / directed X modes, and pluggable builders to customize output formats.

**Memory version (V2.1)**: statistics are updated in real time on every conversation. Whatever you say, it remembers.

**Web version (V2.5)**: Chrome/Selenium fetches Google search results → injects them into the statistics → learns on the spot.

---

## 🔬 Experiment: letting an LLM raise a parrot

Feed the parrot a page of text, then hand the conversation over to an LLM. The parrot replies with the most likely next word, so the LLM quickly finds itself talking to something that only echoes back whatever it was just told. The result is less a dialogue and more a funhouse mirror: **the parrot can be used as a toy for probing how much an LLM adapts its style to a weaker, dumber interlocutor.**

---

## 🤔 What can it do?

| ❌ Cannot | ❤️ Can |
|--------|--------|
| Actually understand anything | ✅ Let you see what "word co-occurrence statistics" looks like |
| Reason | ✅ Let you experience how "instant memory" changes model behavior |
| Generate fluent long-form text | ✅ Help you understand why LLMs need deep learning and attention |

---

## 📚 Getting the corpus

The demos load plain-text novels from the `data/` directory (git-ignored, so it stays out of the repo for copyright hygiene). Download any public-domain text and drop it in `data/`:

| Book | Download (Project Gutenberg) | Suggested filename |
|------|------------------------------|--------------------|
| A Tale of Two Cities | [pg98.txt](https://www.gutenberg.org/cache/epub/98/pg98.txt) | `data/a_tale_of_two_cities.txt` |
| Jane Eyre | [pg1260.txt](https://www.gutenberg.org/cache/epub/1260/pg1260.txt) | `data/jane_eyre.txt` |
| Romeo and Juliet | [pg1513.txt](https://www.gutenberg.org/cache/epub/1513/pg1513.txt) | `data/romeo_and_juliet.txt` |

Other good long-form candidates: *Pride and Prejudice* ([pg1342](https://www.gutenberg.org/cache/epub/1342/pg1342.txt)), *The Adventures of Sherlock Holmes* ([pg1661](https://www.gutenberg.org/cache/epub/1661/pg1661.txt)), *Moby Dick* ([pg2701](https://www.gutenberg.org/cache/epub/2701/pg2701.txt)), *Alice's Adventures in Wonderland* ([pg11](https://www.gutenberg.org/cache/epub/11/pg11.txt)).

You can also point the demos at any other `.txt` by editing `CORPUS_FILES` in `demos/*.py`.

---

## 📁 Project structure

The core algorithms and feature extensions are written as **literate notebooks** (`.ipynb`, runnable directly via `importnb`). `extract_to_classic.py` splits them back into plain `.py` packages under `classic/` (git-ignored).

```
stone_age_NLP/
├── core/                           # Core algorithms → core/core.ipynb (CC-BY-4.0)
│   ├── core.ipynb                  # @config @test @test_func @test2 @test3 @test4
│   └── __init__.py                 # package marker (import core.core)
├── features/                       # Extra features → features/func2.ipynb (MIT)
│   ├── func2.ipynb                 # @test2_1 @test2_5 (V2.1 / V2.5)
│   ├── get_google_result.py        # Scraper (requests version)
│   ├── get_google_result2.py       # Scraper (Selenium Chrome version)
│   └── __init__.py                 # package marker (import features.func2)
├── demos/                          # Demonstrations (WTFPL)
│   ├── demo.py                     # V2 demo
│   ├── demo_1.py                   # Electronic parrot demo
│   └── demo_5.py                   # Web version demo
├── extract_to_classic.py           # Split notebooks into classic/ .py packages
├── README.md                       # This file
└── LICENSE
```

`classic/` is generated by `extract_to_classic.py` (git-ignored):

```
classic/
├── core/                           # from core/core.ipynb (CC-BY-4.0)
│   ├── config.py                   # @config
│   ├── test.py                     # @test (V1)
│   ├── test_func.py                # @test_func
│   ├── test2.py                    # @test2 (V2)
│   ├── test3.py                    # @test3 (V3)
│   └── test4.py                    # @test4 (V4)
├── func/                           # from features/func2.ipynb (MIT)
│   ├── test2_1.py                  # @test2_1 (V2.1)
│   ├── test2_5.py                  # @test2_5 (V2.5)
│   ├── get_google_result.py        # copied
│   └── get_google_result2.py       # copied
└── demo/                           # copied from demos/ (WTFPL)
    ├── demo.py
    ├── demo_1.py
    └── demo_5.py
```

Run the demos either way — they auto-detect `classic/` (extracted mode) or fall back to `importnb` on the notebooks (standard mode).

---

## 🎭 Amazing coincidences and easter eggs

On 2025.12.03 we were still discussing this "electronic parrot". 5 days later (12.08), DeepMind released **Evo-Memory**, whose core idea is also: **"context is weights; memory is not storage, but compression."**

The planned V4.6/V4.7 of this project accidentally collided with the version numbers of Zhipu AI's GLM-4.6/4.7. One is a general model with hundreds of billions of parameters; the other is an electronic parrot with a few thousand word nodes.

---

## 🙏 Acknowledgements

- **差评君 (Chaping)** — the GPT-principle explainer video that opened Pandora's box
- **jieba** — helped the model evolve from "characters" to "words" (later replaced by plain whitespace word splitting)
- **DeepSeek** — patiently chatted with the parrot while it echoed back
- **That sleepless night** — where all the crazy ideas were born

---

*"Master, 'the' and 'best' are the closest here, so this is what I say."*

**Welcome to the Stone Age.** 🪨🦜

---

## 📜 Licensing

This repository uses a layered licensing model (SPDX identifiers are embedded in each file):

| Scope | License | Notes |
|-------|---------|-------|
| Root (`LICENSE`) | **Unlicense** | Project-wide default license |
| Core architecture (`core/`) | **CC BY 4.0** | Core ideas — attribute when used |
| Feature extensions (`features/`) | **MIT** | Permissive, easy to reuse |
| Demo scripts (`demos/`) | **WTFPL** | Do whatever you want |

You are free to use, modify and learn from any part of this project. Enjoy the Stone Age.

