import os
import json
import subprocess
import sys
from datetime import datetime

# تثبيت requests داخل السكربت
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
import requests

token = os.environ["GITHUB_TOKEN"]
print("=" * 60)
print("Token length:", len(token))
print("Token prefix:", token[:12] + "...")
print("=" * 60)

endpoints = [
    "https://models.github.ai/inference/chat/completions",
    "https://models.github.ai/inference/chat/completions?api-version=2024-08-01-preview",
    "https://models.github.ai/inference/v1/chat/completions",
]

models = ["gpt-4o-mini", "openai/gpt-4o-mini", "gpt-4o"]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "curl/8.0",
}

success = False
for url in endpoints:
    if success:
        break
    for model in models:
        if success:
            break
        print("-" * 60)
        print(f"URL:   {url}")
        print(f"Model: {model}")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say hi in Arabic"}],
            "max_tokens": 30,
        }
        try:
            resp = requests.post(
                url, headers=headers, json=payload,
                timeout=60, allow_redirects=False
            )
            print(f"  Status:  {resp.status_code}")
            print(f"  Location: {resp.headers.get('Location', '-')}")
            print(f"  Body length: {len(resp.content)}")
            print(f"  Body[:300]: {resp.text[:300]}")
            if resp.status_code == 200 and resp.text.strip():
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                print("  ✅ SUCCESS!")
                os.makedirs("posts", exist_ok=True)
                ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
                fn = f"posts/post-{ts}.txt"
                with open(fn, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  SAVED: {fn}")
                success = True
        except Exception as e:
            print(f"  Exception: {type(e).__name__}: {e}")

print("=" * 60)
if not success:
    print("❌ ALL ATTEMPTS FAILED")
    sys.exit(1)
print("✅ DONE")
