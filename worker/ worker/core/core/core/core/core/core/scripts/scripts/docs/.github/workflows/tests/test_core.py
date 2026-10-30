"""تست‌های ساده"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_import():
    import core
    assert core.__version__

def test_worker_exists():
    assert Path("worker/worker.js").exists()

if __name__ == "__main__":
    test_import()
    test_worker_exists()
    print("✅ همه تست‌ها موفق")
