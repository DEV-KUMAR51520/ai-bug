import pandas as pd

from agents.parser_agent import ParserAgent
from agents.validator_agent import ValidatorAgent
from agents.explainer_agent import ExplainerAgent


class Orchestrator:
    """Orchestrates the 3-agent pipeline for each row of the dataset."""

    def __init__(self):
        self.parser = ParserAgent()
        self.validator = ValidatorAgent()
        self.explainer = ExplainerAgent()

    def process_dataset(self, input_csv: str, output_csv: str):
        """
        Loads the dataset, processes each row through the agents, and saves the output.
        """
        print(f"Loading dataset from: {input_csv}")
        try:
            df = pd.read_csv(input_csv)
        except Exception as e:
            print(f"Failed to load dataset: {e}")
            return

        results = []
        total_rows = len(df)

        for index, row in df.iterrows():
            row_id = row.get("ID", index)
            code = str(row.get("Code", ""))
            context = str(row.get("Context", ""))
            
            print(f"\nProcessing row {index + 1}/{total_rows} (ID: {row_id})...")

            # 1. Parser Agent -> find buggy line
            buggy_line = self.parser.find_buggy_line(code)
            print(f"  [Parser] Found buggy line: {buggy_line}")

            # 2. Validator Agent -> fetch relevant MCP docs based on Context
            mcp_docs = self.validator.retrieve_context(context)
            print(f"  [Validator] Retrieved {len(mcp_docs)} documents from knowledge base.")

            # 3. Explainer Agent -> generate explanation using Code, Buggy Line, and MCP Docs
            explanation = self.explainer.generate_explanation(code, buggy_line, mcp_docs)
            print(f"  [Explainer] Explanation generated.")

            results.append({
                "ID": row_id,
                "Bug Line": buggy_line,
                "Explanation": explanation
            })

        # Save to output CSV
        print(f"\nSaving results to {output_csv}...")
        out_df = pd.DataFrame(results)
        out_df.to_csv(output_csv, index=False)
        print("Done!")

    def process_single(self, code: str, context: str) -> dict:
        """
        Processes a single snippet of code and context through the agents.
        Returns a dictionary containing the bug line and explanation.
        """
        print("Processing single request...")

        # 1. Parser Agent -> find buggy line
        buggy_line = self.parser.find_buggy_line(code)
        print(f"  [Parser] Found buggy line: {buggy_line}")

        # 2. Validator Agent -> fetch relevant MCP docs based on Context
        mcp_docs = self.validator.retrieve_context(context)
        print(f"  [Validator] Retrieved {len(mcp_docs)} documents from knowledge base.")

        # 3. Explainer Agent -> generate explanation using Code, Buggy Line, and MCP Docs
        explanation = self.explainer.generate_explanation(code, buggy_line, mcp_docs)
        print(f"  [Explainer] Explanation generated.")

        return {
            "bug_line": buggy_line,
            "explanation": explanation
        }
