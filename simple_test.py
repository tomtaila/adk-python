#!/usr/bin/env python3
"""
Simple test for Google ADK MCP Server
Tests basic functionality without running the full test suite.
"""

import asyncio
import json
import sys
from typing import Dict, Any

# Test if imports work
def test_imports():
    """Test that all required imports work."""
    try:
        # Test MCP imports
        import mcp.types as types
        from mcp.server import Server
        print("✅ MCP imports successful")
        
        # Test Google ADK imports  
        from google.adk.agents import LlmAgent
        from google.adk.tools import FunctionTool, google_search
        print("✅ Google ADK imports successful")
        
        # Test our server import
        import mcp_server
        print("✅ MCP server import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_server_creation():
    """Test that we can create the MCP server."""
    try:
        from mcp_server import server
        print("✅ Server creation successful")
        return True
    except Exception as e:
        print(f"❌ Server creation failed: {e}")
        return False

def test_tools_list():
    """Test that we can get the tools list."""
    try:
        from mcp_server import handle_list_tools
        tools = asyncio.run(handle_list_tools())
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "create_adk_agent",
            "list_adk_agents", 
            "get_adk_agent_info",
            "run_adk_agent",
            "list_available_tools",
            "evaluate_adk_agent",
            "create_multi_agent_system",
            "add_mcp_tools_to_agent",
            "search_web",
            "load_webpage_content",
            "get_adk_documentation"
        ]
        
        missing_tools = [tool for tool in expected_tools if tool not in tool_names]
        if missing_tools:
            print(f"❌ Missing tools: {missing_tools}")
            return False
        
        print(f"✅ All {len(tools)} tools available: {tool_names}")
        return True
    except Exception as e:
        print(f"❌ Tools list failed: {e}")
        return False

def main():
    """Run simple tests."""
    print("🧪 Google ADK MCP Server - Simple Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Server Creation Test", test_server_creation), 
        ("Tools List Test", test_tools_list)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n🎯 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Google ADK MCP Server is ready to use.")
        print("\n📚 Next steps:")
        print("1. Set up Google Cloud credentials for ADK")
        print("2. Configure Claude Desktop to use this MCP server")
        print("3. Test creating and running agents")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 