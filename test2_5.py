# 增加外部资料添加到统计
from test2 import *

def jiaquan_output_test1_fix(words,ignor_words=''):
    lst=[]
    lst.extend(words)
    print(*words,sep='',end='')
    while lst[-1] != repl:
        jiaquan_res=jiaquan1(lst,test.word_dic,word_dic_2)
        while jiaquan_res[0][0] in ignor_words or jiaquan_res[0][0] in lst:
            jiaquan_res.pop(0)
        new_word=jiaquan_res[0][0]
        lst.append(new_word)
        print(new_word,end='')
    print()
    return lst

def jiaquan_output_test1_5(words,Ref_Data,ignor_words=''):
    def Proces_Ref_Data():
        result=""
        if type(Ref_Data) is type(list()):
            for i_str in Ref_Data:
                no_sign_i_str=re.sub(r'\W', '', i_str)
                result+=(no_sign_i_str+'_')
        if type(Ref_Data) is type(str()):
            result=Ref_Data+'_'
        # return result
        return test.fenci(result)
    test.tongji(Proces_Ref_Data())
    tongji2(Proces_Ref_Data())
    try:
        jiaquan_output_test1_fix(words,ignor_words)
    except:
        jiaquan_output_test1_fix(words+['_'], ignor_words)
