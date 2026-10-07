import sys
from pathlib import Path
from mcp.server import MCPServer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from registry import get_alert, search_policy, flag_alert  # Day 4's tools, unchanged

mcp = MCPServer("fincrime-tools")
mcp.tool()(get_alert)  # schema from the same type hints + docstring
mcp.tool()(search_policy)
mcp.tool()(flag_alert)

if __name__ == "__main__":
    mcp.run(
        transport="stdio"
    )  # stdio: never print() to stdout in a server, it corrupts the protocol
