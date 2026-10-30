#!/usr/bin/env python3
"""ساخت کانفیگ VLESS از Worker URL"""

import json
import base64
from pathlib import Path

class C:
    G='\033[92m'; Y='\033[93m'; C_='\033[96m'; R='\033[91m'; X='\033[0m'; BOLD='\033[1m'

def main():
    p = Path("config.json")
    if not p.exists():
        print(f"{C.R}❌ اول installer.py اجرا کن.{C.X}")
        return
    cfg = json.loads(p.read_text())
    url, uuid = cfg["worker_url"], cfg["uuid"]

    print(f"{C.BOLD}{C.G}🔗 MrProxy Generator{C.X}")
    print(f"Worker: {url}\n")

    name = input("📝 نام (MrProxy): ").strip() or "MrProxy"
    count = int(input("🔢 تعداد (1): ") or "1")

    base = (f"vless://{uuid}@{url}:443"
            f"?encryption=none&security=tls&type=ws&host={url}&path=%2F&sni={url}")

    links = []
    for i in range(count):
        n = f"{name}-{i+1}"
        link = f"{base}#{n}"
        links.append(link)
        print(f"\n{C.G}{i+1}. {n}{C.X}")
        print(f"{C.C_}{link}{C.X}")

    txt = "\n".join(links)
    Path("configs.txt").write_text(txt, encoding="utf-8")
    Path("subscription.txt").write_text(base64.b64encode(txt.encode()).decode(), encoding="utf-8")

    print(f"\n{C.G}📁 configs.txt{C.X}")
    print(f"{C.G}📁 subscription.txt{C.X}")
    print(f"\n{C.Y}📱 در V2RayNG → Import from Clipboard{C.X}")

if __name__ == "__main__":
    main()
