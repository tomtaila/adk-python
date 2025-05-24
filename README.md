# Google ADK MCP Server

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io/)

<html>
    <h2 align="center">
      <img src="https://raw.githubusercontent.com/google/adk-python/main/assets/agent-development-kit.png" width="256"/>
    </h2>
    <h3 align="center">
      A standalone MCP (Model Context Protocol) server that exposes Google Agent Development Kit (ADK) functionality to MCP clients.
    </h3>
    <h3 align="center">
      Important Links:
      <a href="https://google.github.io/adk-docs/">ADK Docs</a>, 
      <a href="https://github.com/google/adk-python">ADK Repository</a>,
      <a href="https://spec.modelcontextprotocol.io/">MCP Specification</a> &
      <a href="https://modelcontextprotocol.io/">MCP Documentation</a>.
    </h3>
</html>

This standalone MCP server allows any MCP-compatible client (such as Claude Desktop, Cursor IDE, or custom applications) to leverage Google's powerful Agent Development Kit for building, running, and managing AI agents.

---

## ✨ Key Features

- **Complete ADK Integration**: Create, configure, and run Google ADK agents through MCP
- **Multi-Agent Systems**: Build sophisticated multi-agent architectures with coordinators and sub-agents
- **Rich Tool Ecosystem**: Access ADK's built-in tools (Google Search, web scraping, etc.) and integrate external MCP tools
- **Agent Evaluation**: Test and evaluate agent performance with structured test cases
- **Session Management**: Maintain conversation history and state across interactions
- **Real-time Execution**: Run agents and get responses through the MCP protocol
- **IDE Integration**: Works with Claude Desktop, Cursor IDE, and other MCP clients

## 🛠 Available MCP Tools

The server exposes 12 tools to MCP clients:

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
- **`get_server_version`** - Get server version and capability information

## 🚀 Installation

### Prerequisites

- **Python 3.10 or higher** (required for MCP support)
- **Google Cloud credentials** (required for agent execution and web search functionality)
- **Git** (for cloning the repository)

#### Python Version Requirements
MCP requires Python 3.10+. If you have an older version:
- **macOS with Homebrew**: `brew install python@3.11`
- **Ubuntu/Debian**: `sudo apt-get install python3.11`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

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

##### Cursor IDE Configuration

See [examples/CURSOR_SETUP.md](examples/CURSOR_SETUP.md) for detailed Cursor integration instructions.

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

### 2. Building a Multi-Agent System

```json
{
  "tool": "create_multi_agent_system",
  "arguments": {
    "coordinator_name": "customer_service_coordinator",
    "coordinator_instruction": "You coordinate customer service requests by routing them to the appropriate specialist agent.",
    "sub_agents": ["faq_agent", "technical_support", "sales_info"],
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
├── version.py                 # Version management
├── requirements.txt           # Dependencies (uses google-adk as dependency)
├── pyproject.toml            # Project configuration
├── README.md                 # This file
├── CHANGELOG.md              # Version history
├── VERSIONING.md             # Versioning system documentation
├── setup.sh                  # Automated setup script
├── simple_test.py            # Basic functionality tests
├── examples/                 # Configuration examples and tests
│   ├── claude_desktop_config.json
│   ├── cursor_mcp_config.json
│   ├── CURSOR_SETUP.md
│   └── test_mcp_client.py
├── scripts/                  # Release automation
│   └── release.sh
└── .github/workflows/        # CI/CD pipelines
    ├── ci.yml
    └── release.yml
```

### Running Tests

```bash
# Run basic functionality test
python simple_test.py

# Run comprehensive test suite
python examples/test_mcp_client.py

# Install development dependencies
pip install -e ".[dev]"
```

### Versioning

This project uses semantic versioning. See [VERSIONING.md](VERSIONING.md) for details.

```bash
# Create a new release
./scripts/release.sh patch   # 1.0.0 → 1.0.1
./scripts/release.sh minor   # 1.0.0 → 1.1.0  
./scripts/release.sh major   # 1.0.0 → 2.0.0
```

## 📚 Documentation

### Project Documentation
- [USAGE.md](USAGE.md) - Detailed usage guide with examples
- [VERSIONING.md](VERSIONING.md) - Versioning system and release process
- [CHANGELOG.md](CHANGELOG.md) - Version history and changes
- [examples/CURSOR_SETUP.md](examples/CURSOR_SETUP.md) - Cursor IDE integration

### ADK Documentation
- [ADK Docs](https://google.github.io/adk-docs/) - Complete ADK documentation
- [ADK Repository](https://github.com/google/adk-python) - Google ADK source code
- [ADK API Reference](https://google.github.io/adk-docs/api-reference/) - API reference

### MCP Documentation
- [MCP Specification](https://spec.modelcontextprotocol.io/) - Official MCP protocol specification
- [MCP Documentation](https://modelcontextprotocol.io/) - MCP guides and tutorials

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork and clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests to ensure everything works
4. Make your changes and add tests
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

1. **MCP Connection Fails**
   - Ensure Python 3.10+ is being used
   - Check that `mcp` package is installed
   - Verify the server path in client configuration

2. **ADK Agent Creation Fails**
   - Check Google Cloud credentials are configured
   - Verify model names are correct
   - Ensure `google-adk` dependency is installed

3. **Tool Execution Errors**
   - Check tool names are spelled correctly
   - Verify required parameters are provided
   - Look at server logs for detailed error messages

For detailed troubleshooting, see [USAGE.md](USAGE.md).

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes and version information.

## 🔗 Related Projects

- [Google ADK Python](https://github.com/google/adk-python) - The core ADK library this server depends on
- [Model Context Protocol](https://modelcontextprotocol.io/) - The MCP specification and ecosystem

---

*A standalone MCP server that brings Google's powerful Agent Development Kit to the Model Context Protocol ecosystem!*
