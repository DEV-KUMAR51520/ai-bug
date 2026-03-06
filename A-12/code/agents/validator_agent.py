from tools.mcp_client import MCPClient
from config import MCP_SERVER_URL


class ValidatorAgent:
    """Agent responsible for cross-referencing bug context with the knowledge base via MCP."""

    def __init__(self):
        self.mcp_client = MCPClient(MCP_SERVER_URL)

    def retrieve_context(self, search_query: str) -> list:
        """
        Calls the search_documents tool on the MCP server to get documentation.

        Args:
            search_query (str): The context string or query provided in the dataset.

        Returns:
            list: Retrieved documents from LlamaIndex via the MCP server.
        """
        if not search_query or str(search_query) == "nan":
            return []

        print(f"[ValidatorAgent] Querying MCP server for: '{search_query[:50]}...'")
        docs = self.mcp_client.search_documents(search_query)
        return docs
