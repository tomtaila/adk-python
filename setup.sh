#!/bin/bash

# Google ADK MCP Server Setup Script
# This script helps you set up the Google ADK MCP server environment

set -e

echo "🚀 Google ADK MCP Server Setup"
echo "=============================="

# Check Python version
echo "📋 Checking Python version..."

# Function to check Python version
check_python_version() {
    local python_cmd=$1
    if command -v "$python_cmd" >/dev/null 2>&1; then
        if $python_cmd -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
            local version=$($python_cmd --version 2>&1 | awk '{print $2}')
            echo "✅ Found compatible Python: $python_cmd (version $version)"
            export PYTHON_CMD="$python_cmd"
            return 0
        fi
    fi
    return 1
}

# Try to find a suitable Python version
PYTHON_CMD=""
for cmd in python3.11 python3.10 python3 python; do
    if check_python_version "$cmd"; then
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3.10 or higher is required for MCP support."
    echo ""
    echo "Installation instructions:"
    echo "  macOS with Homebrew: brew install python@3.11"
    echo "  Ubuntu/Debian: sudo apt-get install python3.11"
    echo "  Windows: Download from https://www.python.org/downloads/"
    echo "  Other systems: Check your package manager or python.org"
    echo ""
    echo "After installation, try running this script again."
    exit 1
fi

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. It's recommended to use one."
    read -p "Do you want to create a virtual environment? (y/n): " create_venv
    if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
        echo "📦 Creating virtual environment with $PYTHON_CMD..."
        $PYTHON_CMD -m venv venv
        echo "✅ Virtual environment created. Please activate it with:"
        echo "   source venv/bin/activate"
        echo "Then run this setup script again."
        exit 0
    fi
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Installing core dependencies directly..."
    pip install google-adk mcp
fi

echo "✅ Dependencies installed successfully!"

# Check Google Cloud credentials setup
echo ""
echo "🔧 Google Cloud Setup (Required for Agent Execution)"
echo "=================================================="
echo "ADK agents require Google Cloud credentials to run. Without them,"
echo "you'll see errors like: 'Missing key inputs argument!'"
echo ""

# Check for existing credentials
has_creds=false
if [ -n "$GOOGLE_AI_API_KEY" ]; then
    echo "✅ GOOGLE_AI_API_KEY found in environment"
    has_creds=true
elif [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "✅ GOOGLE_APPLICATION_CREDENTIALS found: $GOOGLE_APPLICATION_CREDENTIALS"
    has_creds=true
elif command -v gcloud >/dev/null 2>&1 && gcloud auth application-default print-access-token >/dev/null 2>&1; then
    echo "✅ gcloud authentication found"
    has_creds=true
fi

if [ "$has_creds" = false ]; then
    echo "⚠️  No Google Cloud credentials detected!"
    echo ""
    echo "Setup options (choose one):"
    echo ""
    echo "1. Google AI API Key (easiest):"
    echo "   - Get API key from: https://aistudio.google.com/apikey"
    echo "   - Run: export GOOGLE_AI_API_KEY=\"your-api-key\""
    echo ""
    echo "2. Google Cloud Project (full features):"
    echo "   - Set up project at: https://console.cloud.google.com/"
    echo "   - Download service account JSON"
    echo "   - Run: export GOOGLE_APPLICATION_CREDENTIALS=\"/path/to/key.json\""
    echo ""
    echo "3. gcloud CLI:"
    echo "   - Install gcloud CLI"
    echo "   - Run: gcloud auth application-default login"
    echo ""
    
    read -p "Continue setup without credentials? Agents won't execute until configured. (y/n): " continue_setup
    if [[ $continue_setup == "n" || $continue_setup == "N" ]]; then
        echo "Setup paused. Configure credentials and re-run this script."
        exit 0
    fi
fi

# Test the installation
echo ""
echo "🧪 Testing installation..."
echo "=========================="

if python3 -c "import google.adk; import mcp; print('✅ Core imports successful')"; then
    echo "✅ All core dependencies are working!"
else
    echo "❌ Import test failed. Please check the installation."
    exit 1
fi

# Create example directory if it doesn't exist
if [ ! -d "examples" ]; then
    mkdir examples
    echo "📁 Created examples directory"
fi

# Make scripts executable
chmod +x mcp_server.py 2>/dev/null || echo "⚠️  Note: mcp_server.py not found or already executable"
chmod +x examples/test_mcp_client.py 2>/dev/null || echo "⚠️  Note: test_mcp_client.py not found or already executable"

echo ""
echo "🎉 Setup completed successfully!"
echo "==============================="
echo ""
echo "Next steps:"

if [ "$has_creds" = false ]; then
    echo "⚠️  IMPORTANT: Set up Google Cloud credentials first!"
    echo "   Without credentials, agents cannot execute."
    echo "   See setup options above or README.md for details."
    echo ""
fi

echo "1. Test basic functionality:"
echo "   python simple_test.py"
echo ""
echo "2. Start the MCP server:"
echo "   $PYTHON_CMD mcp_server.py"
echo ""
echo "3. Test with comprehensive suite:"
echo "   $PYTHON_CMD examples/test_mcp_client.py"
echo ""
echo "4. Configure your MCP client (e.g., Claude Desktop):"
echo "   See examples/claude_desktop_config.json for configuration"
echo ""
echo "5. Read USAGE.md for detailed usage instructions"
echo ""

if [ "$has_creds" = true ]; then
    echo "✅ Credentials are configured - ready to build agents!"
else
    echo "📋 Reminder: Configure Google Cloud credentials to run agents"
fi

echo ""
echo "Happy agent building! 🤖" 