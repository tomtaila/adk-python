#!/bin/bash

# Google ADK MCP Server Release Script
# Usage: ./scripts/release.sh [major|minor|patch]

set -e

RELEASE_TYPE=${1:-patch}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Google ADK MCP Server Release Process"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "$PROJECT_ROOT/version.py" ]; then
    echo "❌ Error: version.py not found. Please run from project root."
    exit 1
fi

# Check if git working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Error: Git working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Read current version
CURRENT_VERSION=$(python -c "from version import __version__; print(__version__)")
echo "📋 Current version: $CURRENT_VERSION"

# Calculate new version
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

case $RELEASE_TYPE in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "❌ Error: Invalid release type. Use 'major', 'minor', or 'patch'"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "📦 New version: $NEW_VERSION"

# Confirm release
read -p "🤔 Proceed with release $NEW_VERSION? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "❌ Release cancelled."
    exit 0
fi

# Update version.py
echo "📝 Updating version.py..."
cat > "$PROJECT_ROOT/version.py" << EOF
"""Version information for Google ADK MCP Server."""

__version__ = "$NEW_VERSION"

# Version components
VERSION_INFO = {
    "major": $MAJOR,
    "minor": $MINOR,
    "patch": $PATCH,
    "prerelease": None,
    "build": None
}

def get_version() -> str:
    """Get the current version string."""
    return __version__

def get_version_info() -> dict:
    """Get detailed version information."""
    return VERSION_INFO.copy()
EOF

# Update project config
echo "📝 Updating mcp_server_project.toml..."
sed -i.bak "s/version = \".*\"/version = \"$NEW_VERSION\"/" "$PROJECT_ROOT/mcp_server_project.toml"
rm -f "$PROJECT_ROOT/mcp_server_project.toml.bak"

# Update CHANGELOG.md
echo "📝 Updating CHANGELOG.md..."
RELEASE_DATE=$(date +%Y-%m-%d)
TEMP_CHANGELOG=$(mktemp)

# Add new release section to changelog
cat > "$TEMP_CHANGELOG" << EOF
# Changelog

All notable changes to the Google ADK MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- GitHub Actions CI/CD pipeline
- Docker containerization
- Additional IDE integrations (VS Code, PyCharm)
- Enhanced multi-agent orchestration
- Performance monitoring and metrics
- Additional tool integrations

## [$NEW_VERSION] - $RELEASE_DATE

### Added
- Version $NEW_VERSION release

### Changed
- Updated version to $NEW_VERSION

EOF

# Append existing changelog content (skip first few lines)
tail -n +8 "$PROJECT_ROOT/CHANGELOG.md" >> "$TEMP_CHANGELOG"
mv "$TEMP_CHANGELOG" "$PROJECT_ROOT/CHANGELOG.md"

# Create git commit
echo "📝 Creating git commit..."
git add version.py mcp_server_project.toml CHANGELOG.md
git commit -m "chore: release version $NEW_VERSION"

# Create git tag
echo "🏷️ Creating git tag..."
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"

echo ""
echo "✅ Release $NEW_VERSION completed successfully!"
echo ""
echo "Next steps:"
echo "1. Push changes: git push origin main"
echo "2. Push tags: git push origin v$NEW_VERSION"
echo "3. Create GitHub release with changelog excerpt"
echo "4. Update documentation if needed"
echo ""
echo "📋 Release summary:"
echo "   - Version: $CURRENT_VERSION → $NEW_VERSION"
echo "   - Commit: $(git rev-parse --short HEAD)"
echo "   - Tag: v$NEW_VERSION"
echo "" 