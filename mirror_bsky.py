import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HANDLE = os.environ["BSKY_HANDLE"]
APP_PASSWORD = os.environ["BSKY_APP_PASSWORD"]
FEED_URL = "https://qamarsyria.github.io/qamar-cloud-farm/feed.xml"
STATE_FILE = "bsky_state.json"
API = "https://bsky.social/xrpc"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f))
    return set()

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(list(state), f)

def create_session():
    url = f"{API}/com.atproto.server.createSession"
    data = json.dumps({"identifier": HANDLE, "password": APP_PASSWORD}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def post_bluesky(session, text):
    url = f"{API}/com.atproto.repo.createRecord"
    payload = {
        "repo": session["did"],
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['accessJwt']}"
        },
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
    session = create_session()
    print(f"Logged in as {session['handle']}")
    for it in new_items:
        text = f"{it['title']}\n{it['link']}"
        try:
            post_bluesky(session, text)
            print(f"Posted: {it['title']}")
            state.add(it["link"])
        except Exception as e:
            print(f"Failed: {e}")
    save_state(state)

if __name__ == "__main__":
    main()
