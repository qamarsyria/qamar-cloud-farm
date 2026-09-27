import os
import json
import urllib.request
import urllib.error
from datetime import datetime

token = os.environ["GITHUB_TOKEN"]

print("=" * 60)
print("Starting AI Post Generation")
print("Token length:", len(token) if token else 0)
print("=" * 60)

url = "https://models.github.ai/inference/chat/completions"
payload = {
    "model": "openai/gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": "أنت كاتب محتوى عربي محترف. اكتب مقالات واضحة ومفيدة باللغة العربية الفصحى."
        },
        {
            "role": "user",
            "content": "اكتب مقالاً قصيراً (4-5 أسطر) عن فوائد القراءة اليومية. أضف عنواناً جذاباً في البداية."
        }
    ],
    "temperature": 0.7,
    "max_tokens": 800
}

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers=headers,
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        status = resp.status
        body = resp.read().decode("utf-8")
except urllib.error.HTTPError as e:
    status = e.code
    body = e.read().decode("utf-8")
except Exception as e:
    status = "EXCEPTION"
    body = f"{type(e).__name__}: {e}"

print("STATUS CODE:", status)

if status != 200:
    print("RAW RESPONSE:", body[:2000])
    raise SystemExit(f"Request failed with status {status}")

data = json.loads(body)
content = data["choices"][0]["message"]["content"]

print("=" * 60)
print("GENERATED CONTENT:")
print(content)
print("=" * 60)

os.makedirs("posts", exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"posts/post-{timestamp}.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

print("FILE SAVED:", filename)
print("DONE!")
