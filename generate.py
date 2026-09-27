import os
from datetime import datetime
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=token,
)

timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
os.makedirs("posts", exist_ok=True)

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "أنت كاتب محتوى عربي محترف."},
        {"role": "user", "content": "اكتب مقالاً قصيراً عن فوائد القراءة اليومية في 5 أسطر."}
    ],
    temperature=0.7,
    max_tokens=500
)

post_content = response.choices[0].message.content

print("=" * 50)
print(post_content)
print("=" * 50)

filename = f"posts/post-{timestamp}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(post_content)

print(f"SUCCESS: File saved to {filename}")
