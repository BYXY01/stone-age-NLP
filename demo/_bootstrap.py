"""demo 公共引导：自动定位仓库根并导入 core / func2 / get_baidu_result。

双模式：
- 提取模式：classic/ 已生成，直接导入纯 .py 包（core、func）
- 标准模式：importnb 直接导入 .ipynb（arch.core、func.func2）
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
    import core
    import func as func2
else:
    from importnb import Notebook

    with Notebook():
        import arch.core as core
        import func.func2 as func2

try:
    from func import get_baidu_result
except ImportError:
    get_baidu_result = None

DATA_DIR = ROOT / "data"