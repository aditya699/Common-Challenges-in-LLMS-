from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    # In a real implementation, you would call a weather API here
    return f"It's sunny and 28°C in {location} today!"

if __name__ == "__main__":
    mcp.run(transport="stdio")