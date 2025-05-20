# MCP
# Model Context Protocol (MCP) Project

## Overview

This project demonstrates the implementation of a simple MCP (Model Context Protocol) client-server architecture using LangChain and Python. MCP is a standardized interface designed to enable seamless interaction between AI agents and external tools, breaking down data silos and facilitating interoperability across diverse systems.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol introduced by Anthropic in late 2024 that standardizes how AI applications and agents communicate with external tools and resources. Inspired by the Language Server Protocol (LSP), MCP provides a flexible framework for AI agents to dynamically discover, select, and orchestrate tools based on context.

Key features of MCP:
- Standardized communication between AI agents and external tools
- Dynamic tool discovery and invocation
- Human-in-the-loop mechanisms for data injection or action approval
- Unified interfaces that simplify AI agent development
- Rich two-way interactions with external tools

## Project Structure

Our implementation consists of two main components:

1. **MCP Server (`weather_server.py`)**: Provides a simple weather information tool that can be accessed by the MCP client.
2. **MCP Client (`client1.py`)**: Connects to the MCP server, loads the available tools, and leverages an LLM agent to decide how to use them.

## How It Works

1. The client establishes a connection to the server via the stdio transport mechanism
2. The client loads the available tools from the server
3. The client creates a React agent using an LLM (GPT-4)
4. The agent accepts user queries and determines when to use the available tools
5. When appropriate, the agent invokes the weather tool to get data and returns results to the user

## Implementation Details

### MCP Server (weather_server.py)
