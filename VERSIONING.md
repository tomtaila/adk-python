# Versioning System

This document explains the versioning system and release process for the Google ADK MCP Server.

## Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version (X.y.z): Incompatible API changes
- **MINOR** version (x.Y.z): New functionality (backwards compatible)
- **PATCH** version (x.y.Z): Bug fixes (backwards compatible)

### Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

Examples:
- `1.0.0` - Initial stable release
- `1.1.0` - New features added
- `1.1.1` - Bug fixes
- `2.0.0` - Breaking changes
- `1.2.0-beta.1` - Pre-release version
- `1.2.0+20241219` - Build metadata

## Version Management

### Files Containing Version Information

1. **`version.py`** - Primary version source
   ```python
   __version__ = "1.0.0"
   VERSION_INFO = {
       "major": 1,
       "minor": 0,
       "patch": 0,
       "prerelease": None,
       "build": None
   }
   ```

2. **`mcp_server_project.toml`** - Project configuration
   ```toml
   [project]
   version = "1.0.0"
   ```

3. **`CHANGELOG.md`** - Version history and changes

### Version Access

The version can be accessed programmatically:

```python
from version import __version__, get_version, get_version_info

# Get version string
version = __version__  # "1.0.0"
version = get_version()  # "1.0.0"

# Get detailed version info
info = get_version_info()
# {
#   "major": 1,
#   "minor": 0, 
#   "patch": 0,
#   "prerelease": None,
#   "build": None
# }
```

### MCP Server Version Tool

The MCP server includes a `get_server_version` tool that returns comprehensive version information:

```json
{
  "status": "success",
  "server_name": "Google ADK MCP Server",
  "version": "1.0.0",
  "version_info": {
    "major": 1,
    "minor": 0,
    "patch": 0,
    "prerelease": null,
    "build": null
  },
  "mcp_protocol": "1.0",
  "description": "MCP server exposing Google Agent Development Kit functionality",
  "capabilities": [...],
  "supported_models": [...],
  "documentation": "https://github.com/your-username/google-adk-mcp-server"
}
```

## Release Process

### Automated Release Script

Use the automated release script for version bumps:

```bash
# Patch release (1.0.0 → 1.0.1)
./scripts/release.sh patch

# Minor release (1.0.0 → 1.1.0)
./scripts/release.sh minor

# Major release (1.0.0 → 2.0.0)
./scripts/release.sh major
```

### Manual Release Steps

1. **Update Version Files**
   ```bash
   # Update version.py
   # Update mcp_server_project.toml
   # Update CHANGELOG.md
   ```

2. **Commit Changes**
   ```bash
   git add version.py mcp_server_project.toml CHANGELOG.md
   git commit -m "chore: release version X.Y.Z"
   ```

3. **Create Git Tag**
   ```bash
   git tag -a "vX.Y.Z" -m "Release version X.Y.Z"
   ```

4. **Push Changes**
   ```bash
   git push origin main
   git push origin vX.Y.Z
   ```

### GitHub Actions Automation

The project includes GitHub Actions workflows:

#### Release Workflow (`.github/workflows/release.yml`)
- Triggered on version tags (`v*`)
- Validates version consistency
- Extracts changelog entries
- Creates GitHub releases
- Tests compatibility across Python versions

#### CI Workflow (`.github/workflows/ci.yml`)
- Runs on pushes and pull requests
- Tests across multiple OS and Python versions
- Validates documentation structure
- Checks for security vulnerabilities
- Verifies configuration files

## Changelog Management

### Format

The changelog follows [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.1.0] - 2024-12-20

### Added
- New feature descriptions

### Changed
- Modified functionality descriptions

### Fixed
- Bug fix descriptions

### Removed
- Removed functionality descriptions
```

### Sections

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements

### Unreleased Section

Keep an "Unreleased" section at the top for ongoing development:

```markdown
## [Unreleased]

### Planned
- Feature planning
- Upcoming improvements
```

## Version History

### v1.0.0 (2024-12-19)
- Initial release with complete MCP server functionality
- Full Google ADK integration
- Claude Desktop and Cursor IDE support
- Comprehensive documentation and setup automation
- Multi-agent system capabilities
- Web search and content extraction tools

## Best Practices

### When to Bump Versions

#### PATCH (x.y.Z)
- Bug fixes
- Documentation updates
- Internal refactoring
- Dependency updates (non-breaking)

#### MINOR (x.Y.z)
- New features (backwards compatible)
- New MCP tools
- New agent capabilities
- Enhanced functionality

#### MAJOR (X.y.z)
- Breaking API changes
- Incompatible MCP protocol changes
- Major architectural changes
- Removal of deprecated features

### Pre-release Versions

For testing and development:

```bash
# Alpha release
1.1.0-alpha.1

# Beta release  
1.1.0-beta.1

# Release candidate
1.1.0-rc.1
```

### Development Workflow

1. **Feature Development**
   - Work on feature branches
   - Update "Unreleased" section in CHANGELOG.md
   - Test thoroughly

2. **Release Preparation**
   - Move changes from "Unreleased" to new version section
   - Update version files
   - Create release commit and tag

3. **Post-Release**
   - Monitor for issues
   - Prepare patch releases if needed
   - Plan next version features

## Tools and Scripts

### Release Script (`scripts/release.sh`)
- Automated version bumping
- Changelog updates
- Git tagging
- Validation checks

### GitHub Actions
- Automated testing
- Release creation
- Version validation
- Security scanning

### Version Validation
```bash
# Check version consistency
python -c "from version import __version__; print(__version__)"

# Test MCP server version tool
python -c "import asyncio; from mcp_server import get_server_version; print(asyncio.run(get_server_version()))"
```

This versioning system ensures consistent, traceable releases while maintaining compatibility and providing clear upgrade paths for users. 