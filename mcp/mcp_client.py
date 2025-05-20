from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
import os
import sys
import dotenv
from langchain_core.messages import AIMessage

dotenv.load_dotenv()  # 🔑 Loads the .env file

async def main():
    # STEP 1: Create MCP client session with explicit Python executable
    python_executable = sys.executable
    script_path = os.path.join(os.getcwd(), "weather_server.py")
    
    server_params = StdioServerParameters(
        command=python_executable,
        args=[script_path]
    )
    
    try:
        # Use stdio_client as a context manager
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                
                # STEP 2: Load tools from MCP server
                tools = await load_mcp_tools(session)
                
                # STEP 3: Load the LLM
                llm = ChatOpenAI(model="gpt-4", temperature=0)
                
                # STEP 4: Build agent
                agent = create_react_agent(llm, tools)
                
                # STEP 5: Ask something using the correct message format!
                response = await agent.ainvoke({
                    "messages": [
                        {"role": "user", "content": "What's the weather in Mumbai?"}
                    ]
                })
                
                # Print the type and structure of the response to debug
                print("Response type:", type(response))
                
                # If it's a dictionary
                if isinstance(response, dict):
                    print("Keys in response:", response.keys())
                    if "messages" in response:
                        last_msg = response["messages"][-1]
                        print("Last message type:", type(last_msg))
                        print("Agent response (from messages):", last_msg.content)
                    elif "output" in response:
                        print("Agent response (from output):", response["output"])
                
                # If it's an AIMessage directly
                elif isinstance(response, AIMessage):
                    print("Agent response (direct message):", response.content)
                
                # As a fallback, just print the whole response
                else:
                    print("Full response:", response)
    
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())