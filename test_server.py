#!/usr/bin/env python3
"""Test the MCP server tools directly"""

import asyncio
import json
from src.mcp_config_helper.server import mcp

async def test_server():
    """Test server functionality"""
    print("Testing MCP Config Helper Server\n")
    
    # Test 1: List popular servers
    print("1. Testing list_popular_servers:")
    # Get the tool
    popular_tool = None
    for tool in mcp.list_tools():
        if tool.name == "list_popular_servers":
            popular_tool = tool
            break
    
    if popular_tool:
        result = await popular_tool.fn()
        print(f"   Found {result['count']} popular servers")
        for server in result['servers'][:2]:  # Show first 2
            print(f"   - {server['name']}: {server['description']}")
    
    # Test 2: Transform example config
    print("\n2. Testing get_claude_add_mcp with local file:")
    transform_tool = None
    for tool in mcp.list_tools():
        if tool.name == "get_claude_add_mcp":
            transform_tool = tool
            break
    
    if transform_tool:
        # Use file:// URL for example config
        file_url = f"file:///Users/ironspidermini/PKMS/projects/active/get-mcp-cli/example_config.json"
        result = await transform_tool.fn(url=file_url)
        
        if "error" in result and result["error"]:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Generated {result['count']} commands:")
            for cmd in result['commands']:
                print(f"   {cmd[:80]}...")  # Show first 80 chars
    
    print("\n✅ Server tests complete!")

if __name__ == "__main__":
    asyncio.run(test_server())