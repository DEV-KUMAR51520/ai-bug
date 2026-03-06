from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL


class ExplainerAgent:
    """Agent responsible for generating the final bug explanation."""

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate_explanation(self, code: str, buggy_line: str, mcp_docs: list) -> str:
        """
        Generates an explanation of the bug.

        Args:
            code (str): The original buggy code.
            buggy_line (str): The list of line numbers identified by the Parser.
            mcp_docs (list): Documents retrieved by Validator from the MCP knowledge base.

        Returns:
            str: Generated explanation.
        """
        docs_text = "\n---\n".join([doc.get("text", str(doc)) for doc in mcp_docs])
        if not docs_text:
            docs_text = "No additional relevant documentation accessed."
        else:
            docs_text = docs_text[:3000]  # Prevent token limit exhaustion

        prompt = f"""
You are an expert code reviewer and debugger. I need you to explain a bug in the provided C++ code.

Code:
{code}

Suspicious Lines Identified (1-indexed): {buggy_line if buggy_line not in ("-1", "", " ") else 'Unknown'}

Relevant Knowledge Base Documentation:
{docs_text}

Provide an extremely short, single-phrase explanation of the bug. Focus ONLY on exactly what changed or what is wrong (e.g. "RDI_begin() changed to RDI_END()"). Limit your response to 1 short sentence or phrase. Do NOT provide long explanations.
        """

        try:
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return response.choices[0].message.content.strip().replace("\n", " ").replace(",", ";")
        except Exception as e:
            print(f"[ExplainerAgent] Error: {e}")
            return "Failed to generate explanation."
