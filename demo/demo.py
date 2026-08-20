"""
SPDX-License-Identifier: WTFPL

演示 V1/V2 统计与预测工具箱。
依赖：arch/core.ipynb（importnb 直接导入）。
"""
from _bootstrap import core, DATA_DIR

FILES = ["双城记.txt", "简爱.txt", "罗密欧与朱丽叶.txt"]


def load_data():
    for name in FILES:
        path = DATA_DIR / name
        if path.is_file():
            core.load_from_file(str(path))
            print(f"已加载 {name}")


def main():
    load_data()
    core.predict_next(core.word_dic, input("输入一个词："))
    core.predict_next_rand(core.word_dic, input("输入一个词："))
    core.predict_next_rand_r(core.word_dic, input("输入一个词："))
    start, end = input("开始词："), input("结束词：")
    all_node = core.predict_by_loop(core.word_dic, start, end, 500)
    core.get_path_from_PBL(all_node, start, end, -1)
    core.jiaquan_output_test1(core.fenci(input("输入内容")), "你我他她的是个")


if __name__ == "__main__":
    main()