#!/usr/bin/env python3
"""MCP Config Helper - Transform MCP configurations into Claude CLI commands"""

from fastmcp import FastMCP
import httpx
import json
from typing import Dict, Any

# Initialize FastMCP server
mcp = FastMCP("mcp-config-helper")

@mcp.tool()
async def get_claude_add_mcp(url: str) -> Dict[str, Any]:
    """
    Fetch MCP server configuration from URL and transform to claude mcp add-json command.
    
    Args:
        url: URL pointing to MCP server configuration JSON
        
    Returns:
        Dict containing commands list, count, and source URL (or error)
    """
    try:
        # Fetch configuration from URL
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
        
        # Parse JSON configuration
        config = response.json()
        mcp_servers = config.get("mcpServers", {})
        
        if not mcp_servers:
            return {
                "error": "No mcpServers found in configuration",
                "commands": [],
                "source": url
            }
        
        # Generate commands for each server
        commands = []
        for name, server in mcp_servers.items():
            # Convert server config to JSON string
            json_str = json.dumps(server, separators=(',', ':'))
            # Escape single quotes for shell
            json_str = json_str.replace("'", "'\"'\"'")
            # Create command
            command = f"claude mcp add-json {name} '{json_str}'"
            commands.append(command)
        
        return {
            "commands": commands,
            "count": len(commands),
            "source": url,
            "server_names": list(mcp_servers.keys())
        }
        
    except httpx.HTTPError as e:
        return {
            "error": f"HTTP error: {str(e)}",
            "commands": [],
            "source": url
        }
    except json.JSONDecodeError as e:
        return {
            "error": f"Invalid JSON: {str(e)}",
            "commands": [],
            "source": url
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "commands": [],
            "source": url
        }

@mcp.tool()
async def list_popular_servers() -> Dict[str, Any]:
    """
    List popular MCP servers with pre-configured commands.
    
    Returns:
        Dict containing popular servers with their installation commands
    """
    popular_servers = [
        {
            "name": "filesystem",
            "description": "File system operations",
            "command": "claude mcp add-json filesystem '{\"command\":\"npx\",\"args\":[\"-y\",\"@modelcontextprotocol/server-filesystem\",\"/path/to/allowed/files\"]}'"
        },
        {
            "name": "github",
            "description": "GitHub API integration",
            "command": "claude mcp add-json github '{\"command\":\"npx\",\"args\":[\"-y\",\"@modelcontextprotocol/server-github\"],\"env\":{\"GITHUB_TOKEN\":\"${GITHUB_TOKEN}\"}}'"
        },
        {
            "name": "time",
            "description": "Time and timezone utilities",
            "command": "claude mcp add-json time '{\"command\":\"uvx\",\"args\":[\"mcp-server-time\"]}'"
        }
    ]
    
    return {
        "servers": popular_servers,
        "count": len(popular_servers),
        "note": "Remember to customize paths and tokens as needed"
    }

def main():
    """Entry point for the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()