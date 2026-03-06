"""
MCP Client — connects to the FastMCP server via SSE and wraps the search_documents tool using the official mcp library.
"""

import asyncio
import json
from mcp.client.sse import sse_client
from mcp import ClientSession


class MCPClient:
    """Client that connects to the MCP server and calls search_documents."""

    def __init__(self, server_url: str):
        """
        Args:
            server_url: The SSE endpoint URL of the MCP server (e.g. http://localhost:8003/sse)
        """
        self.server_url = server_url

    async def _search_async(self, query: str) -> list:
        try:
            async with sse_client(self.server_url) as streams:
                # sse_client might return a tuple or dict depending on version, commonly (read_stream, write_stream)
                if isinstance(streams, tuple):
                    read_stream, write_stream = streams
                else:
                    read_stream, write_stream = streams[0], streams[1]

                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("search_documents", arguments={"query": query})
                    
                    if result and hasattr(result, "content") and result.content:
                        for item in result.content:
                            if item.type == "text":
                                try:
                                    # result might be JSON stringified list of dicts
                                    return json.loads(item.text)
                                except (json.JSONDecodeError, TypeError):
                                    return [{"text": item.text, "score": 1.0}]
            return []
        except Exception as e:
            print(f"[MCP Client] Async Error: {e}")
            return []

    def search_documents(self, query: str) -> list:
        """
        Search documents using the MCP server's vector similarity retrieval.

        Args:
            query: The search query string.

        Returns:
            List of dicts with 'text' and 'score' keys.
        """
        try:
            # Use asyncio.run to execute the async task in a sync context
            return asyncio.run(self._search_async(query))
        except Exception as e:
            print(f"[MCP Client] Error calling search_documents: {e}")
            return []
