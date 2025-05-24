# Changelog

All notable changes to the Google ADK MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added

#### Core MCP Server
- Complete MCP (Model Context Protocol) server implementation with 11 tools
- JSON-RPC 2.0 compliance for MCP protocol communication
- Agent management tools: `create_adk_agent`, `list_adk_agents`, `get_adk_agent_info`, `run_adk_agent`
- Multi-agent system support: `create_multi_agent_system`, `add_mcp_tools_to_agent`
- Evaluation and testing: `evaluate_adk_agent`, `list_available_tools`
- Utility tools: `search_web`, `load_webpage_content`, `get_adk_documentation`
- Session management for conversation continuity
- Comprehensive error handling with helpful dependency messages

#### Agent Capabilities
- Support for multiple Gemini models (`gemini-2.0-flash`, `gemini-1.5-pro`, `gemini-1.5-flash`)
- Integration with Google's built-in tools (Google Search, web scraping)
- External MCP server integration for expanding agent capabilities
- Multi-agent coordination with coordinator and specialist agents
- Agent evaluation with structured test cases and performance metrics

#### Documentation & Setup
- Complete README.md with installation, usage, and integration guides
- Comprehensive USAGE.md with detailed examples and troubleshooting (800+ lines)
- Automated setup script (`setup.sh`) with Python version checking and credential validation
- Requirements.txt with all necessary dependencies
- Simple test suite for basic functionality verification
- Comprehensive test client with 11 tool demonstrations

#### IDE Integrations
- Claude Desktop integration with example configuration
- Cursor IDE integration with dedicated setup guide (317 lines)
- Multiple configuration approaches (service account, API key, system environment)
- Platform-specific instructions for macOS, Linux, and Windows
- Development workflow examples and troubleshooting guides

#### Dependencies & Compatibility
- Python 3.10+ support (required for MCP)
- Google ADK integration (`google-adk>=1.0.0`)
- MCP SDK integration (`mcp>=1.5.0`)
- Web scraping support (`beautifulsoup4>=4.12.0`, `lxml>=4.9.0`)
- Async operations (`aiohttp>=3.8.0`, `aiofiles>=23.0.0`)
- Google Cloud integration with multiple authentication methods

### Fixed

#### Import and Type Issues
- Fixed `from google.adk.evaluation import evaluate_agent` → `from google.adk.evaluation import evaluator`
- Fixed MCP type annotations: `types.Content` → `types.TextContent` for return types
- Fixed Google GenAI types: `genai_types.TextContent` → `genai_types.Content` for message creation
- Fixed tool wrapping issues: `google_search` used directly, `load_web_page` wrapped in `FunctionTool`
- Resolved "'GoogleSearchTool' object has no attribute '__name__'" error

#### Dependency Issues
- Added missing `lxml>=4.9.0` (required for BeautifulSoup web scraping)
- Added missing `beautifulsoup4>=4.12.0`, `aiohttp>=3.8.0`, `aiofiles>=23.0.0`
- Fixed BeautifulSoup parser errors with proper lxml installation
- Resolved ModuleNotFoundError issues for web scraping functionality

#### Authentication and Credentials
- Clarified Google Cloud credentials as required (not optional) for agent execution
- Added multiple credential setup methods (Google AI API Key, Google Cloud Project, gcloud CLI)
- Fixed "Missing key inputs argument" errors with proper credential configuration
- Added credential testing and validation in setup script

### Changed

#### Python Version Requirements
- Updated minimum Python requirement from 3.9 to 3.10+ (MCP requirement)
- Added platform-specific Python upgrade instructions
- Enhanced Python version detection in setup script
- Updated virtual environment creation to use Python 3.10+

#### Setup and Installation
- Converted from basic setup to comprehensive automated setup script
- Enhanced error messages with specific platform-specific solutions
- Added credential checking and validation during setup
- Improved dependency installation with better error handling

#### Documentation Structure
- Reorganized README.md with clear prerequisites and step-by-step instructions
- Expanded troubleshooting from basic to comprehensive (10+ common issues)
- Added detailed credential setup guides for multiple authentication methods
- Enhanced usage examples with real-world development workflows

## [Unreleased]

### Planned
- GitHub Actions CI/CD pipeline
- Docker containerization
- Additional IDE integrations (VS Code, PyCharm)
- Enhanced multi-agent orchestration
- Performance monitoring and metrics
- Additional tool integrations

---

## Version History

- **v1.0.0** (2024-12-19) - Initial release with complete MCP server functionality
  - Full Google ADK integration
  - Claude Desktop and Cursor IDE support
  - Comprehensive documentation and setup automation
  - Multi-agent system capabilities
  - Web search and content extraction tools

## Development Notes

### Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Process

1. Update version in `version.py`
2. Update CHANGELOG.md with new features and fixes
3. Create git tag with version number
4. Create GitHub release with changelog excerpt
5. Update documentation if needed

### Contributing

When contributing, please:
- Add new features to the "Unreleased" section
- Follow the changelog format (Added, Changed, Fixed, Removed)
- Update version.py for releases
- Include breaking changes in the description
