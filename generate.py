import os
import json
import random
import smtplib
import urllib.request
import urllib.error
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
BLOGGER_EMAIL = os.environ.get("BLOGGER_EMAIL", "")

print("Groq:", bool(GROQ_API_KEY))
print("Gmail:", bool(GMAIL_USER))
print("Blogger:", bool(BLOGGER_EMAIL))

TOPICS = [
    ("tech", "أفضل تطبيقات الذكاء الاصطناعي في 2026"),
    ("health", "عادات صحية بسيطة تغير حياتك"),
    ("cooking", "وصفة عربية سريعة في 15 دقيقة"),
    ("fashion", "ألوان الموضة لهذا الموسم"),
    ("islamic", "أذكار الصباح والمساء وأثرها"),
    ("horoscope", "توقعات اليوم لجميع الأبراج"),
    ("sports", "أهم مباريات هذا الأسبوع"),
    ("travel", "أجمل الأماكن السياحية في العالم"),
    ("education", "طرق فعّالة لحفظ المفردات"),
    ("cars", "أحدث السيارات الكهربائية"),
    ("selfdev", "كيف تبني عادة القراءة اليومية"),
    ("money", "خطوات بسيطة لتوفير المال"),
    ("tech", "مستقبل العملات الرقمية في 2026"),
    ("health", "فوائد شرب الماء على الريق"),
    ("cooking", "أفضل وصفات الحلويات الشرقية"),
    ("travel", "أفضل الوجهات السياحية الرخيصة"),
]

topic_cat, topic_title = random.choice(TOPICS)
print(f"Topic: [{topic_cat}] {topic_title}")

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "User-Agent": "Mozilla/5.0"
}

payload = {
    "model": "openai/gpt-oss-120b",
    "messages": [
        {
            "role": "system",
            "content": "أنت كاتب محتوى عربي محترف. اكتب مقالاً مفيداً بعنوان جذاب في البداية، بأسلوب واضح ومنظم مع فقرات قصيرة."
        },
        {
            "role": "user",
            "content": f"اكتب مقالاً قصيراً (5-7 أسطر) عن: {topic_title}"
        }
    ],
    "temperature": 0.8,
    "max_tokens": 1200
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

if GMAIL_USER and GMAIL_APP_PASSWORD and BLOGGER_EMAIL:
    try:
        msg = MIMEMultipart()
        msg["From"] = formataddr(("قمر المعرفة", GMAIL_USER))
        msg["To"] = BLOGGER_EMAIL
        msg["Subject"] = topic_title

        html_body = f"""<h1>{topic_title}</h1>
{content.replace(chr(10), '<br>')}
"""
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, BLOGGER_EMAIL, msg.as_string())

        print("PUBLISHED TO BLOGGER!")
    except Exception as e:
        print("BLOGGER PUBLISH ERROR:", type(e).__name__, str(e)[:300])
else:
    print("Blogger secrets missing - skipping publish")
