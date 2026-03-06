import re
from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL


class ParserAgent:
    """Agent responsible for identifying the buggy line in C++ code."""

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def find_buggy_line(self, code: str) -> str:
        """
        Analyzes the code line-by-line and returns the buggy line number.
        """
        # Number the code lines to help the model
        numbered_code = "\n".join([f"{i+1}: {line}" for i, line in enumerate(code.split("\n"))])

        prompt = f"""
You are an expert C++ bug detector. I will provide you with C++ code where the lines are numbered.
Your task is to identify the suspicious or buggy lines.

Code:
{numbered_code}

Respond ONLY with a JSON list of integer line numbers, like [5] or [2, 5, 7]. Do not include any text, explanations, or formatting outside the list.
        """

        try:
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            text = response.choices[0].message.content.strip()
            
            # Extract the list format and remove brackets
            match = re.search(r'\[.*?\]', text)
            if match:
                return match.group().strip("[]")
            return "-1"
        except Exception as e:
            print(f"[ParserAgent] Error: {e}")
            return "-1"
