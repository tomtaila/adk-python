# Google ADK MCP Server Usage Guide

This guide provides comprehensive examples and use cases for the Google ADK MCP Server.

## Table of Contents

1. [Prerequisites & Setup](#prerequisites--setup)
2. [Getting Started](#getting-started)
3. [Basic Agent Operations](#basic-agent-operations)
4. [Multi-Agent Systems](#multi-agent-systems)
5. [Tool Integration](#tool-integration)
6. [Agent Evaluation](#agent-evaluation)
7. [Advanced Workflows](#advanced-workflows)
8. [Integration Examples](#integration-examples)
9. [Troubleshooting](#troubleshooting)

## Prerequisites & Setup

### Required Software

- **Python 3.10+** (tested with Python 3.11+)
- **Git** (for cloning repository)
- **Google Cloud credentials** (required for agent execution)

### Python Version Check & Upgrade

```bash
# Check your Python version
python --version

# If you need to upgrade (example for macOS with Homebrew):
brew install python@3.11

# For Ubuntu/Debian:
sudo apt-get install python3.11

# For Windows or other systems:
# Download from https://www.python.org/downloads/
```

### Google Cloud Credentials Setup (Required)

**Without proper credentials, agents cannot execute and you'll see errors like:**
```
Missing key inputs argument! To use the Google AI API, provide (`api_key`) arguments.
```

#### Option 1: Google AI API Key (Easiest)
1. Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Set environment variable:
   ```bash
   export GOOGLE_AI_API_KEY="your-api-key-here"
   
   # Make it persistent (add to ~/.bashrc or ~/.zshrc):
   echo 'export GOOGLE_AI_API_KEY="your-api-key-here"' >> ~/.bashrc
   ```

#### Option 2: Google Cloud Project (Full Features)
1. Set up a [Google Cloud Project](https://console.cloud.google.com/)
2. Enable required APIs (Vertex AI, etc.)
3. Create service account and download JSON key
4. Set environment variables:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_CLOUD_LOCATION="us-central1"
   ```

#### Option 3: gcloud CLI Authentication
```bash
# Install gcloud CLI if not already installed
# Then authenticate:
gcloud auth application-default login
gcloud config set project your-project-id
```

### Installation & Verification

```bash
# 1. Clone repository
git clone https://github.com/your-username/google-adk-mcp-server.git
cd google-adk-mcp-server

# 2. Run automated setup
chmod +x setup.sh
./setup.sh

# 3. Verify everything works
source venv/bin/activate
python simple_test.py

# Expected output:
# ✅ All tests passed! Google ADK MCP Server is ready to use.
```

### Troubleshooting Setup Issues

**Python version too old:**
```bash
# Error: MCP requires Python 3.10 or higher
# Solution: Install Python 3.11+ (see above)
```

**Missing dependencies:**
```bash
# Error: ModuleNotFoundError
# Solution: Ensure you're in the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

**Google credentials not working:**
```bash
# Test your credentials:
python -c "
from google.adk.agents import LlmAgent
try:
    agent = LlmAgent(name='test', model='gemini-2.0-flash', instruction='Hello')
    print('✅ Credentials working!')
except Exception as e:
    print(f'❌ Credential error: {e}')
"
```

## Getting Started

### Quick Start

1. **Install dependencies**:
   ```bash
   ./setup.sh
   ```

2. **Start the MCP server**:
   ```bash
   python3 mcp_server.py
   ```

3. **Test the server**:
   ```bash
   python3 examples/test_mcp_client.py
   ```

### Claude Desktop Integration

1. **Configure Claude Desktop**:
   Edit your `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "google-adk": {
         "command": "python3",
         "args": ["/absolute/path/to/google-adk-mcp-server/mcp_server.py"]
       }
     }
   }
   ```

2. **Restart Claude Desktop** and start using ADK features!

## Basic Agent Operations

### Creating Your First Agent

```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "my_assistant",
    "instruction": "You are a helpful AI assistant that can search the web and analyze information.",
    "description": "General purpose AI assistant",
    "model": "gemini-2.0-flash",
    "tools": ["google_search", "load_web_page"]
  }
}
```

**Expected Response**:
```json
{
  "status": "success",
  "message": "Successfully created agent 'my_assistant'",
  "agent": {
    "name": "my_assistant",
    "model": "gemini-2.0-flash",
    "description": "General purpose AI assistant",
    "tools_count": 2
  }
}
```

### Running an Agent

```json
{
  "tool": "run_adk_agent",
  "arguments": {
    "agent_name": "my_assistant",
    "message": "What are the latest developments in artificial intelligence?",
    "session_id": "user_session_1"
  }
}
```

### Listing All Agents

```json
{
  "tool": "list_adk_agents",
  "arguments": {}
}
```

### Getting Agent Information

```json
{
  "tool": "get_adk_agent_info",
  "arguments": {
    "agent_name": "my_assistant"
  }
}
```

## Multi-Agent Systems

### Creating Specialized Agents

First, create individual specialist agents:

#### Customer Support FAQ Agent
```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "faq_specialist",
    "instruction": "You are an FAQ specialist who answers common questions about products, services, policies, and procedures. Always provide clear, accurate answers based on available information.",
    "description": "Handles frequently asked questions",
    "model": "gemini-2.0-flash"
  }
}
```

#### Technical Support Agent
```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "tech_support",
    "instruction": "You are a technical support specialist who helps users troubleshoot technical issues, software problems, and provides step-by-step solutions.",
    "description": "Provides technical troubleshooting support",
    "model": "gemini-2.0-flash",
    "tools": ["google_search"]
  }
}
```

#### Sales Information Agent
```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "sales_info",
    "instruction": "You are a sales information specialist who provides details about products, pricing, features, and helps customers make informed purchasing decisions.",
    "description": "Provides sales and product information",
    "model": "gemini-2.0-flash",
    "tools": ["google_search", "load_web_page"]
  }
}
```

### Creating the Coordinator

```json
{
  "tool": "create_multi_agent_system",
  "arguments": {
    "coordinator_name": "customer_service_coordinator",
    "coordinator_instruction": "You are a customer service coordinator who routes customer inquiries to the appropriate specialist agent. Analyze the customer's request and determine whether it should go to: FAQ specialist (for general questions), Technical support (for technical issues), or Sales info (for product/pricing questions). Always explain your routing decision.",
    "sub_agents": ["faq_specialist", "tech_support", "sales_info"],
    "model": "gemini-2.0-flash"
  }
}
```

### Testing the Multi-Agent System

```json
{
  "tool": "run_adk_agent",
  "arguments": {
    "agent_name": "customer_service_coordinator", 
    "message": "I'm having trouble connecting to WiFi on my laptop. Can you help?",
    "session_id": "support_session_1"
  }
}
```

## Tool Integration

### Available Built-in Tools

```json
{
  "tool": "list_available_tools",
  "arguments": {}
}
```

### Adding External MCP Tools

#### File System Tools
```json
{
  "tool": "add_mcp_tools_to_agent",
  "arguments": {
    "agent_name": "my_assistant",
    "mcp_server_command": "npx",
    "mcp_server_args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"],
    "tool_filter": ["read_file", "list_directory", "write_file"]
  }
}
```

#### Database Tools
```json
{
  "tool": "add_mcp_tools_to_agent", 
  "arguments": {
    "agent_name": "data_analyst",
    "mcp_server_command": "python",
    "mcp_server_args": ["/path/to/database-mcp-server.py"],
    "tool_filter": ["query_database", "list_tables"]
  }
}
```

### Direct Tool Usage

#### Web Search
```json
{
  "tool": "search_web",
  "arguments": {
    "query": "Google Agent Development Kit latest features",
    "num_results": 5
  }
}
```

#### Web Page Loading
```json
{
  "tool": "load_webpage_content",
  "arguments": {
    "url": "https://google.github.io/adk-docs/"
  }
}
```

## Agent Evaluation

### Simple Evaluation

```json
{
  "tool": "evaluate_adk_agent",
  "arguments": {
    "agent_name": "my_assistant",
    "test_cases": [
      {
        "input": "What is machine learning?",
        "expected_output": "machine learning"
      },
      {
        "input": "Explain artificial intelligence",
        "expected_output": "artificial intelligence"
      },
      {
        "input": "How do neural networks work?",
        "expected_output": "neural networks"
      }
    ]
  }
}
```

### Comprehensive Evaluation for Technical Support

```json
{
  "tool": "evaluate_adk_agent",
  "arguments": {
    "agent_name": "tech_support",
    "test_cases": [
      {
        "input": "My computer won't start up",
        "expected_output": "troubleshoot"
      },
      {
        "input": "WiFi connection keeps dropping",
        "expected_output": "connection"
      },
      {
        "input": "Software installation failed",
        "expected_output": "installation"
      },
      {
        "input": "Blue screen error on Windows",
        "expected_output": "error"
      },
      {
        "input": "Email not syncing properly",
        "expected_output": "sync"
      }
    ]
  }
}
```

## Advanced Workflows

### Research Assistant Workflow

1. **Create a research specialist**:
   ```json
   {
     "tool": "create_adk_agent",
     "arguments": {
       "name": "research_specialist",
       "instruction": "You are a research specialist who conducts thorough research on topics by searching the web, analyzing multiple sources, and providing comprehensive summaries with citations.",
       "description": "Comprehensive research and analysis agent",
       "model": "gemini-2.0-flash",
       "tools": ["google_search", "load_web_page"]
     }
   }
   ```

2. **Conduct research**:
   ```json
   {
     "tool": "run_adk_agent",
     "arguments": {
       "agent_name": "research_specialist",
       "message": "Research the current state of quantum computing and its potential applications in cybersecurity. Please provide a comprehensive analysis with sources.",
       "session_id": "research_session"
     }
   }
   ```

### Content Creation Workflow

1. **Create content agents**:
   ```json
   {
     "tool": "create_adk_agent",
     "arguments": {
       "name": "content_researcher",
       "instruction": "You research topics thoroughly to gather accurate, up-to-date information for content creation.",
       "model": "gemini-2.0-flash",
       "tools": ["google_search", "load_web_page"]
     }
   }
   ```

   ```json
   {
     "tool": "create_adk_agent",
     "arguments": {
       "name": "content_writer",
       "instruction": "You create engaging, well-structured content based on research provided. You focus on clarity, engagement, and proper formatting.",
       "model": "gemini-2.0-flash"
     }
   }
   ```

2. **Create coordinator**:
   ```json
   {
     "tool": "create_multi_agent_system",
     "arguments": {
       "coordinator_name": "content_creation_coordinator",
       "coordinator_instruction": "You coordinate content creation by first having the researcher gather information, then having the writer create content based on that research.",
       "sub_agents": ["content_researcher", "content_writer"],
       "model": "gemini-2.0-flash"
     }
   }
   ```

## Integration Examples

### Python Application Integration

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def create_and_run_agent():
    server_params = StdioServerParameters(
        command="python3",
        args=["./mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Create agent
            create_result = await session.call_tool("create_adk_agent", {
                "name": "python_assistant",
                "instruction": "You help with Python programming questions and can search for solutions online.",
                "tools": ["google_search"],
                "model": "gemini-2.0-flash"
            })
            
            # Use agent
            response = await session.call_tool("run_adk_agent", {
                "agent_name": "python_assistant",
                "message": "How do I handle exceptions in Python?"
            })
            
            return response

# Run the example
result = asyncio.run(create_and_run_agent())
print(result)
```

### Web Application Integration

```javascript
// Example Node.js/Express integration
const { Client } = require('@modelcontextprotocol/client');

async function setupADKAgent() {
    const client = new Client({
        command: 'python3',
        args: ['./mcp_server.py']
    });
    
    await client.connect();
    
    // Create an agent for the web app
    const result = await client.callTool('create_adk_agent', {
        name: 'web_assistant',
        instruction: 'You help users with web development questions and can search for current best practices.',
        tools: ['google_search', 'load_web_page'],
        model: 'gemini-2.0-flash'
    });
    
    return client;
}
```

## Use Case Examples

### E-commerce Customer Service

```json
{
  "tool": "create_multi_agent_system",
  "arguments": {
    "coordinator_name": "ecommerce_support",
    "coordinator_instruction": "You handle e-commerce customer inquiries by routing them to the appropriate specialist: order_support for order issues, product_info for product questions, or returns_support for return/refund requests.",
    "sub_agents": ["order_support", "product_info", "returns_support"],
    "model": "gemini-2.0-flash"
  }
}
```

### Educational Assistant

```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "math_tutor",
    "instruction": "You are a patient math tutor who explains concepts clearly, provides step-by-step solutions, and can search for additional resources when needed.",
    "description": "Mathematics tutoring assistant",
    "model": "gemini-2.0-flash",
    "tools": ["google_search", "load_web_page"]
  }
}
```

### Code Review Assistant

```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "code_reviewer",
    "instruction": "You are a code review specialist who analyzes code for best practices, potential bugs, security issues, and performance optimizations. You can search for current coding standards and best practices.",
    "description": "Automated code review assistant",
    "model": "gemini-2.0-flash",
    "tools": ["google_search"]
  }
}
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Version Issues

**Problem**: "MCP requires Python 3.10 or higher"
```bash
AttributeError: module 'mcp.types' has no attribute 'Content'
```

**Solution**: Upgrade Python:
```bash
# macOS with Homebrew
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11

# Verify version
python3.11 --version
```

#### 2. Missing Dependencies

**Problem**: `ModuleNotFoundError` for `lxml`, `beautifulsoup4`, etc.

**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
# Or specifically:
pip install lxml beautifulsoup4 aiohttp aiofiles
```

#### 3. Google Cloud Authentication Errors

**Problem**: "Missing key inputs argument! To use the Google AI API, provide (`api_key`) arguments"

**Solutions**:

**Option A - Google AI API Key (easiest):**
```bash
export GOOGLE_AI_API_KEY="your-api-key-from-ai-studio"
```

**Option B - Google Cloud Project:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

**Option C - gcloud CLI:**
```bash
gcloud auth application-default login
```

**Test credentials:**
```bash
python -c "
from google.adk.agents import LlmAgent
try:
    agent = LlmAgent(name='test', model='gemini-2.0-flash', instruction='Hello')
    print('✅ Credentials working!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

#### 4. Agent Execution Fails

**Problem**: Agent runs but returns errors or won't execute

**Solutions**:
- Verify Google Cloud credentials are set (see #3 above)
- Check that the model name is valid (`gemini-2.0-flash`, `gemini-1.5-pro`)
- Ensure tools are properly configured

**Test agent creation:**
```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "test_agent",
    "instruction": "You are a helpful assistant",
    "model": "gemini-2.0-flash"
  }
}
```

#### 5. Web Search Tool Not Working

**Problem**: "GoogleSearchTool is not implemented"

**Solution**: This is expected behavior without Google Search API setup. For full search functionality:
1. Enable Custom Search API in Google Cloud Console
2. Create a Custom Search Engine at https://cse.google.com/
3. Set environment variable: `export GOOGLE_SEARCH_ENGINE_ID="your-search-engine-id"`

#### 6. MCP Server Connection Issues

**Problem**: Cannot connect to MCP server

**Solutions**:
- Verify Python 3.10+ is being used: `python --version`
- Check server is running: `python mcp_server.py`
- Verify client configuration path is correct
- Test with simple test: `python simple_test.py`

#### 7. Import Errors

**Problem**: Various import errors when starting

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python simple_test.py
```

#### 8. BeautifulSoup Parser Error

**Problem**: "Couldn't find a tree builder with the features you requested: lxml"

**Solution**: Install lxml parser:
```bash
pip install lxml
```

#### 9. Evaluation Returns 0% Success Rate

**Problem**: All test cases fail during evaluation

**Cause**: This is expected without proper Google Cloud credentials. Agents cannot execute, so tests fail.

**Solution**: Set up credentials (see #3 above), then re-run evaluation.

#### 10. Claude Desktop Configuration Issues

**Problem**: Tools not appearing in Claude Desktop

**Solution**: Check configuration file path and format:
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

Ensure:
- Use absolute paths
- Python command is correct for your system
- Restart Claude Desktop after configuration changes

### Debug Mode

Enable debug logging:
```bash
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('mcp_server.py').read())
"
```

### Getting Help

Use the built-in documentation tool:
```json
{
  "tool": "get_adk_documentation",
  "arguments": {
    "topic": "agents"
  }
}
```

Available topics: `agents`, `tools`, `deployment`, `evaluation`

## Best Practices

### Agent Design
1. **Clear Instructions**: Provide specific, detailed instructions for what the agent should do
2. **Appropriate Tools**: Only include tools that the agent actually needs
3. **Model Selection**: Use `gemini-2.0-flash` for most use cases, `gemini-1.5-pro` for complex reasoning

### Multi-Agent Systems
1. **Specialized Agents**: Create focused agents for specific tasks
2. **Clear Coordination**: Make coordinator instructions explicit about routing logic
3. **Error Handling**: Test failure scenarios and edge cases

### Performance
1. **Session Management**: Reuse sessions for related conversations
2. **Tool Filtering**: Use tool filters when integrating external MCP servers
3. **Evaluation**: Regularly evaluate agent performance with test cases

### Security
1. **Credential Management**: Use environment variables for sensitive data
2. **Input Validation**: Validate inputs before passing to agents
3. **Access Control**: Limit agent capabilities to what's actually needed

---

For more examples and advanced usage, see the [examples](examples/) directory and the main [README.md](README.md). 