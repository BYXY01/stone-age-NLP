import test2
import test

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
                        dic[wd]=dic.get(wd,[1,0])
                        d=abs(t_lst.index(wd)-t_lst.index(cur_wd))
                        dic[wd][0] = (d if d < dic[wd][0] else dic[wd][0])
                        dic[wd][1] = (d if d > dic[wd][1] else dic[wd][1])
                word_dic_3[cur_wd]=dic
            t_lst=[]

def jiaquan2(input_words:list, word_dic1:dict, word_dic2:dict, word_dic3:dict):
    points=[0,0.5,0.25,0.25]
    dic1_plus_res,dic2_plus_res,dic3_plus_res={},{},{}
    res_dic={}
    for iwd in input_words:
        for k,v in word_dic1.get(iwd,{}).items():
            dic1_plus_res[k]=dic1_plus_res.get(k,0)+v
            res_dic[k]=0
        for k,v in word_dic2.get(iwd,{}).items():
            dic2_plus_res[k]=dic2_plus_res.get(k,0)+v
            res_dic[k]=0
        for k,v in word_dic3.get(iwd,{}).items():
            dic3_plus_res[k]=dic3_plus_res.get(k,0)+(1/v[0])
            res_dic[k]=0
    for k in res_dic.keys():
        res_dic[k] = (dic1_plus_res.get(k,0) * points[1]) + (dic2_plus_res.get(k,0) * points[2]) + (dic3_plus_res.get(k,0) * points[3])
    res_lst = test2.dic_fast_sorted(res_dic)
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