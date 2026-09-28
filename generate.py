import os
import json
import urllib.request
import urllib.error
from datetime import datetime

api_key = os.environ["GROQ_API_KEY"]
print("Key present:", bool(api_key), "| Length:", len(api_key))

url = "https://api.groq.com/openai/v1/chat/completions"

payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "system",
            "content": "أنت كاتب محتوى عربي محترف. اكتب بلغة عربية فصحى واضحة وجذابة."
        },
        {
            "role": "user",
            "content": "اكتب مقالاً قصيراً (4-5 أسطر) بعنوان جذاب عن فوائد القراءة اليومية."
        }
    ],
    "temperature": 0.7,
    "max_tokens": 800
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "User-Agent": "Mozilla/5.0"
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers=headers,
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=90) as resp:
        status = resp.status
        body = resp.read().decode("utf-8")
except urllib.error.HTTPError as e:
    status = e.code
    body = e.read().decode("utf-8")
except Exception as e:
    status = "EXCEPTION"
    body = f"{type(e).__name__}: {e}"

print("STATUS:", status)
print("BODY LENGTH:", len(body))

if status != 200:
    print("ERROR BODY:", body[:2000])
    raise SystemExit(f"Request failed: {status}")

data = json.loads(body)
content = data["choices"][0]["message"]["content"]

print("=" * 60)
print("GENERATED CONTENT:")
print(content)
print("=" * 60)

os.makedirs("posts", exist_ok=True)
ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
fn = f"posts/post-{ts}.txt"
with open(fn, "w", encoding="utf-8") as f:
    f.write(content)
print("SAVED:", fn)
