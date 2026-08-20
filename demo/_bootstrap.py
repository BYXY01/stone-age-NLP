"""demo 公共引导：自动定位仓库根并导入 core / func2 / 搜索器。

双模式：
- 提取模式：classic/ 已生成，直接导入纯 .py 包（core、func）
- 标准模式：importnb 直接导入 .ipynb（arch.core、func.func2）

对齐原版扁平结构，导出 `test`（= core 模块）、`test.test_func` 链、
裸函数 tongji2 / jiaquan_output_test1 / _1 / _5，以及搜索器与 DATA_DIR。
"""
import sys
from pathlib import Path

def _find_root(p):
    for _ in range(4):
        if (p / "classic").is_dir() or (p / "arch").is_dir():
            return p
        p = p.parent
    return p.parent.parent

ROOT = _find_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(ROOT))

if (ROOT / "classic").is_dir():
    sys.path.insert(0, str(ROOT / "classic"))
    import core as test
    import func
    from func import get_baidu_result2
else:
    from importnb import Notebook

    with Notebook():
        import arch.core as test
        import func.func2 as func
    import func.get_baidu_result2 as get_baidu_result2

# 原版 test.py 里 `import test_func`，使 `test.test_func` 链可用。
# 提取模式：core 包下有 test_func 子模块；标准模式：共享命名空间已铺平到 core。
test.test_func = test.test_func if hasattr(test, "test_func") else test

tongji2 = test.tongji2
jiaquan_output_test1 = test.jiaquan_output_test1
# 标准模式 func2 是共享命名空间，test2_1/test2_5 符号铺平；提取模式是子模块。
jiaquan_output_test1_1 = func.jiaquan_output_test1_1 if hasattr(func, "jiaquan_output_test1_1") else func.test2_1.jiaquan_output_test1_1
jiaquan_output_test1_5 = func.jiaquan_output_test1_5 if hasattr(func, "jiaquan_output_test1_5") else func.test2_5.jiaquan_output_test1_5

DATA_DIR = ROOT / "data"