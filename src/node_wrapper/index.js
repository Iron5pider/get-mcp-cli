#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Check if Python is available
const checkPython = () => {
  return new Promise((resolve) => {
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    const check = spawn(pythonCmd, ['--version']);
    
    check.on('close', (code) => {
      resolve(code === 0 ? pythonCmd : null);
    });
    
    check.on('error', () => {
      resolve(null);
    });
  });
};

const main = async () => {
  const pythonCmd = await checkPython();
  
  if (!pythonCmd) {
    console.error('Error: Python 3 is required but not found.');
    console.error('Please install Python 3.10+ or use: uvx mcp-config-helper');
    process.exit(1);
  }
  
  // Run the Python MCP server
  const serverPath = path.join(__dirname, '..', 'mcp_config_helper', 'server.py');
  const python = spawn(pythonCmd, [serverPath], {
    stdio: 'inherit',
    env: { ...process.env }
  });
  
  python.on('error', (err) => {
    console.error('Failed to start MCP server:', err.message);
    process.exit(1);
  });
  
  python.on('close', (code) => {
    process.exit(code || 0);
  });
  
  // Handle graceful shutdown
  process.on('SIGINT', () => {
    python.kill('SIGINT');
  });
  
  process.on('SIGTERM', () => {
    python.kill('SIGTERM');
  });
};

main().catch((err) => {
  console.error('Unexpected error:', err);
  process.exit(1);
});