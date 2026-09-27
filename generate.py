import os
import json
import urllib.request
import urllib.error

token = os.environ["GITHUB_TOKEN"]

print("=" * 60)
print("Token exists:", bool(token))
print("Token length:", len(token) if token else 0)
print("=" * 60)

url = "https://models.github.ai/inference/chat/completions"
payload = {
    "model": "openai/gpt-4o-mini",
    "messages": [{"role": "user", "content": "قل كلمة: نجح"}],
    "max_tokens": 20
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

print("=" * 60)
print("STATUS CODE:", status)
print("=" * 60)
print("RAW RESPONSE:")
print(body[:3000])
print("=" * 60)

if status == 200:
    try:
        data = json.loads(body)
        print("PARSED KEYS:", list(data.keys()))
        if "choices" in data:
            content = data["choices"][0]["message"]["content"]
            print("CONTENT:", content)
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("FILE SAVED!")
        else:
            print("NO 'choices' KEY!")
    except Exception as e:
        print("PARSE ERROR:", e)
