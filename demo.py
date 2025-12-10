from test2 import *

#加载数据
test.load_from_file("双城记.txt")
test.load_from_file("简爱.txt")
test.load_from_file("罗密欧与朱丽叶.txt")
test_words_1=test.fenci(open("双城记.txt",mode='r',encoding='gbk',errors='ignore').read())
test_words_2=test.fenci(open("简爱.txt",mode='r',encoding='gbk',errors='ignore').read())
test_words_3=test.fenci(open("罗密欧与朱丽叶.txt",mode='r',encoding='gbk',errors='ignore').read())
tongji2(test_words_1)
tongji2(test_words_2)
tongji2(test_words_3)

#开始测试
test.test_func.predict_next(test.word_dic,input("输入一个词："))
test.test_func.predict_next_rand(test.word_dic,input("输入一个词："))
test.test_func.predict_next_rand_r(test.word_dic,input("输入一个词："))
start,end=input("开始词："),input("结束词：")
all_node=test.test_func.predict_by_loop(test.word_dic,start,end,500)
test.test_func.get_path_from_PBL(all_node,start,end,-1)

_=jiaquan_output_test1(test.fenci(input("输入内容")),'你我他她的是个')