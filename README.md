<div align="center">

# 🔥 MrProxy Cloudflare

**سرور VLESS روی Cloudflare Workers — رایگان، سریع، ضد فیلتر**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Cloudflare](https://img.shields.io/badge/Cloudflare-Workers-orange)](https://workers.cloudflare.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

---

## ✨ امکانات

- 🚀 **رایگان** — ۱۰۰,۰۰۰ درخواست روزانه
- ⚡ **سریع** — CDN کلادفلر
- 🔒 **امن** — TLS کامل
- 🌍 **بدون IP** — دامنه workers.dev
- 📱 **سازگار** — V2RayNG, Nekobox, Clash
- 🛠 **نصب خودکار** — فقط توکن

## 📦 نصب

### پیش‌نیاز
- Python 3.8+
- اکانت Cloudflare (رایگان)

### دریافت API Token

1. برو به https://dash.cloudflare.com/profile/api-tokens
2. **Create Token** → **Custom Token**
3. دسترسی‌ها:
   - `Account` → `Workers Scripts` → **Edit**
   - `Account` → `Workers KV Storage` → **Edit**
4. **Create Token** و کپی کن

### نصب

```bash
git clone https://github.com/amirhazbavi/MrProxy.git
cd MrProxy
python core/installer.py
