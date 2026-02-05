from datetime import datetime
from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("my_server")

@mcp.tool()
def get_date_time() -> str:
    """Get the current date and time."""
    return datetime.now().isoformat()

if __name__ == "__main__":
    # Get the MCP ASGI app and run it directly with uvicorn
    app = mcp.streamable_http_app()
    
    # Run with uvicorn on the desired port
    uvicorn.run(app, host="0.0.0.0", port=8173)