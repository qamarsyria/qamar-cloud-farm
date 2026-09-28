import os
import json
import urllib.request
import urllib.error

api_key = os.environ["GROQ_API_KEY"]
print("Key length:", len(api_key))

# 1) اسأل Groq عن النماذج المتاحة
url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "User-Agent": "Mozilla/5.0"
}

req = urllib.request.Request(url, headers=headers, method="GET")

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
        data = json.loads(body)
        print("=" * 60)
        print("AVAILABLE MODELS:")
        for m in data.get("data", []):
            print("  -", m["id"])
        print("=" * 60)
except Exception as e:
    print("ERROR listing models:", e)
    raise SystemExit(1)
