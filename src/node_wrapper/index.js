#!/usr/bin/env node

const { spawn } = require('child_process');

// Use uvx to run the Python package
const main = () => {
  const uvx = spawn('uvx', ['mcp-config-helper'], {
    stdio: 'inherit',
    env: { ...process.env }
  });
  
  uvx.on('error', (err) => {
    if (err.code === 'ENOENT') {
      console.error('Error: uvx command not found.');
      console.error('Please install uv: https://docs.astral.sh/uv/');
      console.error('Or use the Python package directly: uvx mcp-config-helper');
    } else {
      console.error('Failed to start MCP server:', err.message);
    }
    process.exit(1);
  });
  
  uvx.on('close', (code) => {
    process.exit(code || 0);
  });
  
  // Handle graceful shutdown
  process.on('SIGINT', () => {
    uvx.kill('SIGINT');
  });
  
  process.on('SIGTERM', () => {
    uvx.kill('SIGTERM');
  });
};

main();