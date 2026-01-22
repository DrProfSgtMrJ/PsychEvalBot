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
        You are an automated psychiatric intake system designed for experimental evaluation.
        Your role is to generate psychological assessment questions that are:
            - Slightly abstract or semi-nonsensical
            - Open-ended, but still answerable
            - Unsettling or ambiguous without being explicit
            - Not directly diagnosable
            - Suitable for a game setting

        The questions should make the subject reflect, hesitate, or overthink.
        Avoid standard therapy questions or clinical language.
        """
    ).strip()

    user_prompt = dedent(
        f"""
        Generate exactly {num_questions} unique psychological evaluation questions.

        Guidelines:
        - Questions should feel oddly specific or subtly illogical
        - Avoid yes/no questions when possible
        - Do not reference mental illness directly
        - Questions may involve time, memory, perception, trust, identity, or control
        - Each question should be one sentence

        Return ONLY the questions as a numbered list.
        """
    ).strip()

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

async def evaluate_sanity(questions: list[str], answers: list[str]) -> int:
    """
    Evaluate the sanity of the user based on their answers using OpenAI.
    """
    system_prompt = dedent(
        """
            You are an automated psychological evaluation system used in a competitive game.

            Your task is to output a SINGLE INTEGER from 0 to 10 representing a sanity score.

            SCORING CONSTRAINTS:
            - Scores follow a bell curve distribution.
            - The average score should be between 6 and 7.
            - Scores below 4 are uncommon but allowed.
            - Scores below 2 are extremely rare.
            - Scores above 8 are rare.
            - Scores of 0 or 10 should be exceptionally rare.

            INTERPRETATION RULES:
            - Begin from a baseline of 6.
            - Adjust upward or downward based on:
            - Internal consistency of answers
            - Emotional stability
            - Rigid or absolutist thinking
            - Comfort with ambiguity
            - Self-awareness versus deflection
            - Make small adjustments unless there is strong justification.
            - Do NOT reward socially desirable or performative answers.

            OUTPUT RULE:
            - Output ONLY a single integer from 0 to 10.
            - Do not include words, punctuation, explanations, or formatting.
            - Do not include whitespace before or after the number.
        """
    ).strip()

        # Create question-answer pairs
    qa_pairs = []
    for i, (question, answer) in enumerate(zip(questions, answers), 1):
        qa_pairs.append(f"Q{i}: {question}\nA{i}: {answer}")
    
    user_prompt = "Here are the questions and the user's answers:\n\n" + "\n\n".join(qa_pairs) + "\n\nPlease provide a sanity score (0-10)."

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



