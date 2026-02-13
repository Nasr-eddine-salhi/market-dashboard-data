import feedparser
import json
import subprocess
import time
from datetime import datetime, timezone

# ================= CONFIG =================
RSS_URL = "https://www.forexlive.com/feed/news/"
NEWS_FILE = "news.json"
CHECK_INTERVAL = 300   # 5 minutes (recommended)
MAX_HEADLINES = 5
# =========================================

def fetch_headlines():
    feed = feedparser.parse(RSS_URL)
    return [e.title.strip() for e in feed.entries[:MAX_HEADLINES]]

def load_existing():
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("headlines", [])
    except Exception:
        return []

def write_news(headlines):
    data = {
        "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "source": "ForexLive",
        "headlines": headlines
    }
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def git_push():
    subprocess.run(["git", "add", NEWS_FILE], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-update market news"], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    print("ForexLive News Daemon started")
    print(f"Checking every {CHECK_INTERVAL} seconds\n")

    while True:
        try:
            new_headlines = fetch_headlines()
            old_headlines = load_existing()

            if new_headlines and new_headlines != old_headlines:
                write_news(new_headlines)
                git_push()
                print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] News updated")
            else:
                print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] No change")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
