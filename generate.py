import os
from openai import OpenAI

# تهيئة العميل للاتصال بـ GitHub Models
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_TOKEN"]
)

# تحديد النموذج والطلب
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "أنت كاتب محتوى عربي محترف. اكتب مقالاً قصيراً ومفيداً."},
        {"role": "user", "content": "اكتب مقالاً عن فوائد القراءة اليومية في 5 أسطر."}
    ],
    temperature=0.7,
    max_tokens=500
)

# استخراج النص من الرد
post_content = response.choices[0].message.content

# حفظ المحتوى في ملف
with open("daily_post.txt", "w", encoding="utf-8") as f:
    f.write(post_content)

print("تم إنشاء المقال بنجاح وحفظه في daily_post.txt")
