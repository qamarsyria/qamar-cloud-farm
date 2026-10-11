import os
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

MASTODON_URL = "https://mastodon.social"
ACCESS_TOKEN = os.environ["MASTODON_TOKEN"]
FEED_URL = "https://qamarsyria.github.io/qamar-cloud-farm/feed.xml"
STATE_FILE = "mastodon_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f))
    return set()

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(list(state), f)

def post_toot(text):
    url = f"{MASTODON_URL}/api/v1/statuses"
    data = urllib.parse.urlencode({"status": text}).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def fetch_feed():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def main():
    state = load_state()
    xml_data = fetch_feed()
    root = ET.fromstring(xml_data)
    items = root.findall(".//item")
    new_items = []
    for item in items:
        link = item.findtext("link", "").strip()
        title = item.findtext("title", "").strip()
        if link and link not in state:
            new_items.append({"title": title, "link": link})
    if not new_items:
        print("No new items")
        return
    new_items.reverse()
    for it in new_items:
        text = f"{it['title']}\n{it['link']}"
        try:
            post_toot(text)
            print(f"Posted: {it['title']}")
            state.add(it["link"])
        except Exception as e:
            print(f"Failed: {e}")
    save_state(state)

if __name__ == "__main__":
    main()
