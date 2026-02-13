import feedparser
import json
import subprocess
from datetime import datetime, timezone

# ================== CONFIG ==================
RSS_URL = "https://www.forexlive.com/feed/news/"
NEWS_FILE = "news.json"
MAX_HEADLINES = 5
# ============================================

def fetch_forexlive_news():
    feed = feedparser.parse(RSS_URL)
    headlines = []

    for entry in feed.entries[:MAX_HEADLINES]:
        title = entry.title.strip()
        headlines.append(title)

    return headlines

def write_news_file(headlines):
    data = {
        "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "source": "ForexLive",
        "headlines": headlines
    }

    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def git_push():
    subprocess.run(["git", "add", NEWS_FILE])
    subprocess.run(["git", "commit", "-m", "Update market news"])
    subprocess.run(["git", "push"])

def main():
    headlines = fetch_forexlive_news()

    if not headlines:
        print("No news fetched")
        return

    write_news_file(headlines)
    git_push()
    print("News updated and pushed successfully")

if __name__ == "__main__":
    main()
