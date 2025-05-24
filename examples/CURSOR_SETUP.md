# Google ADK MCP Server - Cursor Integration Guide

This guide shows how to integrate the Google ADK MCP Server with Cursor IDE to enable AI agent capabilities directly in your code editor.

## Prerequisites

1. **Cursor IDE installed** - Download from [cursor.sh](https://cursor.sh)
2. **Google ADK MCP Server set up** - Follow the main [README.md](../README.md) setup instructions
3. **Google Cloud credentials configured** - Required for agent execution

## Configuration

### Step 1: Locate Cursor Configuration

Cursor stores its MCP configuration in different locations depending on your operating system:

- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/cursor.mcp/settings.json`
- **Linux**: `~/.config/Cursor/User/globalStorage/cursor.mcp/settings.json`  
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\cursor.mcp\settings.json`

### Step 2: Create MCP Configuration

Create or edit the MCP configuration file with the following content:

#### Option 1: With Service Account (Recommended)

```json
{
  "mcpServers": {
    "google-adk": {
      "command": "python",
      "args": ["/absolute/path/to/google-adk-mcp-server/mcp_server.py"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your/service-account-key.json",
        "GOOGLE_CLOUD_PROJECT": "your-project-id",
        "GOOGLE_CLOUD_LOCATION": "us-central1"
      }
    }
  }
}
```

#### Option 2: With Google AI API Key (Simpler)

```json
{
  "mcpServers": {
    "google-adk": {
      "command": "python",
      "args": ["/absolute/path/to/google-adk-mcp-server/mcp_server.py"],
      "env": {
        "GOOGLE_AI_API_KEY": "your-google-ai-api-key"
      }
    }
  }
}
```

#### Option 3: Using System Environment (If already configured)

```json
{
  "mcpServers": {
    "google-adk": {
      "command": "python",
      "args": ["/absolute/path/to/google-adk-mcp-server/mcp_server.py"]
    }
  }
}
```

### Step 3: Update Paths

Replace the placeholder paths with your actual paths:

1. **Server path**: Replace `/absolute/path/to/google-adk-mcp-server/mcp_server.py` with the full path to your server
2. **Service account key**: Replace `/path/to/your/service-account-key.json` with your actual key path
3. **Project ID**: Replace `your-project-id` with your Google Cloud project ID

#### Finding Your Server Path

```bash
# Navigate to your server directory
cd /path/to/google-adk-mcp-server

# Get the absolute path
pwd
# Example output: /Users/username/Documents/google-adk-mcp-server

# Your full server path would be:
# /Users/username/Documents/google-adk-mcp-server/mcp_server.py
```

### Step 4: Verify Python Command

Make sure the `python` command in the configuration points to the correct Python installation:

```bash
# Check which Python Cursor should use
which python
# or
which python3

# Verify it's 3.10+ and has the required packages
python --version
python -c "import google.adk; import mcp; print('✅ Ready!')"
```

If you need to use a specific Python path:

```json
{
  "mcpServers": {
    "google-adk": {
      "command": "/usr/local/bin/python3.11",
      "args": ["/absolute/path/to/google-adk-mcp-server/mcp_server.py"],
      "env": {
        "GOOGLE_AI_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Testing the Integration

### Step 1: Restart Cursor

After updating the configuration, restart Cursor completely to load the new MCP server.

### Step 2: Verify Connection

1. Open Cursor
2. Open the command palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux)
3. Look for MCP-related commands or check if Google ADK tools are available

### Step 3: Test Agent Creation

Try creating a simple agent through Cursor's chat interface:

```
Can you create a Google ADK agent named "code_assistant" that helps with code review and can search the web for programming best practices?
```

If the integration is working, Cursor should be able to:
- Create ADK agents
- Run agents with your questions  
- Use Google Search and web scraping tools
- Help with multi-agent systems

## Example Usage in Cursor

Once configured, you can use the Google ADK MCP server directly in Cursor:

### Code Review Assistant

```
Create an ADK agent called "code_reviewer" that:
1. Reviews code for best practices
2. Can search for current coding standards
3. Provides specific improvement suggestions

Then use it to review this Python function: [paste your code]
```

### Research Assistant

```
Create a research agent that can help me understand this new technology. Have it search for:
1. Latest documentation
2. Best practices 
3. Common implementation patterns

Topic: [your technology/framework]
```

### Multi-Agent Development Team

```
Set up a multi-agent system with:
1. A coordinator that manages development tasks
2. A code reviewer agent
3. A documentation writer agent  
4. A testing specialist agent

Use this system to help me build a new feature for my project.
```

## Troubleshooting

### Common Issues

#### 1. "MCP Server Not Found"

**Problem**: Cursor can't locate the MCP server

**Solutions**:
- Verify the absolute path to `mcp_server.py` is correct
- Check that the Python command is accessible from Cursor's environment
- Ensure the virtual environment is properly configured

#### 2. "Google ADK Tools Not Available"

**Problem**: MCP server starts but Google ADK features don't work

**Solutions**:
- Check Google Cloud credentials are properly set in the environment variables
- Verify the credentials have the necessary permissions
- Test credentials outside Cursor: `python -c "from google.adk.agents import LlmAgent; print('OK')"`

#### 3. "Python Version Issues"

**Problem**: Import errors or version conflicts

**Solutions**:
- Ensure Python 3.10+ is being used
- Use the full path to your Python installation in the config
- Check that all dependencies are installed in the correct environment

#### 4. "Permission Denied"

**Problem**: Cursor can't execute the Python script

**Solutions**:
- Make the script executable: `chmod +x mcp_server.py`
- Check file permissions on the server directory
- On Windows, ensure Python is in your PATH

### Debug Mode

Enable debug logging by modifying your configuration:

```json
{
  "mcpServers": {
    "google-adk": {
      "command": "python",
      "args": ["-u", "/absolute/path/to/google-adk-mcp-server/mcp_server.py", "--debug"],
      "env": {
        "GOOGLE_AI_API_KEY": "your-api-key",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Testing Without Cursor

Test the MCP server independently to isolate issues:

```bash
# Test server startup
python mcp_server.py

# Test with the test client
python examples/test_mcp_client.py

# Simple functionality test
python simple_test.py
```

## Advanced Configuration

### Multiple Environments

You can configure different MCP servers for different environments:

```json
{
  "mcpServers": {
    "google-adk-dev": {
      "command": "python",
      "args": ["/path/to/dev/google-adk-mcp-server/mcp_server.py"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "my-dev-project"
      }
    },
    "google-adk-prod": {
      "command": "python", 
      "args": ["/path/to/prod/google-adk-mcp-server/mcp_server.py"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "my-prod-project"
      }
    }
  }
}
```

### Custom Agent Templates

Create predefined agents for common development tasks by adding initialization scripts.

### Integration with Cursor Rules

You can create Cursor rules that automatically suggest using Google ADK agents for specific types of questions or tasks.

## Benefits in Cursor

With Google ADK MCP integration, Cursor gains:

1. **Intelligent Code Review** - AI agents that understand your codebase and current best practices
2. **Research Assistance** - Agents that can search for and analyze the latest documentation
3. **Multi-Agent Workflows** - Coordinate multiple AI specialists for complex development tasks
4. **Web-Connected AI** - Access to real-time information and current technology trends
5. **Custom Agent Creation** - Build specialized agents for your specific development needs

## Next Steps

1. **Explore Agent Templates** - Check the [USAGE.md](../USAGE.md) for pre-built agent examples
2. **Build Custom Workflows** - Create multi-agent systems for your development process
3. **Integrate with CI/CD** - Use ADK agents in your automated development pipelines
4. **Share Configurations** - Export and share successful agent configurations with your team

---

For more examples and advanced usage, see the main [README.md](../README.md) and [USAGE.md](../USAGE.md) files. 