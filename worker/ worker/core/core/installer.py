#!/usr/bin/env python3
"""نصب خودکار Worker روی Cloudflare"""

import json
import urllib.request
import urllib.error
from pathlib import Path

class C:
    R='\033[91m'; G='\033[92m'; Y='\033[93m'; C_='\033[96m'; X='\033[0m'; BOLD='\033[1m'

API = "https://api.cloudflare.com/client/v4"
CONFIG = "config.json"

def req(method, path, token, body=None, ctype="application/json"):
    url = f"{API}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    data = None
    if body is not None:
        if isinstance(body, dict):
            data = json.dumps(body).encode()
            headers["Content-Type"] = ctype
        else:
            data = body
            headers["Content-Type"] = ctype
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try: return json.loads(e.read().decode())
        except: return {"success": False, "errors": [{"message": str(e)}]}

def get_account(token):
    r = req("GET", "/accounts", token)
    if not r.get("success"):
        print(f"{C.R}❌ {r.get('errors')}{C.X}")
        return None
    accs = r["result"]
    if not accs:
        print(f"{C.R}❌ اکانت پیدا نشد.{C.X}")
        return None
    if len(accs) == 1:
        print(f"{C.G}✅ {accs[0]['name']}{C.X}")
        return accs[0]["id"]
    for i, a in enumerate(accs, 1):
        print(f"  {i}. {a['name']} ({a['id']})")
    return accs[int(input("انتخاب: "))-1]["id"]

def deploy(token, acc, name, script):
    r = req("PUT", f"/accounts/{acc}/workers/scripts/{name}", token, script, "application/javascript")
    return r.get("success", False)

def enable(token, acc, name):
    req("POST", f"/accounts/{acc}/workers/scripts/{name}/subdomain",
        token, {"enabled": True, "previews_enabled": False})

def subdomain(token, acc):
    r = req("GET", f"/accounts/{acc}/workers/subdomain", token)
    return r["result"].get("subdomain") if r.get("success") else None

def main():
    print(C.BOLD + C.C_ + "☁️  MrProxy Cloudflare Installer" + C.X)
    token = input("🔑 API Token: ").strip()
    if not token: return

    acc = get_account(token)
    if not acc: return

    name = input("نام Worker (mrproxy): ").strip() or "mrproxy"

    wpath = Path("worker/worker.js")
    if not wpath.exists():
        print(f"{C.R}❌ worker/worker.js پیدا نشد.{C.X}")
        return

    print(f"{C.C_}📤 در حال آپلود...{C.X}")
    if not deploy(token, acc, name, wpath.read_text()):
        print(f"{C.R}❌ آپلود ناموفق.{C.X}")
        return
    print(f"{C.G}✅ آپلود شد.{C.X}")

    enable(token, acc, name)
    sub = subdomain(token, acc)
    if not sub:
        print(f"{C.R}❌ subdomain پیدا نشد.{C.X}")
        return

    url = f"{name}.{sub}.workers.dev"
    print(f"\n{C.G}{'='*50}{C.X}")
    print(f"{C.BOLD}✅ نصب کامل شد!{C.X}")
    print(f"{C.C_}🌐 {url}{C.X}")
    print(f"{C.G}{'='*50}{C.X}")

    Path(CONFIG).write_text(json.dumps({
        "worker_url": url,
        "uuid": "50414e45-4c5f-5a45-5553-a83e1adb66b6",
        "worker_name": name,
        "account_id": acc,
    }, indent=2, ensure_ascii=False))
    print(f"{C.G}📁 config.json ذخیره شد.{C.X}")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.R}لغو شد.{C.X}")
