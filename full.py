import os
import time
import requests
import feedparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from mailjet_rest import Client as MailjetClient
from supabase import create_client, Client as SupaClient
from openai import OpenAI
import google.generativeai as genai


# Load environment variables
load_dotenv()

# Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")
MAILJET_RECIPIENTS = [email.strip() for email in os.getenv("MAILJET_RECIPIENTS", "").split(",")]
INTERVAL = int(os.getenv("INTERVAL_MINUTES", 60))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Clients
supabase: SupaClient = create_client(SUPABASE_URL, SUPABASE_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)
mailjet = MailjetClient(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version="v3.1")

KEYWORDS = ["speech-to-text", "transcription", "whisper", "voice", "audio ai", "real-time", "openai", "text to speech"]

SOURCES = {
    "rss": [
        "https://www.analyticsvidhya.com/blog/feed/",
        "https://www.reddit.com/r/MachineLearning/.rss"
    ],
    "web": [
        "https://zapier.com/blog/best-text-dictation-software/",
        "https://www.techradar.com/best/best-speech-to-text-software"
    ],
    "selenium": [
        "https://www.reddit.com/r/speechtech/",
        "https://www.pcmag.com/picks/the-best-speech-to-text-software"
    ]
}

def matches_keywords(text):
    return any(k.lower() in text.lower() for k in KEYWORDS)

def fetch_stories():
    print("📰 Scraping AI news...")
    stories = []

    # RSS
    for url in SOURCES["rss"]:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if matches_keywords(entry.title):
                    stories.append({"title": entry.title.strip(), "url": entry.link})
        except Exception as e:
            print(f"❌ RSS error: {e}")

    # BeautifulSoup
    for url in SOURCES["web"]:
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                text = a.text.strip()
                href = requests.compat.urljoin(url, a['href'])
                if matches_keywords(text):
                    stories.append({"title": text[:100], "url": href})
        except Exception as e:
            print(f"❌ Web scraping error: {e}")

    # Selenium
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for url in SOURCES["selenium"]:
        try:
            print(f"🌐 Visiting: {url}")
            driver.get(url)
            time.sleep(3)
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                text = link.text.strip()
                href = link.get_attribute("href")
                if text and href and matches_keywords(text):
                    stories.append({"title": text[:100], "url": href})
        except Exception as e:
            print(f"❌ Selenium error: {e}")
    driver.quit()

    print(f"✅ Found {len(stories)} relevant articles.")
    return stories

def save_to_supabase(stories):
    print("💾 Saving to Supabase...")
    for story in stories:
        try:
            res = supabase.table("stories").insert(story).execute()
            if res.data is None:
                print(f"⚠️ Insert skipped or blocked by RLS for: {story['title']}")
        except Exception as e:
            print(f"❌ Supabase insert failed: {e}")
    print("✅ Supabase save done.")

# def generate_newsletter(stories):
#     print("🧐 Generating newsletter...")
#     joined = "\n".join(f"- {s['title']} ({s['url']})" for s in stories)
#     try:
#         # response = openai.chat.completions.create(
#         #     model="gpt-3.5-turbo",
#         #     messages=[{
#         #         "role": "user",
#         #         "content": f"Summarize the following AI news headlines in a friendly newsletter:\n{joined}"
#         #     }]
#         # )
#         # summary = response.choices[0].message.content.strip()
#         # print("✅ Newsletter generated.")
#         summary = "testing mail generate newsletter"
#         print(joined)
#         return summary
#     except Exception as e:
#         print(f"❌ OpenAI Error: {e}")
#         return joined


def generate_newsletter(stories):
    print("🧐 Generating newsletter using Gemini...")
    joined = "\n".join(f"- {s['title']} ({s['url']})" for s in stories)
    prompt = f"Summarize the following AI news headlines in a short, friendly newsletter:\n{joined}"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        summary = result['candidates'][0]['content']['parts'][0]['text']
        print("✅ Gemini newsletter generated.")
        return summary
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return joined  


def send_newsletter(content):
    print("📨 Sending email...")
    try:
        data = {
            "Messages": [{
                "From": {"Email": MAILJET_SENDER, "Name": "AI Newsletter Bot"},
                "To": [{"Email": email} for email in MAILJET_RECIPIENTS],
                "Subject": "🧠 Daily AI Newsletter",
                "TextPart": content,
                "HTMLPart": f"<pre>{content}</pre>"
            }]
        }
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            print("✅ Email sent.")
        else:
            print(f"❌ Mailjet failed: {result.status_code} - {result.json()}")
    except Exception as e:
        print(f"❌ Mailjet Exception: {e}")

def run_cycle():
    print("\n🚀 Starting newsletter cycle...")
    stories = fetch_stories()
    if not stories:
        print("⚠️ No new stories found.")
        return
    save_to_supabase(stories)
    summary = generate_newsletter(stories)
    send_newsletter(summary)

if __name__ == "__main__":
    while True:
        try:
            run_cycle()
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        print(f"⏳ Waiting {INTERVAL} minutes...\n")
        time.sleep(INTERVAL)
