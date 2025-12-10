import jieba
import re
import test_func
from config import *

all_in_lst=[vocab_headefine,{},{},set(),dict()]
all_tokens = all_in_lst[3]
word2idx = lambda: all_in_lst[2]
idx2word = lambda: all_in_lst[1]
word_dic=all_in_lst[4]


def fenci(words_str):
    # import jieba
    no_sign_WS = re.sub(r'\W', repl, words_str)
    no_sign_WS2 = re.sub(f'{repl}{repl}+', repl, no_sign_WS)
    cut_res = jieba.lcut(no_sign_WS2)
    # print(cut_res)
    return cut_res

def tongji(cut_res):
    for i in range(1,len(cut_res)):
        dic=word_dic.get(cut_res[i-1],{})
        dic[cut_res[i]]=(dic.get(cut_res[i],0)+1)
        word_dic[cut_res[i-1]]=dic
    # return word_dic

def update_vocab(new_words):
    # global word2idx,idx2word
    all_tokens.update(new_words)
    vocab = vocab_headefine + sorted(all_tokens)
    # print('ok1')
    # print(*enumerate(vocab))
    all_in_lst[1] = dict(enumerate(vocab))
    all_in_lst[2] = {w: i for i, w in idx2word().items()}


def load_from_file(filename):
    words=[]
    with open(filename,mode='r',encoding='gbk',errors='ignore') as file:
        context=file.read()
        words = fenci(context)
        tongji(words)
        update_vocab(words)
    # return words


# jieba.lcut(re.sub(r'\W','\r',context))
pass