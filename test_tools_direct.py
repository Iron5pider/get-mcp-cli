#!/usr/bin/env python3
"""Test the MCP tools directly"""

import asyncio
from src.mcp_config_helper.server import get_claude_add_mcp, list_popular_servers

async def main():
    print("Testing MCP Config Helper Tools\n")
    
    # Test 1: List popular servers
    print("1. Testing list_popular_servers:")
    result = await list_popular_servers.fn()
    print(f"   Found {result['count']} servers")
    for server in result['servers']:
        print(f"   - {server['name']}: {server['description']}")
    
    # Test 2: Test with example config
    print("\n2. Testing get_claude_add_mcp:")
    file_url = "file:///Users/ironspidermini/PKMS/projects/active/get-mcp-cli/example_config.json"
    result = await get_claude_add_mcp.fn(url=file_url)
    
    if result.get("error"):
        print(f"   Error: {result['error']}")
    else:
        print(f"   Generated {result['count']} commands from {result['source']}:")
        for i, cmd in enumerate(result['commands'], 1):
            print(f"   {i}. {cmd}")
        print(f"   Servers found: {', '.join(result['server_names'])}")
    
    # Test 3: Test error handling
    print("\n3. Testing error handling with bad URL:")
    result = await get_claude_add_mcp.fn(url="https://nonexistent-url-12345.com/config.json")
    print(f"   Expected error: {result.get('error', 'No error?')}")
    
    print("\n✅ All tests complete!")

if __name__ == "__main__":
    asyncio.run(main())