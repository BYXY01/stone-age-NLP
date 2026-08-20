"""
SPDX-License-Identifier: WTFPL

演示 V2.5 联网版（搜索引擎注入）。
依赖：arch/core.ipynb、func/func2.ipynb（importnb 直接导入）+ func/get_baidu_result.py。
"""
from _bootstrap import core, func2, get_baidu_result, DATA_DIR

FILES = ["双城记.txt", "简爱.txt", "罗密欧与朱丽叶.txt"]


def load_data():
    for name in FILES:
        path = DATA_DIR / name
        if path.is_file():
            core.load_from_file(str(path))
            core.tongji2(core.fenci(path.read_text(encoding="gbk", errors="ignore")))
            print(f"已加载 {name}")


def main():
    load_data()
    while True:
        raw = input("输入内容 (直接回车退出): ")
        if not raw:
            break
        input_words = core.fenci(raw)
        results = get_baidu_result.get_baidu_search_smart(raw)
        summaries = [r["summary"] for r in results] if results else []
        func2.jiaquan_output_test1_5(input_words, summaries, "你我他她的是个")


if __name__ == "__main__":
    main()