import os
import json
import urllib.request
import urllib.error
from datetime import datetime

token = os.environ["GITHUB_TOKEN"]
print("Token present:", bool(token), "| Length:", len(token))

url = "https://models.inference.ai.azure.com/chat/completions"
print("URL:", url)

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "أنت كاتب محتوى عربي محترف. اكتب بلغة عربية فصحى واضحة."},
        {"role": "user", "content": "اكتب مقالاً قصيراً (4-5 أسطر) بعنوان جذاب عن فوائد القراءة اليومية."}
    ],
    "temperature": 0.7,
    "max_tokens": 800
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
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
        body = resp.read().decode("utf-8", errors="replace")
except urllib.error.HTTPError as e:
    status = e.code
    body = e.read().decode("utf-8", errors="replace")
except Exception as e:
    status = "EXCEPTION"
    body = f"{type(e).__name__}: {e}"

print("STATUS:", status)
print("BODY LENGTH:", len(body))
print("BODY (first 1500 chars):")
print(body[:1500])
print("=" * 60)

if status != 200 or not body.strip():
    raise SystemExit(f"Request failed. Status={status}")

data = json.loads(body)
content = data["choices"][0]["message"]["content"]

print("GENERATED CONTENT:")
print(content)
print("=" * 60)

os.makedirs("posts", exist_ok=True)
ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
fn = f"posts/post-{ts}.txt"
with open(fn, "w", encoding="utf-8") as f:
    f.write(content)
print("SAVED:", fn)
