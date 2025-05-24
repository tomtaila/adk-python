"""Version information for Google ADK MCP Server."""

__version__ = "1.0.0"

# Version components
VERSION_INFO = {
    "major": 1,
    "minor": 0,
    "patch": 0,
    "prerelease": None,
    "build": None
}

def get_version() -> str:
    """Get the current version string."""
    return __version__

def get_version_info() -> dict:
    """Get detailed version information."""
    return VERSION_INFO.copy() 