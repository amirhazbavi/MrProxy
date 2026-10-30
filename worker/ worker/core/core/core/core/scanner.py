#!/usr/bin/env python3
"""اسکنر IP از مخزن"""

import ipaddress
import random
import concurrent.futures
from urllib.request import urlopen, Request

class C:
    G='\033[92m'; Y='\033[93m'; C_='\033[96m'; X='\033[0m'; BOLD='\033[1m'

SOURCES = [
    "https://raw.githubusercontent.com/amirhazbavi/Iplist/refs/heads/main/generated_ips_1000000%20(1).txt",
    "https://raw.githubusercontent.com/amirhazbavi/Iplist/refs/heads/main/generated_ips_100000.txt",
    "https://raw.githubusercontent.com/amirhazbavi/Iplist/refs/heads/main/generated_ips_155165.txt",
    "https://raw.githubusercontent.com/amirhazbavi/Iplist/refs/heads/main/generated_ips_500000.txt",
]

def fetch(url, max_ips):
    ips = []
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as r:
            for line in r:
                if len(ips) >= max_ips: break
                line = line.decode().strip()
                try:
                    ipaddress.ip_address(line)
                    ips.append(line)
                except ValueError:
                    continue
    except Exception as e:
        print(f"{C.Y}⚠️ {url}: {e}{C.X}")
    return ips

def scan(total=5000):
    per = total // len(SOURCES) + 1
    all_ips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SOURCES)) as ex:
        futs = [ex.submit(fetch, u, per) for u in SOURCES]
        for f in concurrent.futures.as_completed(futs):
            all_ips.extend(f.result())
            if len(all_ips) >= total: break
    uniq = list(set(all_ips))
    random.shuffle(uniq)
    return uniq[:total]

if __name__ == "__main__":
    print(f"{C.BOLD}{C.C_}📡 IP Scanner{C.X}")
    n = int(input("تعداد IP (5000): ") or "5000")
    ips = scan(n)
    print(f"{C.G}✅ {len(ips)} IP دریافت شد.{C.X}")
    with open("ips.txt", "w") as f:
        f.write("\n".join(ips))
    print(f"{C.G}📁 ips.txt{C.X}")
