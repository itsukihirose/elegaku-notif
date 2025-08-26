import os
import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CAST_URL = "https://www.elegaku.com/profile/top/castCode/382626/"
STATE_FILE = "last_status.txt"

def fetch_schedule():
    res = requests.get(CAST_URL)
    soup = BeautifulSoup(res.text, "html.parser")
    div = soup.find("div", class_="cast-schedule__list")
    return div.get_text(strip=True) if div else ""

def notify_discord(message):
    if not WEBHOOK_URL:
        print("❌ Discord Webhook URL not found.")
        return
    requests.post(WEBHOOK_URL, json={"content": message})

def main():
    current = fetch_schedule()

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            previous = f.read()
    else:
        previous = ""

    if current != previous:
        notify_discord(f"🌟 星野さんの出勤情報が更新されました！\n👉 {CAST_URL}")
        with open(STATE_FILE, "w") as f:
            f.write(current)
    else:
        print("出勤情報に変化なし。")

if __name__ == "__main__":
    main()
