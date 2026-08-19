"""Prediction utilities built on the adjacency dictionary (incl. BFS/DFS graph search)."""

import random

from arch.config import SEP


def sort_by_weight(word_dict, word):
    """Sort the neighbours of a word by their counts, descending."""
    return sorted(word_dict[word].items(), key=lambda d: d[1], reverse=True)


def predict_next(word_dict, word):
    """Greedy prediction: always pick the most likely next word until SEP."""
    print(word, end='')
    while word != SEP:
        word = sort_by_weight(word_dict, word)[0][0]
        print(' ' + word, end='')
    print()


def predict_next_rand(word_dict, word):
    """Random prediction sampled from the weighted distribution until SEP."""
    print(word, end='')
    while word != SEP:
        choices = list(word_dict[word].keys())
        weights = list(word_dict[word].values())
        word = random.choices(choices, weights=weights, k=1)[0]
        print(' ' + word, end='')
    print()


def predict_next_rand_r(word_dict, word, limit=None):
    """Random prediction with a limit on the candidate window.

    ``limit`` can be an int (keep top-N), a (min, max) tuple (random slice),
    or a [start, stop] list (explicit slice).
    """
    print(word, end='')
    while True:
        lst = sort_by_weight(word_dict, word)
        if type(limit) is type(int()):
            lst = lst[:limit]
        if type(limit) is type(tuple()):
            lst = lst[:random.randint(*limit)]
        if type(limit) is type(list()):
            lst = lst[limit[0]:limit[1]]
        dic = dict(lst)
        new_word = random.choices(list(dic.keys()), weights=list(dic.values()), k=1)[0]
        if not new_word == SEP:
            word = new_word
            print(' ' + word, end='')
        else:
            if len(word_dict[word]) == 1:
                print(word_dict[word])
                break
            else:
                print('-', end='')


def predict_by_recursion(word_dict, start, end, limit):
    """Find a path from ``start`` to ``end`` via recursive DFS over the top-N candidates."""
    if start == end:
        return end
    if start == SEP:
        return ''
    for candidate, _ in sort_by_weight(word_dict, start)[:limit]:
        result = predict_by_recursion(word_dict, candidate, end, limit)
        if result and result != SEP:
            return start + result


def predict_by_loop(word_dict, start, end, limit, bfs: bool = False):
    """Expand a graph of nodes from ``start`` to ``end`` (BFS or DFS).

    Returns ``all_nodes``, a dict of word -> WNode used by ``get_path``.
    """
    class WNode:
        def __init__(self, data):
            self.data = data
            self.came_from = []
            self.next = []

    lst = [WNode(start)]
    all_nodes = dict()
    while lst:
        # BFS pops from the front, DFS pops from the back.
        cur_node = lst.pop(bfs - 1)
        if cur_node.data not in all_nodes:
            all_nodes[cur_node.data] = cur_node
        for wd, _count in sort_by_weight(word_dict, cur_node.data)[:limit]:
            if wd not in all_nodes:
                node = WNode(wd)
                node.came_from.append(cur_node)
                if not (cur_node.data == end or wd == SEP):
                    lst.append(node)
                    cur_node.next.append(node)
            else:
                node = all_nodes[wd]
                node.came_from.append(cur_node)
    return all_nodes


def get_path(all_nodes, start, end, direction):
    """Reconstruct a path from the graph built by ``predict_by_loop``.

    ``direction > 0`` walks forward through ``next``; ``direction < 0`` walks
    backward through ``came_from``.
    """
    path = []
    if direction > 0:
        cur_node = all_nodes[start]
        while True:
            path.append(cur_node.data)
            if cur_node == all_nodes[end]:
                return path
            cur_node = cur_node.next[direction - 1]
    if direction < 0:
        cur_node = all_nodes[end]
        while True:
            path.append(cur_node.data)
            if cur_node == all_nodes[start]:
                path.reverse()
                return path
            cur_node = cur_node.came_from[-direction - 1]
