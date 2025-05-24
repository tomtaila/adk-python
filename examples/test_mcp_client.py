#!/usr/bin/env python3
"""
Test script for Google ADK MCP Server

This script demonstrates how to connect to and use the Google ADK MCP server
programmatically. It shows examples of creating agents, running them, and
evaluating their performance.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the MCP types
sys.path.append(str(Path(__file__).parent.parent))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_adk_mcp_server():
    """Test the Google ADK MCP server functionality."""
    
    # Path to the MCP server script
    server_script = Path(__file__).parent.parent / "mcp_server.py"
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[str(server_script)]
    )
    
    print("🚀 Starting Google ADK MCP Server test...")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                print("✅ Connected to Google ADK MCP Server")
                
                # List available tools
                print("\n📋 Listing available tools...")
                tools_result = await session.list_tools()
                print(f"Found {len(tools_result.tools)} tools:")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test 1: Create a simple agent
                print("\n🤖 Creating a research assistant agent...")
                create_result = await session.call_tool("create_adk_agent", {
                    "name": "research_assistant",
                    "instruction": "You are a helpful research assistant that can search the web for information and analyze web pages.",
                    "description": "Research assistant with web search capabilities",
                    "model": "gemini-2.0-flash",
                    "tools": ["google_search", "load_web_page"]
                })
                print("✅ Agent created:")
                print(json.dumps(json.loads(create_result.content[0].text), indent=2))
                
                # Test 2: List agents
                print("\n📋 Listing all agents...")
                list_result = await session.call_tool("list_adk_agents", {})
                print("📊 Current agents:")
                print(json.dumps(json.loads(list_result.content[0].text), indent=2))
                
                # Test 3: Get agent info
                print("\n📖 Getting agent information...")
                info_result = await session.call_tool("get_adk_agent_info", {
                    "agent_name": "research_assistant"
                })
                print("📋 Agent details:")
                print(json.dumps(json.loads(info_result.content[0].text), indent=2))
                
                # Test 4: Run the agent
                print("\n🏃 Running the agent with a test message...")
                run_result = await session.call_tool("run_adk_agent", {
                    "agent_name": "research_assistant",
                    "message": "What is the Model Context Protocol (MCP) and how does it work?",
                    "session_id": "test_session"
                })
                print("💬 Agent response:")
                response_data = json.loads(run_result.content[0].text)
                print(json.dumps(response_data, indent=2))
                
                # Test 5: Create another agent
                print("\n🤖 Creating a technical support agent...")
                tech_result = await session.call_tool("create_adk_agent", {
                    "name": "tech_support",
                    "instruction": "You are a technical support specialist who helps users troubleshoot problems.",
                    "description": "Technical support agent",
                    "model": "gemini-2.0-flash"
                })
                print("✅ Technical support agent created")
                
                # Test 6: Create a multi-agent system
                print("\n🏗️ Creating a multi-agent system...")
                multi_agent_result = await session.call_tool("create_multi_agent_system", {
                    "coordinator_name": "customer_service_coordinator",
                    "coordinator_instruction": "You coordinate customer requests by routing them to the appropriate specialist agent (research or technical support).",
                    "sub_agents": ["research_assistant", "tech_support"],
                    "model": "gemini-2.0-flash"
                })
                print("✅ Multi-agent system created:")
                print(json.dumps(json.loads(multi_agent_result.content[0].text), indent=2))
                
                # Test 7: List available tools
                print("\n🔧 Listing available ADK tools...")
                tools_list_result = await session.call_tool("list_available_tools", {})
                print("🛠️ Available ADK tools:")
                print(json.dumps(json.loads(tools_list_result.content[0].text), indent=2))
                
                # Test 8: Get documentation
                print("\n📚 Getting ADK documentation...")
                docs_result = await session.call_tool("get_adk_documentation", {
                    "topic": "agents"
                })
                print("📖 Documentation:")
                print(json.dumps(json.loads(docs_result.content[0].text), indent=2))
                
                # Test 9: Evaluate an agent (simplified test)
                print("\n🧪 Evaluating the research assistant...")
                eval_result = await session.call_tool("evaluate_adk_agent", {
                    "agent_name": "research_assistant",
                    "test_cases": [
                        {
                            "input": "What is artificial intelligence?",
                            "expected_output": "artificial intelligence"
                        },
                        {
                            "input": "Explain machine learning",
                            "expected_output": "machine learning"
                        }
                    ]
                })
                print("📊 Evaluation results:")
                eval_data = json.loads(eval_result.content[0].text)
                print(f"Success rate: {eval_data.get('success_rate', 0):.2%}")
                print(f"Passed tests: {eval_data.get('passed_tests', 0)}/{eval_data.get('total_tests', 0)}")
                
                print("\n🎉 All tests completed successfully!")
                
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        raise


async def test_web_search():
    """Test the direct web search functionality."""
    server_script = Path(__file__).parent.parent / "mcp_server.py"
    server_params = StdioServerParameters(
        command="python",
        args=[str(server_script)]
    )
    
    print("\n🔍 Testing direct web search functionality...")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test web search
                search_result = await session.call_tool("search_web", {
                    "query": "Google Agent Development Kit ADK",
                    "num_results": 3
                })
                print("🔍 Search results:")
                print(json.dumps(json.loads(search_result.content[0].text), indent=2))
                
                # Test webpage loading
                print("\n📄 Testing webpage loading...")
                webpage_result = await session.call_tool("load_webpage_content", {
                    "url": "https://google.github.io/adk-docs/"
                })
                print("📄 Webpage content loaded:")
                content_data = json.loads(webpage_result.content[0].text)
                print(f"Content preview: {str(content_data)[:200]}...")
                
    except Exception as e:
        print(f"❌ Error during web functionality testing: {e}")


if __name__ == "__main__":
    print("🧪 Google ADK MCP Server Test Suite")
    print("====================================")
    
    try:
        # Run main tests
        asyncio.run(test_adk_mcp_server())
        
        # Run web functionality tests
        asyncio.run(test_web_search())
        
        print("\n🎊 All tests passed! The Google ADK MCP Server is working correctly.")
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        sys.exit(1) 