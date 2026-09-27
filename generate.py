import os
import requests

token = os.environ["GITHUB_TOKEN"]

print("=" * 60)
print("Token exists:", bool(token))
print("Token length:", len(token) if token else 0)
print("Token prefix:", token[:8] if token else "NONE")
print("=" * 60)

url = "https://models.github.ai/inference/chat/completions"
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
payload = {
    "model": "openai/gpt-4o-mini",
    "messages": [
        {"role": "user", "content": "قل كلمة: نجح"}
    ],
    "max_tokens": 20
}

print("Sending request to:", url)
resp = requests.post(url, headers=headers, json=payload, timeout=60)

print("=" * 60)
print("STATUS CODE:", resp.status_code)
print("=" * 60)
print("RAW RESPONSE:")
print(resp.text[:3000])
print("=" * 60)

if resp.status_code == 200:
    data = resp.json()
    print("PARSED JSON KEYS:", list(data.keys()))
    if "choices" in data:
        content = data["choices"][0]["message"]["content"]
        print("CONTENT:", content)
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(content)
        print("FILE SAVED!")
    else:
        print("NO 'choices' in response!")
else:
    print("REQUEST FAILED!")
