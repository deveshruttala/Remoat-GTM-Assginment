import os
import time
import threading
import requests
from flask import Flask, jsonify, request
from supabase import create_client, Client as SupaClient
from dotenv import load_dotenv
from main import fetch_stories, save_to_supabase, generate_newsletter, send_newsletter

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
INTERVAL = int(os.getenv("INTERVAL_MINUTES", 60))

supabase: SupaClient = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
running = False
thread = None
scrape_count = 0
latest_summary = ""


def run_cycle():
    global scrape_count, latest_summary
    while running:
        try:
            stories = fetch_stories()
            scrape_count = len(stories)
            if stories:
                save_to_supabase(stories)
                latest_summary = generate_newsletter(stories)
                send_newsletter(latest_summary)
        except Exception as e:
            print(f"Unexpected error: {e}")
        time.sleep(INTERVAL * 60)


@app.route("/start", methods=[POST])
def start_cycle():
    global running, thread
    if not running:
        running = True
        thread = threading.Thread(target=run_cycle)
        thread.start()
        return jsonify({"status": "started"})
    return jsonify({"status": "already running"})


@app.route("/stop", methods=[POST])
def stop_cycle():
    global running
    running = False
    return jsonify({"status": "stopped"})


@app.route("/status")
def status():
    return jsonify({
        "running": running,
        "last_scrape_count": scrape_count,
        "last_summary": latest_summary[:500]  # Trim to avoid huge response
    })


@app.route("/top5")
def top5():
    try:
        res = supabase.table("stories").select("*").order("created_at", desc=True).limit(5).execute()
        return jsonify(res.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index():
    return "<h1>AI Newsletter Bot</h1><ul><li><a href='/status'>Status</a></li><li><a href='/top5'>Top 5 from Supabase</a></li></ul>"


if __name__ == "__main__":
    app.run(debug=True)
