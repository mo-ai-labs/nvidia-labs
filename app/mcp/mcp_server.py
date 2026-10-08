from mcp.server import MCPServer

# Day 4's tools, unchanged
from app.tools.registry import get_alert, search_policy, flag_alert

mcp = MCPServer("fincrime-tools")
mcp.tool()(get_alert)  # schema from the same type hints + docstring
mcp.tool()(search_policy)
mcp.tool()(flag_alert)

if __name__ == "__main__":
    mcp.run(
        transport="stdio"
    )  # stdio: never print() to stdout in a server, it corrupts the protocol
