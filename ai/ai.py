import os
from textwrap import dedent
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
client = OpenAI(api_key=OPENAI_API_KEY)



async def generate_questions(num_questions: int) -> list[str]:
    """
    Generate {num_questions} psychological evaluation questions using OpenAI.
    """
    system_prompt = dedent(
        """
        You are a helpful assistant that generates psychological evaluation questions for a fun Discord Survivor
        ORG game. The questions should be thought-provoking and suitable for a general audience.
        Please follow Discord content guidelines and avoid sensitive topics.

        These questions should be light-hearted and silly, suitable for a fun game environment.
        """
    ).strip()

    user_prompt = f"Generate {num_questions} psychological evaluation questions."

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )

    if response and response.choices:
        content = response.choices[0].message.content
        questions = [q.strip() for q in content.split("\n") if q.strip()]
        return questions
    return []



