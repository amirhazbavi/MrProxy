#!/usr/bin/env python3
"""دیپلوی خودکار روی Cloudflare"""

import subprocess
import sys
from pathlib import Path

def run(script):
    print(f"▶️ {script}")
    subprocess.run([sys.executable, script], check=True)

if __name__ == "__main__":
    run("core/installer.py")
    run("core/generator.py")
