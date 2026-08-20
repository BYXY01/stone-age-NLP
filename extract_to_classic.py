#!/usr/bin/env python3
"""
extract_to_classic.py —— 从 .ipynb 提取代码到 classic/ 目录（拆分包结构）

按每个 code cell 的 metadata["tags"] 标记把 notebook 拆成独立模块，
生成与 main 英文分支同构的包结构：

    classic/
    ├── core/                     # 来自 arch/core.ipynb (CC-BY-4.0)，arch 改名 core
    │   ├── __init__.py
    │   ├── config.py             #  @config
    │   ├── test.py               #  @test      (V1)
    │   ├── test_func.py          #  @test_func
    │   ├── test2.py              #  @test2     (V2)
    │   ├── test3.py              #  @test3     (V3)
    │   └── test4.py              #  @test4     (V4)
    ├── func/                     # 来自 func/func2.ipynb (MIT)
    │   ├── __init__.py
    │   ├── test2_1.py            #  @test2_1   (V2.1)
    │   ├── test2_5.py            #  @test2_5   (V2.5)
    │   ├── get_baidu_result.py   # 复制自 func/
    │   └── get_baidu_result2.py  # 复制自 func/
    └── demo/                     # 复制自 demo/ (WTFPL)
        ├── _bootstrap.py         # 公共引导（路径定位 + 双模式导入）
        ├── demo.py
        ├── demo_1.py
        └── demo_5.py

classic/ 已加入 .gitignore。
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "classic"

NOTEBOOKS = [
    (ROOT / "arch" / "core.ipynb", "core", "CC-BY-4.0"),
    (ROOT / "func" / "func2.ipynb", "func", "MIT"),
]

# notebook 内为共享命名空间（原版代码，仅把 test./test2. 模块限定引用改为裸变量）。
# 拆分后每个模块需要注入标准 import 头（与 main 分支的模块依赖一致）：
MODULE_HEADERS = {
    # core/ 包内
    "config": [],
    "test": ["import jieba", "import re", "", "from core.config import repl, vocab_headefine"],
    "test_func": ["import random", "", "from core.config import repl"],
    "test2": ["from core.test import word_dic", "from core.config import repl"],
    "test3": ["from core.test import word_dic", "from core.test2 import word_dic_2", "from core.config import repl"],
    "test4": ["from itertools import pairwise", "from core.config import repl"],
    # func/ 包内
    "test2_1": ["from core.test import tongji", "from core.test2 import tongji2, jiaquan_output_test1"],
    "test2_5": ["import re", "", "from core.test import fenci, tongji, word_dic", "from core.config import repl", "from core.test2 import jiaquan1, tongji2, word_dic_2"],
}

COPY_FILES = [
    (ROOT / "func" / "get_baidu_result.py", "func/get_baidu_result.py"),
    (ROOT / "func" / "get_baidu_result2.py", "func/get_baidu_result2.py"),
    (ROOT / "demo" / "_bootstrap.py", "demo/_bootstrap.py"),
    (ROOT / "demo" / "demo.py", "demo/demo.py"),
    (ROOT / "demo" / "demo_1.py", "demo/demo_1.py"),
    (ROOT / "demo" / "demo_5.py", "demo/demo_5.py"),
]

# demo 里的 import 在提取后要改指向 classic 包。
IMPORT_REWRITES = [
    (r"from demo\._bootstrap import", "from _bootstrap import"),
]

SPDX_HEADER = """# SPDX-License-Identifier: {license_id}
# 本文件由 extract_to_classic.py 从 {source} 自动提取。
# 上游文档与完整说明见 https://github.com/BYXY01/stone-age-NLP
"""


def grouped_cells(ipynb_path: Path) -> dict:
    """按 cell 的 metadata["tags"][0] 分组，返回 {tag: [code_block, ...]}。
    无 tag 的 code cell（如依赖导入）跳过，不生成模块。"""
    nb = json.loads(ipynb_path.read_text(encoding="utf-8"))
    groups = {}
    order = []
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        tags = cell["metadata"].get("tags") or []
        if not tags:
            continue
        tag = tags[0]
        code = "".join(cell["source"]).rstrip() + "\n"
        if tag not in groups:
            groups[tag] = []
            order.append(tag)
        groups[tag].append(code)
    return {tag: "\n".join(groups[tag]) for tag in order}


def build_module(ipynb_path: Path, pkg: str, tag: str, license_id: str):
    """把某个标记下的全部代码写为 classic/<pkg>/<tag>.py，注入模块头。"""
    code = grouped_cells(ipynb_path)[tag]
    header_lines = MODULE_HEADERS.get(tag, [])
    body = "\n\n".join(header_lines + [code]) + "\n" if header_lines else code + "\n"
    header = SPDX_HEADER.format(license_id=license_id, source=f"{ipynb_path} (cell @{tag})")
    out = OUT / pkg / f"{tag}.py"
    out.write_text(header + body, encoding="utf-8")
    print(f"  ✓ {pkg}/{tag}.py  ({license_id})")


def copy_file(src: Path, rel: str, license_id: str):
    text = src.read_text(encoding="utf-8")
    for pattern, repl in IMPORT_REWRITES:
        text = re.sub(pattern, repl, text)
    header = SPDX_HEADER.format(license_id=license_id, source=str(src))
    out = OUT / rel
    out.write_text(header + text, encoding="utf-8")
    print(f"  ✓ {rel}  ({license_id})")


def write_init(pkg: str, submodules: list):
    init = OUT / pkg / "__init__.py"
    body = "# 由 extract_to_classic.py 生成\n"
    for mod in submodules:
        body += f"from .{mod} import *\n"
    init.write_text(body, encoding="utf-8")
    print(f"  ✓ {pkg}/__init__.py")


def main():
    OUT.mkdir(exist_ok=True)
    print("提取到 classic/ ...")
    for nb, pkg, lic in NOTEBOOKS:
        (OUT / pkg).mkdir(exist_ok=True)
        tags = list(grouped_cells(nb))
        for tag in tags:
            build_module(nb, pkg, tag, lic)
        write_init(pkg, tags)
    for src, rel in COPY_FILES:
        lic = "WTFPL" if rel.startswith("demo/") else "MIT"
        out = OUT / rel
        out.parent.mkdir(exist_ok=True)
        copy_file(src, rel, lic)
    print("\n完成。运行演示:")
    print("  python demo/demo_1.py")


if __name__ == "__main__":
    main()