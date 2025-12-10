import random
from config import *

sort_WDlst=lambda word_dic,word: sorted(word_dic[word].items(), key=lambda d: d[1], reverse=True)

def predict_next(word_dic,word):
    while not word == repl:
        print(word,end='')
        word = sort_WDlst(word_dic,word)[0][0]
    print(word)

def predict_next_rand(word_dic,word):
    while not word == repl:
        print(word,end='')
        word=random.choices(list(word_dic[word].keys()),weights=list(word_dic[word].values()),k=1)[0]
    print(repl)

def predict_next_rand_r(word_dic,word,l=None):
    import time
    print(word, end='')
    while True:
        lst = sort_WDlst(word_dic,word)
        if type(l) is type(int()):
            lst=lst[:l]
        if type(l) is type(tuple()):
            lst=lst[:random.randint(*l)]
        if type(l) is type(list()):
            lst=lst[l[0]:l[1]]
        dic=dict(lst)
        new_word=random.choices(list(dic.keys()),weights=list(dic.values()),k=1)[0]
        if not new_word == repl:
            word = new_word
            print(word,end='')
        else:
            if len(word_dic[word])==1:
                print(word_dic[word])
                break
            else:
                print('-',end='')

def predict_by_recursion(word_dic,start,end,l):
    if start == end:
        return end
    if start == repl:
        return ''
    lst = sort_WDlst(word_dic,start)
    for i in lst[:l]:
        result=predict_by_recursion(word_dic,i[0],end,l)
        if result and result != repl:
            return start+result

def predict_by_loop(word_dic,start,end,l,BFS:bool=False):
    class W_node_lite():
        def __init__(self,data):
            self.data=data
            self.came_from=[]
            self.next=[]
    lst = [W_node_lite(start)]
    # visited = set()
    all_node=dict()
    while lst:
        cur_node = lst.pop(BFS-1)
        if cur_node not in all_node.keys():
            all_node[cur_node.data]=cur_node
        for wd,t in [*sort_WDlst(word_dic,cur_node.data)[:l]]:
            if wd not in all_node.keys():
                node = W_node_lite(wd)
                node.came_from.append(cur_node)
                # all_node[wd] = node
                if not (cur_node.data == end or wd == repl):
                    lst.append(node)
                    cur_node.next.append(node)
            else:
                node = all_node[wd]
                node.came_from.append(cur_node)
    return all_node

def get_path_from_PBL(all_node,start,end,i):
    res_lst = []
    if i > 0:
        cur_node = all_node[start]
        while True:
            # print(cur_node.data,end='')
            res_lst.append(cur_node.data)
            if cur_node == all_node[end]: return res_lst
            else: cur_node=cur_node.next[i-1]
    if i < 0:
        cur_node = all_node[end]
        while True:
            # print(cur_node.data, end='')
            res_lst.append(cur_node.data)
            if cur_node == all_node[start]:
                res_lst.reverse()
                return res_lst
            else:
                cur_node = cur_node.came_from[-i-1]

    pass
