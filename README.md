# Google ADK MCP Server

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Unit Tests](https://github.com/google/adk-python/actions/workflows/python-unit-tests.yml/badge.svg)](https://github.com/google/adk-python/actions/workflows/python-unit-tests.yml)
[![r/agentdevelopmentkit](https://img.shields.io/badge/Reddit-r%2Fagentdevelopmentkit-FF4500?style=flat&logo=reddit&logoColor=white)](https://www.reddit.com/r/agentdevelopmentkit/)

<html>
    <h2 align="center">
      <img src="https://raw.githubusercontent.com/google/adk-python/main/assets/agent-development-kit.png" width="256"/>
    </h2>
    <h3 align="center">
      A comprehensive MCP (Model Context Protocol) server that exposes Google Agent Development Kit (ADK) functionality to MCP clients.
    </h3>
    <h3 align="center">
      Important Links:
      <a href="https://google.github.io/adk-docs/">ADK Docs</a>, 
      <a href="https://github.com/google/adk-samples">ADK Samples</a>,
      <a href="https://spec.modelcontextprotocol.io/">MCP Specification</a> &
      <a href="https://modelcontextprotocol.io/">MCP Documentation</a>.
    </h3>
</html>

This MCP server allows any MCP-compatible client (such as Claude Desktop, IDEs with MCP support, or custom applications) to leverage Google's powerful Agent Development Kit for building, running, and managing AI agents.

---

## ✨ Key Features

- **Complete ADK Integration**: Create, configure, and run Google ADK agents through MCP
- **Multi-Agent Systems**: Build sophisticated multi-agent architectures with coordinators and sub-agents
- **Rich Tool Ecosystem**: Access ADK's built-in tools (Google Search, web scraping, etc.) and integrate external MCP tools
- **Agent Evaluation**: Test and evaluate agent performance with structured test cases
- **Session Management**: Maintain conversation history and state across interactions
- **Real-time Execution**: Run agents and get responses through the MCP protocol
- **Documentation Access**: Get help and information about ADK features and capabilities

## 🛠 Available MCP Tools

The server exposes the following tools to MCP clients:

### Agent Management
- **`create_adk_agent`** - Create new ADK agents with custom configurations
- **`list_adk_agents`** - List all created agents
- **`get_adk_agent_info`** - Get detailed information about specific agents
- **`run_adk_agent`** - Execute agents with user messages and get responses

### Multi-Agent Systems
- **`create_multi_agent_system`** - Create coordinator agents with sub-agents
- **`add_mcp_tools_to_agent`** - Integrate external MCP servers into ADK agents

### Evaluation & Testing
- **`evaluate_adk_agent`** - Run test cases against agents and get performance metrics
- **`list_available_tools`** - Discover available ADK tools

### Utility Tools
- **`search_web`** - Perform Google searches
- **`load_webpage_content`** - Extract content from web pages
- **`get_adk_documentation`** - Access ADK documentation and help

## 🚀 Installation

### Prerequisites

- **Python 3.10 or higher** (required for MCP support, tested with Python 3.11+)
- **Google Cloud credentials** (required for agent execution and web search functionality)
- **Git** (for cloning the repository)

#### Python Version Requirements
MCP requires Python 3.10+. If you have an older version:
- **macOS with Homebrew**: `brew install python@3.11`
- **Ubuntu/Debian**: `sudo apt-get install python3.11`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Other systems**: Check your package manager or download from [python.org](https://www.python.org/downloads/)

#### Google Cloud Setup (Required)
For full functionality, you need Google Cloud credentials:
1. **Google AI API Key** (simpler setup) - Get from [Google AI Studio](https://aistudio.google.com/apikey)
2. **Google Cloud Project** (full features) - Set up at [Google Cloud Console](https://console.cloud.google.com/)

### Install Dependencies

#### Quick Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-username/google-adk-mcp-server.git
cd google-adk-mcp-server

# Run the automated setup script
chmod +x setup.sh
./setup.sh
```

#### Manual Setup
```bash
# Create a virtual environment (Python 3.10+ required)
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python simple_test.py
```

#### Dependencies Installed
The setup includes:
- `google-adk>=1.0.0` - Google Agent Development Kit
- `mcp>=1.5.0` - Model Context Protocol
- `beautifulsoup4>=4.12.0` + `lxml>=4.9.0` - Web scraping
- `aiohttp>=3.8.0` + `aiofiles>=23.0.0` - Async HTTP and file operations
- Various Google Cloud libraries for enhanced features

### Environment Setup

**⚠️ Required**: Set up Google Cloud credentials for agent execution and web search:

#### Option 1: Google AI API Key (Recommended for getting started)
```bash
# Set your Google AI API key
export GOOGLE_AI_API_KEY="your-api-key-here"
```

#### Option 2: Google Cloud Project (Full features)
```bash
# Set up Google Cloud credentials using service account
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"

# Or authenticate using gcloud CLI
gcloud auth application-default login

# Set your Google Cloud project
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"  # or your preferred region
```

#### Additional Setup for Web Search
For Google Search functionality, you may also need:
```bash
# Enable Custom Search API in Google Cloud Console
# Create a Custom Search Engine at https://cse.google.com/
export GOOGLE_SEARCH_ENGINE_ID="your-search-engine-id"
```

#### Testing Credentials
Run this to verify your setup:
```bash
python -c "
from google.adk.agents import LlmAgent
agent = LlmAgent(name='test', model='gemini-2.0-flash', instruction='Hello')
print('✅ Credentials configured correctly!')
"
```

## 📖 Usage

### Running the MCP Server

#### As a Standalone Server

```bash
# Run the MCP server directly
python mcp_server.py
```

#### With MCP Clients

##### Claude Desktop Configuration

Add to your Claude Desktop MCP configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "google-adk": {
      "command": "python",
      "args": ["/path/to/google-adk-mcp-server/mcp_server.py"]
    }
  }
}
```

##### Custom MCP Client

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Connect to the ADK MCP server
server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize connection
        await session.initialize()
        
        # List available tools
        tools = await session.list_tools()
        
        # Create an agent
        result = await session.call_tool("create_adk_agent", {
            "name": "my_assistant",
            "instruction": "You are a helpful assistant that can search the web and answer questions.",
            "model": "gemini-2.0-flash",
            "tools": ["google_search", "load_web_page"]
        })
        
        # Run the agent
        response = await session.call_tool("run_adk_agent", {
            "agent_name": "my_assistant",
            "message": "What's the latest news about AI?"
        })
```

## 🎯 Example Workflows

### 1. Creating a Research Assistant

```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "research_assistant",
    "instruction": "You are a research assistant that helps users find and analyze information from the web. Always provide sources and summarize key findings.",
    "description": "AI assistant specialized in web research and analysis",
    "model": "gemini-2.0-flash",
    "tools": ["google_search", "load_web_page"]
  }
}
```

### 2. Building a Multi-Agent Customer Service System

First, create specialized agents:

```json
{
  "tool": "create_adk_agent",
  "arguments": {
    "name": "faq_agent",
    "instruction": "You specialize in answering frequently asked questions about our products and services.",
    "model": "gemini-2.0-flash"
  }
}
```

```json
{
  "tool": "create_adk_agent", 
  "arguments": {
    "name": "technical_support",
    "instruction": "You provide technical support and troubleshooting assistance.",
    "model": "gemini-2.0-flash",
    "tools": ["google_search"]
  }
}
```

Then create a coordinator:

```json
{
  "tool": "create_multi_agent_system",
  "arguments": {
    "coordinator_name": "customer_service_coordinator",
    "coordinator_instruction": "You coordinate customer service requests by routing them to the appropriate specialist agent.",
    "sub_agents": ["faq_agent", "technical_support"],
    "model": "gemini-2.0-flash"
  }
}
```

### 3. Agent Evaluation

```json
{
  "tool": "evaluate_adk_agent",
  "arguments": {
    "agent_name": "research_assistant",
    "test_cases": [
      {
        "input": "Find information about climate change effects",
        "expected_output": "climate change"
      },
      {
        "input": "What are the latest developments in AI?",
        "expected_output": "artificial intelligence"
      }
    ]
  }
}
```

## 🔧 Configuration

### Agent Models

Supported models include:
- `gemini-2.0-flash` (default)
- `gemini-1.5-pro`
- `gemini-1.5-flash`

### Available Tools

Built-in ADK tools that can be added to agents:
- `google_search` - Web search functionality
- `load_web_page` - Web page content extraction
- `agent_tool` - Wrap other agents as tools

### External MCP Integration

You can integrate external MCP servers into your ADK agents:

```json
{
  "tool": "add_mcp_tools_to_agent",
  "arguments": {
    "agent_name": "my_agent",
    "mcp_server_command": "npx",
    "mcp_server_args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"],
    "tool_filter": ["read_file", "list_directory"]
  }
}
```

## 🧪 Development

### Project Structure

```
google-adk-mcp-server/
├── mcp_server.py              # Main MCP server implementation
├── README.md                  # This file
├── pyproject.toml            # Project configuration
├── src/google/adk/           # Google ADK source code
├── tests/                    # Test files
└── assets/                   # Assets and documentation
```

### Running Tests

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/

# Run with coverage
python -m pytest tests/ --cov=src/
```

### Code Quality

```bash
# Format code
./autoformat.sh

# Run linting
pylint src/

# Type checking
mypy src/
```

## 📚 Documentation

### ADK Documentation
- [ADK Docs](https://google.github.io/adk-docs/) - Complete ADK documentation
- [ADK Samples](https://github.com/google/adk-samples) - Example implementations
- [ADK Python API](https://google.github.io/adk-docs/api-reference/) - API reference

### MCP Documentation
- [MCP Specification](https://spec.modelcontextprotocol.io/) - Official MCP protocol specification
- [MCP Documentation](https://modelcontextprotocol.io/) - MCP guides and tutorials
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Python implementation

### Getting Help

```json
{
  "tool": "get_adk_documentation",
  "arguments": {
    "topic": "agents"
  }
}
```

Available documentation topics:
- `agents` - Information about agent types and features
- `tools` - Tool ecosystem and integration
- `deployment` - Deployment options and configuration
- `evaluation` - Testing and evaluation capabilities

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork and clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests to ensure everything works
4. Make your changes and add tests
5. Submit a pull request

### Code Style

We use Google's Python style guide and enforce it with:
- `pyink` for formatting
- `pylint` for linting
- `mypy` for type checking

## 🐛 Troubleshooting

### Common Issues

1. **MCP Connection Fails**
   - Ensure Python 3.10+ is being used
   - Check that `mcp` package is installed
   - Verify the server path in client configuration

2. **ADK Agent Creation Fails**
   - Check Google Cloud credentials if using cloud features
   - Verify model names are correct
   - Ensure required dependencies are installed

3. **Tool Execution Errors**
   - Check tool names are spelled correctly
   - Verify required parameters are provided
   - Look at server logs for detailed error messages

### Debug Mode

Run the server with debug logging:

```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('mcp_server.py').read())
"
```

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Google ADK Python](https://github.com/google/adk-python) - The core ADK library
- [Google ADK Java](https://github.com/google/adk-java) - Java implementation of ADK
- [Model Context Protocol](https://modelcontextprotocol.io/) - The MCP specification and ecosystem

---

*Build powerful AI agents with Google ADK through the Model Context Protocol!*
