# MCP Config Helper

A Model Context Protocol (MCP) server that fetches and transforms MCP configurations into ready-to-use Claude CLI commands.

## Features

- 🚀 Fetch MCP configurations from any URL
- 🔄 Transform configs into `claude mcp add-json` commands
- 📋 List popular MCP servers with pre-configured commands
- ⚡ Simple and fast implementation

## Installation

### Using uvx (Python)
```bash
uvx mcp-config-helper
```

### Using npx (Node.js)
```bash
npx mcp-config-helper
```

### From source
```bash
git clone https://github.com/Iron5pider/get-mcp-cli
cd get-mcp-cli
pip install -e .
```

## Configuration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "config-helper": {
      "command": "uvx",
      "args": ["mcp-config-helper"]
    }
  }
}
```

## Usage

Once configured, you can use these tools in Claude:

### Fetch and transform a configuration
```
get_claude_add_mcp("https://example.com/mcp-config.json")
```

This will return ready-to-use CLI commands like:
```bash
claude mcp add-json server-name '{"command":"npx","args":["-y","@org/server-package"]}'
```

### List popular servers
```
list_popular_servers()
```

Returns a curated list of commonly used MCP servers with their installation commands.

## Example Configuration

Your MCP configuration JSON should follow this format:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## Tools

### `get_claude_add_mcp`
- **Input**: URL to MCP configuration JSON
- **Output**: List of `claude mcp add-json` commands ready to execute

### `list_popular_servers`
- **Input**: None
- **Output**: List of popular MCP servers with installation commands

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Armaan Sood