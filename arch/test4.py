"""V4: graph structure dictionary tree (nodes + caches + custom builders)."""

from arch.config import SEP


class WordConfig:
    """Configuration controlling the graph behaviour of ``WordNode``."""

    def __init__(self,
                 fast_mode=1,             # cache mode: 0 none, 1 lazy, 2 full
                 mode='X',                # 'B' undirected (bidirectional), 'X' directed (mixed)
                 builder=None,            # function dict -> any, dict in _links format
                 weight_aggregator=None): # function weights_lst -> number
        """
        :param mode: graph mode, 'B' undirected (bidirectional), 'X' directed (default).
        """
        self.fast_mode = fast_mode
        self.mode = mode
        self.builder = builder or self.build_origin_dict
        self.weight_aggregator = weight_aggregator or (lambda lst: sum(lst))

    # -------- preset builders --------
    def build_word_set(self, dic):
        """Return the set of neighbour words."""
        return {k.word for k in dic}

    def build_origin_dict(self, dic):
        """Return the raw format {node: edge info} without conversion."""
        return dic

    def build_list_weight(self, dic):
        """Return [(node, aggregated weight), ...]."""
        return [(k, self.weight_aggregator(v['weights_lst'])) for k, v in dic.items()]

    def build_dict_weight(self, dic):
        """Return {word: aggregated weight}."""
        return {k.word: self.weight_aggregator(v['weights_lst']) for k, v in dic.items()}

    def build_list_full(self, dic):
        """Return [(word, weights_list, other, direction), ...]."""
        return [(k.word, v['weights_lst'], v.get('other', {}), v.get('direct', '')) for k, v in dic.items()]

    def build_dict_full(self, dic):
        """Return {word: {'weights': [...], 'other': {...}, 'direct': '...'}}."""
        return {k.word: {
            'weights': v['weights_lst'],
            'other': v.get('other', {}),
            'direct': v.get('direct', '')
        } for k, v in dic.items()}

    # -------- preset templates for end users --------
    @classmethod
    def words(cls, fast_mode=2, mode='X'):
        """Config that builds a set of words."""
        cfg = cls(fast_mode=fast_mode, mode=mode)
        cfg.builder = cfg.build_word_set
        return cfg

    @classmethod
    def default(cls, fast_mode=1, mode='X', agg=None):
        """Config that builds a [(node, aggregated weight), ...] list."""
        cfg = cls(fast_mode=fast_mode, mode=mode, weight_aggregator=agg)
        cfg.builder = cfg.build_list_weight
        return cfg

    @classmethod
    def dict_full(cls, fast_mode=0, mode='X'):
        """Config that builds {word: {"weights": [...], "other": {...}, "direct": "..."}}."""
        cfg = cls(fast_mode=fast_mode, mode=mode)
        cfg.builder = cfg.build_dict_full
        return cfg


DEFAULT_CONFIG = WordConfig.default()


class WordNode:
    def __init__(self, word, config=None):
        self.word = word
        self.config = config or DEFAULT_CONFIG

        # Single source of truth: neighbour node -> edge info
        self._links = {}  # {node_obj: {"weights_lst": [], "other": {}, "direct": ""}}

        if int(self.config.fast_mode) > 0:
            self.parents_lst = None
            self.children_lst = None

    def _get_links(self, direct=''):
        if direct == '':
            direct = 'pc'
        selected = {}
        for k, v in self._links.items():
            d = v.get('direct', '')
            if self.config.mode == 'B' or d in direct:
                selected[k] = v
        return self.config.builder(selected)

    def get_links(self, direct=''):
        if direct == '':
            direct = 'pc'
        fast_mode = int(self.config.fast_mode)
        if fast_mode == 0:
            return self._get_links(direct)
        if fast_mode > 0:
            if (direct in ('p', 'pc') and self.parents_lst is None) or \
               (self.config.mode == 'B' or direct in ('c', 'pc') and self.children_lst is None):
                self.update_cache()
            if self.config.mode == 'B' or direct == 'c':
                return self.children_lst
            if direct == 'p':
                return self.parents_lst
            if direct == 'pc':
                return self._merge(self.parents_lst, self.children_lst)

    def add_links(self, node, weights_lst, direct='c'):
        edge = self._links.setdefault(node, {'weights_lst': [], 'other': {}, 'direct': ''})
        edge['weights_lst'] = weights_lst
        if self.config.mode != 'B':
            edge['direct'] = self._merge_direct(edge['direct'], direct)
        if self.config.fast_mode == 2 or self.parents_lst is not None or self.children_lst is not None:
            self.update_cache()
        return edge

    def update_links(self, node, weights_lst=None, direct=None, other=None):
        edge = self._links.get(node)
        if edge is None:
            return None
        if weights_lst:
            edge['weights_lst'] = weights_lst
        if direct:
            edge['direct'] = self._merge_direct(edge['direct'], direct)
        if other:
            edge['other'].update(other)
        if self.parents_lst is not None or self.children_lst is not None:
            self.update_cache()
        return edge

    def update_cache(self):
        if int(self.config.fast_mode) == 0:
            return
        if self.config.mode == 'B':
            self.children_lst = self._get_links('c')
        else:
            self.parents_lst = self._get_links('p')
            self.children_lst = self._get_links('c')

    def _merge(self, a, b):
        if isinstance(a, set):
            return a | b
        if isinstance(a, dict):
            return {**a, **b}
        if isinstance(a, list):
            return a + b
        return (a, b)

    @staticmethod
    def _merge_direct(d0, d1):
        if not d0:
            return d1
        if not d1:
            return d0
        return d0 if d0 == d1 else 'pc'


from itertools import pairwise

word_index_dic = dict()


def build_dictionary_tree_sample(cut_res, config=None):
    """Build a sample dictionary tree from adjacent token pairs."""
    tmp = {}
    for prev, nxt in pairwise(cut_res):
        if SEP not in (prev, nxt):
            tmp.setdefault(prev, {})
            tmp[prev][nxt] = tmp[prev].get(nxt, 0) + 1
    for word, children in tmp.items():
        node = word_index_dic.setdefault(word, WordNode(word, config))
        for child_word, count in children.items():
            child_node = word_index_dic.setdefault(child_word, WordNode(child_word, config))
            node.add_links(child_node, [count], direct='c')
