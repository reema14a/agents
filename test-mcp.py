import asyncio
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

async def test_fetcher():
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    fetcher = await mcp_server_tools(fetch_mcp_server)
    result = await fetcher.run("Hello world")
    print("Result:", result)

asyncio.run(test_fetcher())
