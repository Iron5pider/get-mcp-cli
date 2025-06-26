# MCP Config Helper - Node.js Wrapper

This is the Node.js wrapper for the MCP Config Helper Python server.

## Installation

```bash
npm install -g @iron5pider/mcp-config-helper
# or
npx @iron5pider/mcp-config-helper
```

## Requirements

- Node.js 14+
- uv (Python package manager) - [Installation guide](https://docs.astral.sh/uv/)

## How it works

This Node.js wrapper uses `uvx` to automatically download and run the Python mcp-config-helper package. No separate Python installation is needed as uvx handles everything.

## Usage

Simply run the command and uvx will handle the rest:

For more information, see the main [README](https://github.com/Iron5pider/get-mcp-cli).