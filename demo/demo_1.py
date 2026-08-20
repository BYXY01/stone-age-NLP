"""
SPDX-License-Identifier: WTFPL

演示 V2.1 电子鹦鹉（记忆版）。
依赖：arch/core.ipynb、func/func2.ipynb（importnb 直接导入）。
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
    import func as func2
else:
    # 标准模式：importnb 直接导入 .ipynb
    from importnb import Notebook

    with Notebook():
        import arch.core as core
        import func.func2 as func2

DATA_DIR = REPO_ROOT / "data"
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
        words = core.fenci(raw)
        func2.jiaquan_output_test1_1(words, "你我他她的是个")


if __name__ == "__main__":
    main()