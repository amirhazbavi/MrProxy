#!/usr/bin/env python3
"""پنل مدیریت ساده"""

import json
from pathlib import Path

class C:
    G='\033[92m'; Y='\033[93m'; C_='\033[96m'; R='\033[91m'; X='\033[0m'; BOLD='\033[1m'

def status():
    print(f"{C.BOLD}{C.C_}📊 Dashboard{C.X}")
    p = Path("config.json")
    if p.exists():
        c = json.loads(p.read_text())
        print(f"{C.G}✅ Worker: {c['worker_url']}{C.X}")
        print(f"   UUID: {c['uuid']}")
    else:
        print(f"{C.R}❌ config.json نیست.{C.X}")
    for f in ["configs.txt", "subscription.txt", "ips.txt", "working_ips.txt"]:
        fp = Path(f)
        if fp.exists():
            n = len(fp.read_text().splitlines())
            print(f"{C.C_}📄 {f}: {n} خط{C.X}")

def main():
    while True:
        print(f"""
{C.Y}1. 📊 وضعیت
2. 🚀 ساخت کانفیگ
3. 📡 اسکن IP
4. ⚡ تست IP
5. ❌ خروج{C.X}""")
        c = input("انتخاب: ").strip()
        if c == '1': status()
        elif c == '2':
            import subprocess, sys
            subprocess.run([sys.executable, "core/generator.py"])
        elif c == '3':
            import subprocess, sys
            subprocess.run([sys.executable, "core/scanner.py"])
        elif c == '4':
            import subprocess, sys
            subprocess.run([sys.executable, "core/tester.py"])
        elif c == '5': break

if __name__ == "__main__":
    main()
