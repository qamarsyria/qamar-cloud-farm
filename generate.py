import os
import json
import random
import urllib.request
import urllib.error
from datetime import datetime

api_key = os.environ["GROQ_API_KEY"]

TOPICS = [
    ("تقنية", "أفضل تطبيقات الذكاء الاصطناعي في 2026"),
    ("صحة", "عادات صحية بسيطة تغير حياتك"),
    ("طبخ", "وصفة عربية سريعة في 15 دقيقة"),
    ("موضة", "ألوان الموضة لهذا الموسم"),
    ("إسلاميات", "أذكار الصباح والمساء وأثرها"),
    ("أبراج", "توقعات اليوم لجميع الأبراج"),
    ("رياضة", "أهم مباريات هذا الأسبوع"),
    ("سياحة", "أجمل الأماكن السياحية في العالم"),
    ("تعليم", "طرق فعّالة لحفظ المفردات"),
    ("سيارات", "أحدث السيارات الكهربائية"),
    ("تطوير ذات", "كيف تبني عادة القراءة اليومية"),
    ("مال", "خطوات بسيطة لتوفير المال"),
]

topic_cat, topic_title = random.choice(TOPICS)
print(f"Topic: [{topic_cat}] {topic_title}")

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "User-Agent": "Mozilla/5.0"
}

payload = {
    "model": "openai/gpt-oss-120b",
    "messages": [
        {
            "role": "system",
            "content": "أنت كاتب محتوى عربي محترف. اكتب مقالاً مفيداً بعنوان جذاب، بأسلوب واضح وجذاب."
        },
        {
            "role": "user",
            "content": f"اكتب مقالاً قصيراً (5-6 أسطر) عن: {topic_title}"
        }
    ],
    "temperature": 0.8,
    "max_tokens": 1000
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers=headers,
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = resp.read().decode("utf-8")
except urllib.error.HTTPError as e:
    print("ERROR:", e.code, e.read().decode("utf-8")[:500])
    raise SystemExit(1)

data = json.loads(body)
content = data["choices"][0]["message"]["content"]

print("=" * 60)
print(content)
print("=" * 60)

os.makedirs("posts", exist_ok=True)
ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
safe_cat = topic_cat.replace("/", "-")
fn = f"posts/{safe_cat}-{ts}.txt"
with open(fn, "w", encoding="utf-8") as f:
    f.write(f"# {topic_title}\n\n{content}")
print("SAVED:", fn)
