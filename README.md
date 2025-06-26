#  Remoat-GTM-Assignment: Automated AI Newsletter 

> **Challenge**: Speech-to-Text Newsletter Automation  
> **Goal**: Scrape, summarize & send AI news via email, fully automated using Supabase, Gemini/OpenAI, Mailjet & n8n.

---

##  Key Objectives

-  **Topic Focused**: Speech-to-Text / Real-time AI
-  **Automation Flow**: Scraping → Summarization → Emailing
-  **10+ Editions** Published Automatically
-  **Zero Manual Intervention** Once Setup
-  **Added Test Script** Test Code and find errors

---

##  Overview

This project scrapes AI-related articles using RSS, BeautifulSoup, and Selenium. The scraped headlines are summarized using **Gemini** (Google) or **OpenAI** and stored in **Supabase**. Summarized newsletters are emailed via **Mailjet**, with scheduling & manual triggers handled via **n8n** automation workflows.

---

##  Architecture Overview

```text
    ┌────────────┐      ┌────────────┐      ┌────────────┐
    │  RSS Feeds │◄────►│  Scrapers  │─────►│  Supabase  │
    └────────────┘      └────────────┘      └────────────┘
                              │
                ┌────────────▼────────────┐
                │  Gemini / OpenAI Models │
                └────────────┬────────────┘
                             ▼
                      ┌────────────┐
                      │  Mailjet   │──────► 📬 Subscribers
                      └────────────┘
                             ▲
                        Trigger via
                    n8n or Scheduled Loop (used here)

```

## n8n Automation

* Set up a Webhook in n8n:

```

 Trigger URL:http://localhost:5678/webhook/newsletter

```

* Workflow Logic:

```
Webhook Trigger → Run Python Script (main.py) → Return Success

```
Example:

```cd /app && python main.py```

This lets you run the newsletter anytime via HTTP trigger or scheduler.


## Setup Instructions

* Local Installation (Recommended for Simplicity)


```bash

git clone https://github.com/deveshruttala/Remoat-GTM-Assginment.git
cd Remoat-GTM-Assginment

cp .env.example .env    # Fill in your Supabase, Mailjet, Gemini/OpenAI keys

pip install -r requirements.txt
python main.py


```

The script runs in an infinite loop and emails at the interval specified in .env


* Docker Installation (Optional)

```bash

docker-compose up --build


```

- n8n available at: http://localhost:5678

- Add n8n Webhook Trigger and connect main.py via Shell command node


* Test.py (only for testing the code)

```bash

python test.py


```


##  Conclusion

This project delivers a fully automated, production-ready AI newsletter generator that scrapes, summarizes, stores, and sends AI-related news articles using:

*  **Python + Selenium + BeautifulSoup + RSS** for multi-source ingestion
*  **Gemini/OpenAI** for intelligent summarization
*  **Supabase** as a scalable and serverless backend
*  **Mailjet** for reliable newsletter delivery to 1000+ subscribers
*  **n8n + Docker** for no-code scheduling, monitoring, and workflow automation
*  **Gemini/OpenAI APIs** for high-quality summarization

### 🎥 Demo

Watch the full 3-minute walkthrough showing:

1. Scraping + summarization
2. Automated newsletter generation
3. Triggering from n8n

 **Demo Video**: [Watch here](Demo%20GTM%20assignment.mp4)



###  Release Documentation

Includes technical overview, features shipped, known issues, and future roadmap.

📘 **Release Notes**: [View release\_notes.md](AI_Newsletter_Release_Notes_v1.0.docx)

## Author

- Devesh

