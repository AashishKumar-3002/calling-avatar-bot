import anthropic

from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def repharse_question_claude(question):
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model="claude-instant-1.2",
        system="Given a question your task is to rephrase the question keeping the meaning same. Keep it short and precise. if the meaning is clear do not change it, return as it is. Don't give answer to the question", # <-- system prompt
        max_tokens=100,
        messages=[
          {"role": "user", "content": question}
        ],
    )

    rephrased_question = response.content[0].text
    return rephrased_question

if __name__ == '__main__':
    question = "What is the capital of France?"
    resp = repharse_question_claude(question)
    print(resp)