#!/bin/bash
# نصب سریع MrProxy

set -e

echo "🔥 MrProxy Installer"
echo "===================="

# چک پایتون
if ! command -v python3 &> /dev/null; then
    echo "❌ پایتون نصب نیست."
    exit 1
fi

# نصب
python3 core/installer.py

# ساخت
python3 core/generator.py

echo "✅ نصب کامل شد!"
