class WdConfig:
    def __init__(self,
                 fast_mode=1,                 # 缓存方式 0, 1, 2
                 mode='X',                    # 模式，B or X (mB(memBer,neighBors) or mX(miX,eXtend))，即无向平等或有向混合
                 builder=None,                # 函数 dic -> any，dic为_links格式
                 weight_aggregator=None):     # 函数 weights_lst -> number
        """
        :param mode: 图模式，'B' 无向（双向），'X' 有向（默认）
        """
        self.fast_mode = fast_mode
        self.mode = mode
        self.builder = builder or self.origin_dic_build
        self.weight_aggregator = weight_aggregator or (lambda lst: sum(lst))

    word_s_build = lambda self,dic: {k.word for k in dic}                     # {词} 集合
    origin_dic_build = lambda self,dic: dic                                   # 原始格式：{node: 边信息}，不转换
    list_weight_builder = lambda self,dic: [(k, self.weight_aggregator(v['weights_lst'])) for k, v in dic.items()]  # [(节点, 聚合权重)]
    dict_weight_builder = lambda self,dic: {k.word: self.weight_aggregator(v['weights_lst']) for k, v in dic.items()}  # {词: 聚合权重}
    list_full_builder = lambda self,dic: [(k.word, v['weights_lst'], v.get('other', {}), v.get('direct', '')) for k, v in dic.items()]  # [(词, 权重列表, 其他, 方向)]
    dict_full_builder = lambda self,dic: {k.word: {
        'weights': v['weights_lst'],
        'other': v.get('other', {}),
        'direct': v.get('direct', '')
    } for k, v in dic.items()}                        # {词: {权重, 其他, 方向}}

    # ---------- 预设配置模板（供用户选用） ----------
    @classmethod
    def words(cls, fast_mode=2, mode='X'):
        """返回 {词} 集合"""
        cfg = cls(fast_mode=fast_mode, mode=mode)
        cfg.builder = cfg.word_s_build
        return cfg

    @classmethod
    def default(cls, fast_mode=1, mode='X', agg=None):
        """返回 [(节点, 聚合权重), ...] 列表"""
        cfg = cls(fast_mode=fast_mode, mode=mode, weight_aggregator=agg)
        cfg.builder = cfg.list_weight_builder
        return cfg

    @classmethod
    def dict_full(cls, fast_mode=0, mode='X'):
        """返回 {词: {"weights": [...], "other": {...}, "direct": "..."}}"""
        cfg = cls(fast_mode=fast_mode, mode=mode)
        cfg.builder = cfg.dict_full_builder
        return cfg

DEFAULT_CONFIG = WdConfig.default()

class Wd_Node:
    def __init__(self, word, config=None):
        self.word = word
        self.config = config or DEFAULT_CONFIG

        # 唯一真相源：邻居节点 -> 边信息
        self._links = {}  # {node_obj: {"weights_lst": [], "other": {}, "direct": ""}}

        if int(self.config.fast_mode)>0:
            self.parents_lst = None
            self.children_lst = None

    def _get_links(self,direct=''):
        if direct=='': direct='pc'
        t_dic={}
        for k,v in self._links.items():
            d=v.get('direct','')
            if self.config.mode=='B' or d in direct:
                t_dic[k]=v
        return self.config.builder(t_dic)

    def get_links(self,direct=''):
        if direct=='': direct='pc'
        fm=int(self.config.fast_mode)
        if fm == 0: return self._get_links(direct)
        if fm > 0:
            if (direct in ('p','pc','') and self.parents_lst is None) or (self.config.mode=='B' or direct in ('c','pc','') and self.children_lst is None):
                self.update_cache()
            if self.config.mode=='B' or direct=='c':
                return self.children_lst
            elif direct=='p':
                return self.parents_lst
            elif direct=='pc':
                return self._merge(self.parents_lst,self.children_lst)

    def add_links(self, node, weights_lst, direct='c'):
        edge = self._links.setdefault(node, {'weights_lst': [], 'other': {}, 'direct': ''})
        edge['weights_lst']=weights_lst
        if self.config.mode!='B':
            edge['direct'] = self._merge_direct(edge['direct'], direct)
        if self.config.fast_mode==2 or self.parents_lst is not None or self.children_lst is not None:
            self.update_cache()
        return edge

    def update_links(self, node, weights_lst=None, direct=None, other=None):
        edge = self._links.get(node)
        if edge is None:
            return None
        if weights_lst:
            edge['weights_lst']=weights_lst
        if direct:
            edge['direct'] = self._merge_direct(edge['direct'], direct)
        if other:
            edge['other'].update(other)
        if self.parents_lst is not None or self.children_lst is not None:
            self.update_cache()
        return edge

    def update_cache(self):
        if int(self.config.fast_mode)==0: return
        if self.config.mode=='B':
            self.children_lst = self._get_links('c')
        else:
            self.parents_lst = self._get_links('p')
            self.children_lst = self._get_links('c')

    def _merge(self,a,b):
        if isinstance(a,set): return a|b
        if isinstance(a,dict): return {**a,**b}
        if isinstance(a,list): return a+b
        return (a,b)

    @staticmethod
    def _merge_direct(d0,d1):
        if not d0: return d1
        if not d1: return d0
        return d0 if d0==d1 else 'pc'


import config
repl = config.repl

word_index_dic = dict()

from itertools import pairwise

def build_dic_tree_sample(cut_res, config=None):
    tmp = {}
    for prev, nxt in pairwise(cut_res):
        if repl not in (prev, nxt):
            tmp.setdefault(prev, {})
            tmp[prev][nxt] = tmp[prev].get(nxt, 0) + 1
    for w, children in tmp.items():
        node = word_index_dic.setdefault(w, Wd_Node(w, config))
        for cw, cnt in children.items():
            cnode = word_index_dic.setdefault(cw, Wd_Node(cw, config))
            node.add_links(cnode, [cnt], direct='c')