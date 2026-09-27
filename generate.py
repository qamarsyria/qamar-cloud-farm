import os
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=token,
)

try:
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "user", "content": "اكتب مقالاً قصيراً عن فوائد القراءة اليومية في 5 أسطر."}
        ],
        temperature=0.7,
        max_tokens=500
    )

    print("Response type:", type(response))

    if hasattr(response, "choices"):
        post_content = response.choices[0].message.content
    else:
        post_content = str(response)

    print("=" * 50)
    print(post_content)
    print("=" * 50)

    with open("daily_post.txt", "w", encoding="utf-8") as f:
        f.write(post_content)

    print("SUCCESS: File saved!")

except Exception as e:
    print("=" * 50)
    print("FAILED!")
    print("=" * 50)
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    import traceback
    traceback.print_exc()
    raise
