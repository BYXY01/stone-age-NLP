import test
import test2

import config
repl = config.repl

word_dic_3 = dict()

def tongji3(cut_res:list): # 统计词和词之间的距离
    t_lst = []
    for word in cut_res:
        if word != repl:
            t_lst.append(word)
        else:
            # print(t_lst)
            for cur_wd in t_lst:
                dic = word_dic_3.get(cur_wd, {})
                for wd in t_lst:
                    if wd != cur_wd and wd != repl:
                        dic[wd]=dic.get(wd,[float('inf'),0])
                        d=abs(t_lst.index(wd)-t_lst.index(cur_wd))
                        if d < dic[wd][0]: dic[wd][0] = d
                        if d > dic[wd][1]: dic[wd][1] = d
                word_dic_3[cur_wd]=dic
            t_lst=[]

def minmax_norm(t_dic, a):   #归一化：将数值从其它区间比如[1,5878]变成[0,1]，保证权值按权重计算
    for i in range(1,a):
        vals=[v[i] for v in t_dic.values()]
        lo,hi=min(vals),max(vals)
        if lo==hi: continue
        for v in t_dic.values():
            v[i]=(v[i]-lo)/(hi-lo)

def jiaquan2(input_words:list, word_dic1:dict, word_dic2:dict, word_dic3:dict):
    points=[0,0.5,0.25,0.25]
    t_dic={}
    for iwd in input_words:
        for k,v in word_dic1.get(iwd,{}).items():
            t_dic.setdefault(k,[0,0,0,0])[1]+=v
        for k,v in word_dic2.get(iwd,{}).items():
            t_dic.setdefault(k,[0,0,0,0])[2]+=v
        for k,v in word_dic3.get(iwd,{}).items():
            t_dic.setdefault(k,[0,0,0,0])[3]+=1/v[0]
    minmax_norm(t_dic,3)
    for v in t_dic.values():
        v[0]=sum(v[i]*points[i] for i in range(1,4))
    res_lst=sorted(t_dic.items(),key=lambda d:d[1][0],reverse=True)
    return res_lst[:len(res_lst)//2]

def jiaquan_output_test2(words,ignor_words=''):
    lst=[]
    lst.extend(words)
    print(*words,sep='',end='')
    while lst[-1] != repl:
        jiaquan_res=jiaquan2(lst,test.word_dic,test2.word_dic_2,word_dic_3)
        while jiaquan_res[0][0] in ignor_words or jiaquan_res[0][0] in lst:
            jiaquan_res.pop(0)
        new_word=jiaquan_res[0][0]
        lst.append(new_word)
        print(new_word,end='')
    print()
    return lst

pass