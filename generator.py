import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_content(stories):

    print(stories)
    return "Testing content generation with OpenAI API"

# def generate_content(stories):
#     joined = "\n".join(f"- {s}" for s in stories)
#     prompt = f"""
#     Write a professional AI newsletter highlighting the most important news. Use the following list:
#     {joined}
#     """
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content