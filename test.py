# test.py
import main

def test_scraping():
    print("🔍 Testing: Fetch Stories")
    stories = main.fetch_stories()
    print(f"✅ {len(stories)} stories fetched.")
    for story in stories[:5]:
        print(f"• {story['title']} ({story['url']})")
    return stories

def test_supabase(stories):
    print("💾 Testing: Supabase Insertion")
    main.save_to_supabase(stories[:3])  # Insert only top 3 for testing

def test_summary(stories):
    print("🧠 Testing: Newsletter Summarization")
    summary = main.generate_newsletter(stories[:5])
    print("📄 Generated Summary:")
    print(summary)

def test_email(summary):
    print("✉️ Testing: Mailjet Email Sending")
    main.send_newsletter(summary)

if __name__ == "__main__":
    # 1. Test scraping
    stories = test_scraping()

    # 2. Test database insert
    test_supabase(stories)

    # 3. Test summarization
    summary = main.generate_newsletter(stories[:5])

    # 4. Test email
    test_email(summary)

    print("✅ All tests completed.")
