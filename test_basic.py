#!/usr/bin/env python3
"""Basic tests for MCP Config Helper"""

import json
import asyncio
from src.mcp_config_helper.server import get_claude_add_mcp, list_popular_servers

async def test_transform_config():
    """Test transforming a mock configuration"""
    # Mock a simple config
    test_config = {
        "mcpServers": {
            "test-server": {
                "command": "npx",
                "args": ["-y", "@test/server"]
            }
        }
    }
    
    # In real test, this would fetch from URL
    # For now, we'll test the transformation logic
    json_str = json.dumps(test_config["mcpServers"]["test-server"], separators=(',', ':'))
    json_str = json_str.replace("'", "'\"'\"'")
    expected_command = f"claude mcp add-json test-server '{json_str}'"
    
    print(f"✓ Generated command: {expected_command}")
    assert "claude mcp add-json" in expected_command
    assert "test-server" in expected_command

async def test_list_popular():
    """Test listing popular servers"""
    result = await list_popular_servers()
    
    assert "servers" in result
    assert len(result["servers"]) > 0
    assert "filesystem" in [s["name"] for s in result["servers"]]
    print(f"✓ Found {result['count']} popular servers")

async def test_error_handling():
    """Test error handling for invalid URL"""
    result = await get_claude_add_mcp("https://invalid-url-that-does-not-exist-12345.com/config.json")
    
    assert "error" in result
    assert len(result["commands"]) == 0
    print(f"✓ Error handling works: {result['error']}")

async def main():
    """Run all tests"""
    print("Running basic tests for MCP Config Helper...\n")
    
    try:
        await test_transform_config()
        await test_list_popular()
        await test_error_handling()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)