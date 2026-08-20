"""
SPDX-License-Identifier: WTFPL

演示 V2.1 电子鹦鹉（记忆版）。
依赖：arch/core.ipynb、func/func2.ipynb（importnb 直接导入）。
"""
from _bootstrap import test, tongji2, jiaquan_output_test1_1, DATA_DIR

# 加载数据
files = [
    r"D:\Documents\双城记.txt",
    r"D:\Documents\简爱.txt",
    r"D:\天翼云盘下载\罗密欧与朱丽叶.txt",
]
for filename in files:
    test.load_from_file(filename)
    tongji2(test.fenci(open(filename, mode='r', encoding='gbk', errors='ignore').read()))

# 开始测试
while input_words := test.fenci(input("输入内容:")):
    _ = jiaquan_output_test1_1(input_words, '你我他她的是个')