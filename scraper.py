from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

KEYWORDS = [
    "speech-to-text", "transcription", "whisper",
    "voice", "audio ai", "real-time audio", "openai whisper"
]

def scrape_ai_news():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # ✅ Corrected setup with Service object
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    urls = [
        "https://zapier.com/blog/best-text-dictation-software/",
        "https://www.zdnet.com/article/best-speech-to-text-software/",
        "https://www.pcmag.com/picks/the-best-speech-to-text-software",
        "https://www.techradar.com/best/best-speech-to-text-software",
        "https://www.reddit.com/r/speechtech/",
        "https://www.reddit.com/r/MachineLearning/",
        "https://www.analyticsvidhya.com/blog/",
    ]

    results = []

    for url in urls:
        try:
            print(f"🔍 Visiting: {url}", flush=True)
            driver.get(url)
            time.sleep(3)  # wait for JS content

            links = driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                text = link.text.strip()
                href = link.get_attribute('href')

                if text and href and any(keyword in text.lower() or keyword in href.lower() for keyword in KEYWORDS):
                    results.append({
                        "title": text,
                        "url": href
                    })

        except Exception as e:
            print(f"❌ Error scraping {url}: {e}", flush=True)

    driver.quit()
    return results
