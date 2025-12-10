import jieba
import re
import test

import config
repl = config.repl

word_dic_2 = dict()

dic_fast_sorted=lambda dic: sorted(dic.items(), key=lambda d: d[1], reverse=True)

def tongji2(cut_res:list): # 统计词和词之间在同一个句子出现的次数，将来可以算概率
    t_lst = []
    for word in cut_res:
        if word != repl:
            t_lst.append(word)
        else:
            # print(t_lst)
            for cur_wd in t_lst:
                dic = word_dic_2.get(cur_wd, {})
                for wd in t_lst:
                    if wd != cur_wd and wd != repl:
                        dic[wd]=dic.get(wd,0)+1
                word_dic_2[cur_wd]=dic
            t_lst=[]

def jiaquan1(input_words:list, word_dic1:dict, word_dic2:dict):
    points=[0,0.5,0.25]
    dic1_plus_res,dic2_plus_res={},{}
    res_dic={}
    for iwd in input_words:
        for k,v in word_dic2[iwd].items():
            dic2_plus_res[k]=dic2_plus_res.get(k,0)+v
            res_dic[k]=0
        for k,v in word_dic1[iwd].items():
            dic1_plus_res[k]=dic1_plus_res.get(k,0)+v
            res_dic[k]=0
    for k in res_dic.keys():
        res_dic[k] = (dic1_plus_res.get(k,0) * points[1]) + (dic2_plus_res.get(k,0) * points[2])
    res_lst = dic_fast_sorted(res_dic)
    return res_lst[:len(res_lst)//2]

def jiaquan_output_test1(words,ignor_words=''):
    lst=[]
    lst.extend(words)
    print(*words,sep='',end='')
    while lst[-1] != repl:
        jiaquan_res=jiaquan1(lst,test.word_dic,word_dic_2)
        while jiaquan_res[0][0] in ignor_words:
            jiaquan_res.pop(0)
        new_word=jiaquan_res[0][0]
        lst.append(new_word)
        print(new_word,end='')
    print()
    return lst

pass