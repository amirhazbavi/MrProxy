#!/usr/bin/env python3
"""تست TCP پورت‌های IP"""

import asyncio
import socket
import time

class C:
    G='\033[92m'; Y='\033[93m'; C_='\033[96m'; X='\033[0m'; BOLD='\033[1m'

async def test(host, port, timeout=1.0):
    try:
        start = time.time()
        r, w = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        lat = (time.time() - start) * 1000
        w.close()
        await w.wait_closed()
        return lat
    except:
        return None

async def main():
    print(f"{C.BOLD}{C.C_}⚡ Tester{C.X}")
    target = input("فایل IP (ips.txt): ").strip() or "ips.txt"
    port = int(input("پورت (443): ") or "443")
    try:
        with open(target) as f:
            ips = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"{C.Y}❌ فایل پیدا نشد.{C.X}")
        return

    sem = asyncio.Semaphore(200)
    async def one(ip):
        async with sem:
            return ip, await test(ip, port)
    tasks = [one(ip) for ip in ips]
    res = await asyncio.gather(*tasks)
    ok = [(i, l) for i, l in res if l is not None]
    ok.sort(key=lambda x: x[1])
    print(f"{C.G}✅ {len(ok)}/{len(ips)} پاسخ داد.{C.X}")
    with open("working_ips.txt", "w") as f:
        for i, l in ok:
            f.write(f"{i}\n")
    print(f"{C.G}📁 working_ips.txt{C.X}")

if __name__ == "__main__":
    asyncio.run(main())
