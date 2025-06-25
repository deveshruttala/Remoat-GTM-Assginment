import sys

import time
from scraper import scrape_ai_news
from generator import generate_content
from emailer import send_newsletter
from database import init_db, save_stories
sys.stdout.reconfigure(line_buffering=True)  

def run_once():
    print("🚀 Starting newsletter bot cycle...")

    print("🔧 Initializing DB...")
    init_db()

    print("🕵️ Scraping AI news...")
    stories = scrape_ai_news()
    print(f"✅ Scraped {len(stories)} stories.")

    print("💾 Saving to database...")
    save_stories(stories)

    print("🧠 Generating newsletter content...")
    newsletter = generate_content(stories)

    print("📨 Sending newsletter...")
    send_newsletter(newsletter)

    print("✅ Cycle completed.\n")

if __name__ == "__main__":
    while True:
        try:
            run_once()
        except Exception as e:
            print(f"❌ Error in cycle: {e}")
        print("🕒 Waiting 20 sec before next run...\n")
        time.sleep(20)  # 5 minutes = 300 seconds
