import os
import json
import re
import random
import html
import time
import urllib.request
from datetime import datetime

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
SITE_URL = "https://qamarsyria.github.io/qamar-cloud-farm"

POSTS_PER_RUN = 5

SOCIAL_BAR = '<script src="https://pl31550649.profitableratecpmnetwork.com/92/61/d9/9261d933b308eb828b628c26fe0bcc81.js"></script>'

NATIVE_BANNER = '''<script async="async" data-cfasync="false" src="https://pl31550650.profitableratecpmnetwork.com/72fe6369c79d70b638130f8c07117e01/invoke.js"></script>
<div id="container-72fe6369c79d70b638130f8c07117e01"></div>'''

# ==== المواضيع (مع تركيز على الإسلاميات) ====
TOPICS = [
    # ============ إسلاميات سنية (50%) ============
    ("islamic", "فضل قراءة القرآن يومياً"),
    ("islamic", "أذكار الصباح والمساء وأثرها في حياة المسلم"),
    ("islamic", "أسماء الله الحسنى ومعانيها"),
    ("islamic", "أهمية الصلاة في حياة المسلم"),
    ("islamic", "فضائل صلاة الفجر"),
    ("islamic", "أدعية مأثورة من السنة النبوية"),
    ("islamic", "أخلاق النبي محمد ﷺ في التعامل مع الناس"),
    ("islamic", "فضل صيام الاثنين والخميس"),
    ("islamic", "أهمية بر الوالدين في الإسلام"),
    ("islamic", "فضائل صلة الرحم"),
    ("islamic", "آداب الطعام والشراب في الإسلام"),
    ("islamic", "كيف تحافظ على صلاة الجماعة"),
    ("islamic", "فضل الاستغفار وأثره"),
    ("islamic", "معاني سورة الفاتحة"),
    ("islamic", "فضل قيام الليل"),
    ("islamic", "أهمية الصدقة في حياة المسلم"),
    ("islamic", "فضائل يوم الجمعة"),
    ("islamic", "أدب المجلس في الإسلام"),
    ("islamic", "فضل حفظ القرآن الكريم"),
    ("islamic", "أهمية طلب العلم الشرعي"),
    ("islamic", "فضل صلة الأرحام"),
    ("islamic", "حقوق الجار في الإسلام"),
    ("islamic", "أثر الدعاء في حياة المسلم"),
    ("islamic", "فضل الصلاة على النبي ﷺ"),
    ("islamic", "معاني أذكار النوم والاستيقاظ"),
    ("islamic", "قصص الأنبياء - قصة نبي الله نوح عليه السلام"),
    ("islamic", "قصص الأنبياء - قصة نبي الله إبراهيم عليه السلام"),
    ("islamic", "قصص الأنبياء - قصة نبي الله يوسف عليه السلام"),
    ("islamic", "قصص الصحابة - أبو بكر الصديق رضي الله عنه"),
    ("islamic", "قصص الصحابة - عمر بن الخطاب رضي الله عنه"),
    ("islamic", "قصص الصحابة - عثمان بن عفان رضي الله عنه"),
    ("islamic", "قصص الصحابة - علي بن أبي طالب رضي الله عنه"),
    ("islamic", "أمهات المؤمنين - السيدة خديجة رضي الله عنها"),
    ("islamic", "أمهات المؤمنين - السيدة عائشة رضي الله عنها"),
    ("islamic", "فضل يوم عرفة"),
    ("islamic", "فضل شهر رمضان"),
    ("islamic", "العشر الأوائل من ذي الحجة"),
    ("islamic", "أهمية التوبة والرجوع إلى الله"),
    ("islamic", "معنى التوكل على الله"),
    ("islamic", "فضل الصبر في الإسلام"),

    # ============ متنوعة (50%) ============
    ("tech", "أفضل تطبيقات الذكاء الاصطناعي في 2026"),
    ("tech", "كيف تحمي خصوصيتك على الإنترنت"),
    ("tech", "أفضل هواتف ذكية لعام 2026"),
    ("health", "عادات صحية بسيطة تغير حياتك"),
    ("health", "فوائد شرب الماء على الريق"),
    ("health", "كيف تحسن جودة نومك"),
    ("health", "أطعمة تقوي المناعة"),
    ("cooking", "وصفة عربية سريعة في 15 دقيقة"),
    ("cooking", "أفضل وصفات الحلويات الشرقية"),
    ("fashion", "ألوان الموضة لهذا الموسم"),
    ("horoscope", "توقعات اليوم لجميع الأبراج"),
    ("sports", "فوائد الرياضة اليومية"),
    ("travel", "أجمل الأماكن السياحية في العالم"),
    ("travel", "نصائح للسفر بميزانية محدودة"),
    ("education", "طرق فعّالة لحفظ المفردات"),
    ("education", "كيف تتعلم لغة جديدة بسرعة"),
    ("cars", "أحدث السيارات الكهربائية"),
    ("selfdev", "كيف تبني عادة القراءة اليومية"),
    ("selfdev", "قوة الاستيقاظ مبكراً"),
    ("selfdev", "كيف تتغلب على التسويف"),
    ("money", "خطوات بسيطة لتوفير المال"),
    ("money", "كيف تبدأ الاستثمار بمبلغ صغير"),
]

# ==== System Prompt حسب نوع الموضوع ====
SYSTEM_ISLAMIC = """أنت كاتب محتوى إسلامي سني محترف على منهج أهل السنة والجماعة.

قواعد صارمة يجب الالتزام بها:
1. اتبع منهج أهل السنة والجماعة فقط.
2. لا تذكر آراء مذهبية متعصبة أو خلافات.
3. استخدم فقط الأحاديث الصحيحة أو الحسنة من كتب السنة المعتمدة (البخاري، مسلم، السنن).
4. لا تنسب للنبي ﷺ شيئاً غير مؤكد.
5. اكتب بأسلوب بسيط ومؤثر، مناسب للعامة.
6. ابدأ المقال بعنوان جذاب، ثم مقدمة، ثم 4-6 فقرات، ثم خاتمة عملية.
7. أضف آية قرآنية أو حديثاً صحيحاً واحداً على الأقل.
8. لا تُفتِ في مسائل خلافية.
9. اختم بدعاء أو نصيحة عملية للتطبيق.
10. اكتب بلغة عربية فصيحة واضحة."""

SYSTEM_GENERAL = """أنت كاتب محتوى عربي محترف. اكتب مقالاً مفيداً بعنوان جذاب، بأسلوب واضح ومنظم مع فقرات قصيرة."""

STYLE = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;line-height:1.9;direction:rtl;padding:20px;max-width:800px;margin:0 auto;min-height:100vh}
header{padding:30px 0;border-bottom:1px solid #334155;margin-bottom:30px;text-align:center}
header a{color:#fbbf24;text-decoration:none;font-size:24px;font-weight:bold}
h1{color:#fbbf24;font-size:26px;margin-bottom:15px;line-height:1.5}
.meta{color:#94a3b8;font-size:13px;margin-bottom:25px;padding-bottom:20px;border-bottom:1px solid #1e293b}
.content p{margin-bottom:18px;font-size:17px}
footer{margin-top:60px;padding-top:20px;border-top:1px solid #334155;color:#64748b;text-align:center;font-size:13px}
.post-card{background:#1e293b;padding:20px;border-radius:12px;margin-bottom:15px;border:1px solid #334155}
.post-card a{color:#fbbf24;text-decoration:none;font-size:20px;font-weight:bold}
.post-card .cat{display:inline-block;background:#334155;color:#94a3b8;padding:3px 10px;border-radius:15px;font-size:12px;margin-top:10px}
.back{color:#fbbf24;text-decoration:none;display:inline-block;margin-top:20px}
.ad-slot{margin:25px 0;text-align:center;min-height:90px}
"""

def generate_article(topic_cat, topic_title):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_API_KEY}", "User-Agent": "Mozilla/5.0"}

    system = SYSTEM_ISLAMIC if topic_cat == "islamic" else SYSTEM_GENERAL

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"اكتب مقالاً (5-7 فقرات) عن: {topic_title}"}
        ],
        "temperature": 0.7, "max_tokens": 1400
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]

# ==== توليد مقالات متعددة ====
os.makedirs("posts", exist_ok=True)
used_titles = set()
generated = 0

topics_shuffled = TOPICS.copy()
random.shuffle(topics_shuffled)

for topic_cat, topic_title in topics_shuffled:
    if generated >= POSTS_PER_RUN:
        break
    if topic_title in used_titles:
        continue

    print("=" * 50)
    print(f"[{generated+1}/{POSTS_PER_RUN}] [{topic_cat}] {topic_title}")

    try:
        content = generate_article(topic_cat, topic_title)
    except Exception as e:
        print(f"  FAILED: {e}")
        continue

    ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    slug = f"{topic_cat}-{ts}"

    paras = [html.escape(line.strip()) for line in content.split("\n") if line.strip()]
    body_parts = []
    for i, p in enumerate(paras):
        body_parts.append(f"<p>{p}</p>")
        if i == 1:
            body_parts.append(f'<div class="ad-slot">{NATIVE_BANNER}</div>')
    body_html = "".join(body_parts)

    post_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(topic_title)}</title>
<meta name="description" content="{html.escape(content[:155])}">
<style>{STYLE}</style>
</head>
<body>
<header><a href="../index.html">🌙 قمر المعرفة</a></header>
<article>
<h1>{html.escape(topic_title)}</h1>
<div class="meta">{datetime.now().strftime('%Y-%m-%d')} · {topic_cat}</div>
<div class="content">{body_html}</div>
<a href="../index.html" class="back">← العودة للرئيسية</a>
</article>
<footer>© 2026 قمر المعرفة</footer>
{SOCIAL_BAR}
</body>
</html>'''

    with open(f"posts/{slug}.html", "w", encoding="utf-8") as f:
        f.write(post_html)
    print(f"  SAVED: {slug}")
    used_titles.add(topic_title)
    generated += 1

    if generated < POSTS_PER_RUN:
        time.sleep(15)

print("=" * 50)
print(f"Generated {generated} posts")

# ==== بناء index.html ====
posts = []
for fname in sorted(os.listdir("posts"), reverse=True):
    if not fname.endswith(".html"):
        continue
    with open(f"posts/{fname}", "r", encoding="utf-8") as f:
        phtml = f.read()
    m = re.search(r"<title>(.*?)</title>", phtml)
    title = m.group(1) if m else fname
    m = re.search(r'<div class="meta">(.*?)</div>', phtml)
    meta = m.group(1) if m else ""
    posts.append({"slug": fname.replace(".html", ""), "title": title, "meta": meta})

cards = "\n".join(
    f'<div class="post-card"><a href="posts/{p["slug"]}.html">{html.escape(p["title"])}</a><div class="cat">{p["meta"]}</div></div>'
    for p in posts
)

index_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>قمر المعرفة — مقالات عربية يومية</title>
<meta name="description" content="مدونة عربية تنشر مقالات يومية في الإسلاميات والتقنية والصحة والطبخ والسفر.">
<style>{STYLE}</style>
</head>
<body>
<header><a href="index.html">🌙 قمر المعرفة</a></header>
<main>
{cards}
</main>
<footer>© 2026 قمر المعرفة</footer>
{SOCIAL_BAR}
</body>
</html>'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print(f"INDEX built with {len(posts)} posts")

# ==== بناء sitemap.xml ====
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
           f'<url><loc>{SITE_URL}/</loc><priority>1.0</priority></url>']
for p in posts:
    sitemap.append(f'<url><loc>{SITE_URL}/posts/{p["slug"]}.html</loc><priority>0.8</priority></url>')
sitemap.append('</urlset>')
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap))
print("SITEMAP built")
