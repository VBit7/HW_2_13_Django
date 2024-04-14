from openai import OpenAI
from django.conf import settings


# client = OpenAI(api_key=settings.OPEN_AI_KEY)
client = OpenAI(api_key=settings.OPEN_AI_KEY, base_url="https://api.deepseek.com/v1")


def ask_gpt(user_prompt: str) -> str:
    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a writer-journalist. Write a quote from a famous person."},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content


def generate_random_quote():
    print("Quote generator is started...")
    user_prompt = "Write a quote on behalf of Albert Einstein. The quote should be in English."
    quote = ask_gpt(user_prompt)
    print(quote)
