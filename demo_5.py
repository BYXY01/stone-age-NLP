from test2_5 import *
import get_baidu_result2

#加载数据
files=[
    r"D:\Documents\双城记.txt",
    r"D:\Documents\简爱.txt",
    r"D:\天翼云盘下载\罗密欧与朱丽叶.txt"
]
for filename in files:
    test.load_from_file(filename)
    tongji2(test.fenci(open(filename,mode='r',encoding='gbk',errors='ignore').read()))

#初始化搜索器
searcher = get_baidu_result2.BaiduSearcherEdge(headless=True)

#开始测试
while input_str:=input("输入内容:"):
    input_words=test.fenci(input_str)
    web_results=searcher.search(input_words)
    WR_lst=[]
    for i, res in enumerate(web_results, 1):
        WR_lst.append(res['summary'])
    _=jiaquan_output_test1_5(input_words,WR_lst,'你我他她的是个')