"""
SPDX-License-Identifier: WTFPL

演示 V1/V2 统计与预测工具箱。
依赖：arch/core.ipynb（importnb 直接导入）。
"""
import sys
from pathlib import Path

def _find_root(p):
    for _ in range(4):
        if (p / "classic").is_dir() or (p / "arch").is_dir():
            return p
        p = p.parent
    return p.parent.parent

REPO_ROOT = _find_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(REPO_ROOT))

_IN_CLASSIC = (REPO_ROOT / "classic").is_dir()
if _IN_CLASSIC:
    # 提取模式：classic/ 已生成，直接导入纯 .py
    sys.path.insert(0, str(REPO_ROOT / "classic"))
    import core
else:
    # 标准模式：importnb 直接导入 .ipynb
    from importnb import Notebook

    with Notebook():
        import arch.core as core

DATA_DIR = REPO_ROOT / "data"
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