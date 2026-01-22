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
        ORG game. The questions should be somewhat silly and nonsensical, suitable for light-hearted psychological evaluation.
        Please follow Discord content guidelines and avoid sensitive topics.
        
        I want the questions to not have a clear 'sane' answer. These questions will be used to evaluate the sanity of users
        based on their responses.
        
        An example could be:
         - Would you rather fight one horse-sized duck or a hundred duck-sized horses?
         - If you could only eat one food for the rest of your life, what would it be and why?
         - If you were a fruit, which fruit would you be and why?
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

async def evaluate_sanity(answers: list[str]) -> int:
    """
    Evaluate the sanity of the user based on their answers using OpenAI.
    """
    system_prompt = dedent(
        """
        You are a psychological evaluation assistant for a silly Discord game. Based on the user's answers,
        provide a sanity score from 0-10.

        IMPORTANT SCORING GUIDELINES:
        - 0-2: Completely nonsensical, incoherent, or disturbing responses
        - 3-4: Very bizarre or illogical answers with little coherence
        - 5-6: Quirky, weird, or silly answers but still somewhat understandable (THIS SHOULD BE THE AVERAGE)
        - 7-8: Creative but mostly logical responses
        - 9-10: Perfectly reasonable and boring answers (reserve for genuinely mundane responses)

        Remember: These questions are meant to be silly and have no "correct" answer. 
        Most people should score in the 4-7 range. Be critical and look for oddities, 
        inconsistencies, or overly creative responses. A "normal" person answering silly 
        questions should still sound a bit weird.

        The only output should be the integer score with no explanation.
        """
    ).strip()

    user_prompt = "Here are the user's answers:\n" + "\n".join(
        [f"Q{i+1}: {answer}" for i, answer in enumerate(answers)]
    ) + "\nPlease provide a brief evaluation of their sanity."

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=300,
        temperature=0.7,
    )

    if response and response.choices:
        return int(response.choices[0].message.content.strip())
    return "Could not evaluate sanity at this time."



