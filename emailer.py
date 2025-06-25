import os
from mailjet_rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_newsletter(content):
    mailjet = Client(
        auth=(os.getenv('MAILJET_API_KEY'), os.getenv('MAILJET_SECRET_KEY')),
        version='v3.1'  
    )

    recipients = os.getenv('MAILJET_RECIPIENTS').split(',')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.getenv('MAILJET_SENDER'),
                    "Name": "AI Newsletter Bot"
                },
                "To": [{"Email": email.strip(), "Name": "Subscriber"} for email in recipients],
                "Subject": "🧠 Today's AI Newsletter",
                "TextPart": content,
                "HTMLPart": f"<pre>{content}</pre>"
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print("Status:", result.status_code)
    print("Response:", result.json())
