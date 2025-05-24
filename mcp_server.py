#!/usr/bin/env python3
"""
Google ADK MCP Server

This MCP server exposes Google Agent Development Kit (ADK) functionality
to MCP clients, allowing them to create, configure, and run AI agents
with ADK's powerful tooling ecosystem.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

# Import version information
try:
    from version import __version__, get_version
except ImportError:
    __version__ = "1.0.0"
    get_version = lambda: __version__

# Check for required dependencies and provide helpful error messages
try:
    # MCP imports
    import mcp.types as types
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    import mcp.server.stdio
except ImportError as e:
    print("❌ Error: MCP (Model Context Protocol) library not found.")
    print("Please install it with: pip install mcp")
    print("Note: MCP requires Python 3.10 or higher.")
    sys.exit(1)

try:
    # ADK imports
    from google.adk.agents import LlmAgent, Agent
    from google.adk.tools import (
        FunctionTool, 
        google_search,
        load_web_page,
        agent_tool,
    )
    from google.adk.tools.mcp_tool import MCPToolset
    from google.adk.sessions import InMemorySessionService
    from google.adk.artifacts import InMemoryArtifactService
    from google.adk.runners import Runner
    from google.genai import types as genai_types
    from google.adk.evaluation import evaluator
except ImportError as e:
    print("❌ Error: Google ADK library not found.")
    print("Please install it with: pip install google-adk")
    print(f"Detailed error: {e}")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google-adk-mcp-server")

# Global state to store created agents and sessions
AGENTS: Dict[str, Any] = {}
SESSIONS: Dict[str, Any] = {}
SESSION_SERVICE = InMemorySessionService()
ARTIFACT_SERVICE = InMemoryArtifactService()

# Initialize the MCP server
server = Server("google-adk-mcp-server")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools provided by this MCP server.
    """
    return [
        types.Tool(
            name="create_adk_agent",
            description="Create a new Google ADK agent with specified configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the agent"
                    },
                    "model": {
                        "type": "string", 
                        "description": "Model to use (e.g., 'gemini-2.0-flash', 'gemini-1.5-pro')",
                        "default": "gemini-2.0-flash"
                    },
                    "instruction": {
                        "type": "string",
                        "description": "System instruction for the agent"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of what the agent does"
                    },
                    "tools": {
                        "type": "array",
                        "description": "List of tool names to include with the agent",
                        "items": {"type": "string"},
                        "default": []
                    }
                },
                "required": ["name", "instruction"]
            }
        ),
        types.Tool(
            name="list_adk_agents",
            description="List all created ADK agents",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="get_adk_agent_info", 
            description="Get detailed information about a specific ADK agent",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "Name of the agent to get info for"
                    }
                },
                "required": ["agent_name"]
            }
        ),
        types.Tool(
            name="run_adk_agent",
            description="Run an ADK agent with a user message and get the response",
            inputSchema={
                "type": "object", 
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "Name of the agent to run"
                    },
                    "message": {
                        "type": "string",
                        "description": "User message to send to the agent"
                    },
                    "session_id": {
                        "type": "string",
                        "description": "Session ID to maintain conversation history (optional)",
                        "default": "default"
                    },
                    "user_id": {
                        "type": "string", 
                        "description": "User ID for the session",
                        "default": "user"
                    }
                },
                "required": ["agent_name", "message"]
            }
        ),
        types.Tool(
            name="list_available_tools",
            description="List all available ADK tools that can be added to agents", 
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="evaluate_adk_agent",
            description="Evaluate an ADK agent using a test dataset",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "Name of the agent to evaluate"
                    },
                    "test_cases": {
                        "type": "array",
                        "description": "Array of test cases with input and expected output",
                        "items": {
                            "type": "object",
                            "properties": {
                                "input": {"type": "string"},
                                "expected_output": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["agent_name", "test_cases"]
            }
        ),
        types.Tool(
            name="create_multi_agent_system",
            description="Create a multi-agent system with a coordinator and sub-agents",
            inputSchema={
                "type": "object",
                "properties": {
                    "coordinator_name": {
                        "type": "string",
                        "description": "Name for the coordinator agent"
                    },
                    "coordinator_instruction": {
                        "type": "string", 
                        "description": "Instruction for the coordinator agent"
                    },
                    "sub_agents": {
                        "type": "array",
                        "description": "List of sub-agent names to include",
                        "items": {"type": "string"}
                    },
                    "model": {
                        "type": "string",
                        "description": "Model to use for the coordinator",
                        "default": "gemini-2.0-flash"
                    }
                },
                "required": ["coordinator_name", "coordinator_instruction", "sub_agents"]
            }
        ),
        types.Tool(
            name="add_mcp_tools_to_agent",
            description="Add MCP tools from external servers to an existing ADK agent",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "Name of the agent to add tools to"
                    },
                    "mcp_server_command": {
                        "type": "string",
                        "description": "Command to run the MCP server (e.g., 'npx')"
                    },
                    "mcp_server_args": {
                        "type": "array", 
                        "description": "Arguments for the MCP server command",
                        "items": {"type": "string"}
                    },
                    "tool_filter": {
                        "type": "array",
                        "description": "Optional list of specific tools to include",
                        "items": {"type": "string"},
                        "default": []
                    }
                },
                "required": ["agent_name", "mcp_server_command", "mcp_server_args"]
            }
        ),
        types.Tool(
            name="search_web",
            description="Perform a web search using Google Search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="load_webpage_content",
            description="Load and extract content from a webpage URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the webpage to load"
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="get_adk_documentation",
            description="Get information about ADK features, capabilities, and usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to get documentation for (agents, tools, evaluation, deployment, etc.)"
                    }
                },
                "required": ["topic"]
            }
        ),
        types.Tool(
            name="get_server_version",
            description="Get version information for the Google ADK MCP Server",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """Handle tool execution requests."""
    try:
        if name == "create_adk_agent":
            return await create_adk_agent(**arguments)
        elif name == "list_adk_agents":
            return await list_adk_agents(**arguments)
        elif name == "get_adk_agent_info":
            return await get_adk_agent_info(**arguments)
        elif name == "run_adk_agent":
            return await run_adk_agent(**arguments)
        elif name == "list_available_tools":
            return await list_available_tools(**arguments)
        elif name == "evaluate_adk_agent":
            return await evaluate_adk_agent(**arguments)
        elif name == "create_multi_agent_system":
            return await create_multi_agent_system(**arguments)
        elif name == "add_mcp_tools_to_agent":
            return await add_mcp_tools_to_agent(**arguments)
        elif name == "search_web":
            return await search_web(**arguments)
        elif name == "load_webpage_content":
            return await load_webpage_content(**arguments)
        elif name == "get_adk_documentation":
            return await get_adk_documentation(**arguments)
        elif name == "get_server_version":
            return await get_server_version(**arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]

async def create_adk_agent(name: str, instruction: str, model: str = "gemini-2.0-flash", 
                         description: str = "", tools: List[str] = None) -> List[types.TextContent]:
    """Create a new ADK agent."""
    if tools is None:
        tools = []
    
    # Build tools list
    agent_tools = []
    # Import the actual load_web_page function
    from google.adk.tools.load_web_page import load_web_page as load_web_page_func
    
    available_tools = {
        "google_search": google_search,  # Already a tool instance
        "load_web_page": FunctionTool(load_web_page_func),  # Function wrapped in FunctionTool
    }
    
    for tool_name in tools:
        if tool_name in available_tools:
            agent_tools.append(available_tools[tool_name])
        else:
            logger.warning(f"Unknown tool: {tool_name}")
    
    # Create the agent
    agent = LlmAgent(
        name=name,
        model=model,
        instruction=instruction,
        description=description,
        tools=agent_tools
    )
    
    # Store the agent
    AGENTS[name] = {
        "agent": agent,
        "config": {
            "name": name,
            "model": model, 
            "instruction": instruction,
            "description": description,
            "tools": tools
        }
    }
    
    result = {
        "status": "success",
        "message": f"Successfully created agent '{name}'",
        "agent": {
            "name": name,
            "model": model,
            "description": description,
            "tools_count": len(agent_tools)
        }
    }
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def list_adk_agents() -> List[types.TextContent]:
    """List all created ADK agents."""
    agents_info = []
    for name, agent_data in AGENTS.items():
        config = agent_data["config"]
        agents_info.append({
            "name": name,
            "model": config["model"],
            "description": config["description"],
            "tools": config["tools"]
        })
    
    result = {
        "status": "success",
        "agents": agents_info,
        "total_count": len(agents_info)
    }
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def get_adk_agent_info(agent_name: str) -> List[types.TextContent]:
    """Get detailed information about a specific ADK agent."""
    if agent_name not in AGENTS:
        return [types.TextContent(
            type="text", 
            text=json.dumps({"error": f"Agent '{agent_name}' not found"})
        )]
    
    agent_data = AGENTS[agent_name]
    config = agent_data["config"]
    
    result = {
        "status": "success",
        "agent": {
            "name": config["name"],
            "model": config["model"],
            "instruction": config["instruction"],
            "description": config["description"],
            "tools": config["tools"],
            "created": True
        }
    }
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def run_adk_agent(agent_name: str, message: str, session_id: str = "default", 
                       user_id: str = "user") -> List[types.TextContent]:
    """Run an ADK agent with a user message."""
    if agent_name not in AGENTS:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"Agent '{agent_name}' not found"})
        )]
    
    try:
        agent = AGENTS[agent_name]["agent"]
        
        # Create or get session
        session_key = f"{agent_name}_{session_id}"
        if session_key not in SESSIONS:
            session = await SESSION_SERVICE.create_session(
                state={}, 
                app_name=f"adk-mcp-{agent_name}",
                user_id=user_id
            )
            SESSIONS[session_key] = session
        else:
            session = SESSIONS[session_key]
        
        # Create runner
        runner = Runner(
            app_name=f"adk-mcp-{agent_name}",
            agent=agent,
            session_service=SESSION_SERVICE,
            artifact_service=ARTIFACT_SERVICE
        )
        
        # Create message content
        content = genai_types.Content(
            role='user',
            parts=[genai_types.Part(text=message)]
        )
        
        # Run the agent
        response_events = []
        async for event in runner.run_async(
            session_id=session.id,
            user_id=user_id,
            new_message=content
        ):
            response_events.append(event)
        
        # Extract the final response
        final_response = ""
        for event in response_events:
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text'):
                        final_response += part.text
        
        result = {
            "status": "success",
            "agent_name": agent_name,
            "user_message": message,
            "agent_response": final_response,
            "session_id": session_id,
            "events_count": len(response_events)
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        logger.error(f"Error running agent {agent_name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"Failed to run agent: {str(e)}"})
        )]

async def list_available_tools() -> List[types.TextContent]:
    """List all available ADK tools."""
    available_tools = {
        "google_search": {
            "name": "google_search",
            "description": "Search the web using Google Search API",
            "type": "function_tool"
        },
        "load_web_page": {
            "name": "load_web_page", 
            "description": "Load and extract content from web pages",
            "type": "function_tool"
        },
        "agent_tool": {
            "name": "agent_tool",
            "description": "Tool that wraps another agent as a tool",
            "type": "agent_tool"
        }
    }
    
    result = {
        "status": "success",
        "available_tools": available_tools,
        "total_count": len(available_tools)
    }
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def evaluate_adk_agent(agent_name: str, test_cases: List[Dict[str, str]]) -> List[types.TextContent]:
    """Evaluate an ADK agent using test cases."""
    if agent_name not in AGENTS:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"Agent '{agent_name}' not found"})
        )]
    
    # This is a simplified evaluation - in practice you'd want more sophisticated metrics
    results = []
    agent = AGENTS[agent_name]["agent"]
    
    for i, test_case in enumerate(test_cases):
        try:
            # Run the agent with test input
            session = await SESSION_SERVICE.create_session(
                state={},
                app_name=f"eval-{agent_name}",
                user_id="evaluator"
            )
            
            runner = Runner(
                app_name=f"eval-{agent_name}",
                agent=agent,
                session_service=SESSION_SERVICE,
                artifact_service=ARTIFACT_SERVICE
            )
            
            content = genai_types.Content(
                role='user',
                parts=[genai_types.Part(text=test_case["input"])]
            )
            
            response_text = ""
            async for event in runner.run_async(
                session_id=session.id,
                user_id="evaluator", 
                new_message=content
            ):
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            response_text += part.text
            
            # Simple evaluation - check if expected output is in response
            passed = test_case["expected_output"].lower() in response_text.lower()
            
            results.append({
                "test_case": i + 1,
                "input": test_case["input"],
                "expected": test_case["expected_output"],
                "actual": response_text,
                "passed": passed
            })
            
        except Exception as e:
            results.append({
                "test_case": i + 1,
                "input": test_case["input"],
                "expected": test_case["expected_output"],
                "actual": f"Error: {str(e)}",
                "passed": False
            })
    
    passed_count = sum(1 for r in results if r["passed"])
    
    evaluation_result = {
        "status": "success",
        "agent_name": agent_name,
        "total_tests": len(test_cases),
        "passed_tests": passed_count,
        "success_rate": passed_count / len(test_cases) if test_cases else 0,
        "results": results
    }
    
    return [types.TextContent(type="text", text=json.dumps(evaluation_result, indent=2))]

async def create_multi_agent_system(coordinator_name: str, coordinator_instruction: str,
                                  sub_agents: List[str], model: str = "gemini-2.0-flash") -> List[types.TextContent]:
    """Create a multi-agent system with coordinator and sub-agents."""
    # Check if all sub-agents exist
    missing_agents = [name for name in sub_agents if name not in AGENTS]
    if missing_agents:
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "error": f"Missing sub-agents: {missing_agents}. Create them first."
            })
        )]
    
    # Get sub-agent instances
    sub_agent_instances = [AGENTS[name]["agent"] for name in sub_agents]
    
    # Create coordinator agent
    coordinator = LlmAgent(
        name=coordinator_name,
        model=model,
        instruction=coordinator_instruction,
        description=f"Coordinator agent managing {len(sub_agents)} sub-agents",
        sub_agents=sub_agent_instances
    )
    
    # Store the coordinator
    AGENTS[coordinator_name] = {
        "agent": coordinator,
        "config": {
            "name": coordinator_name,
            "model": model,
            "instruction": coordinator_instruction,
            "description": f"Multi-agent coordinator with {len(sub_agents)} sub-agents",
            "sub_agents": sub_agents,
            "type": "multi_agent_coordinator"
        }
    }
    
    result = {
        "status": "success",
        "message": f"Successfully created multi-agent system '{coordinator_name}'",
        "coordinator": {
            "name": coordinator_name,
            "model": model,
            "sub_agents": sub_agents,
            "sub_agent_count": len(sub_agents)
        }
    }
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def add_mcp_tools_to_agent(agent_name: str, mcp_server_command: str,
                               mcp_server_args: List[str], tool_filter: List[str] = None) -> List[types.TextContent]:
    """Add MCP tools from external servers to an existing ADK agent."""
    if agent_name not in AGENTS:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"Agent '{agent_name}' not found"})
        )]
    
    try:
        from mcp import StdioServerParameters
        
        # Create MCPToolset
        mcp_toolset = MCPToolset(
            connection_params=StdioServerParameters(
                command=mcp_server_command,
                args=mcp_server_args
            ),
            tool_filter=tool_filter if tool_filter else None
        )
        
        # Get the agent and add the toolset
        agent_data = AGENTS[agent_name]
        agent = agent_data["agent"]
        
        # Add the MCP toolset to the agent's tools
        if hasattr(agent, 'tools'):
            agent.tools.append(mcp_toolset)
        else:
            agent.tools = [mcp_toolset]
        
        # Update the stored config
        agent_data["config"]["mcp_tools"] = {
            "command": mcp_server_command,
            "args": mcp_server_args,
            "filter": tool_filter
        }
        
        result = {
            "status": "success",
            "message": f"Successfully added MCP tools to agent '{agent_name}'",
            "mcp_server": {
                "command": mcp_server_command,
                "args": mcp_server_args,
                "filter": tool_filter
            }
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        logger.error(f"Error adding MCP tools to agent {agent_name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"Failed to add MCP tools: {str(e)}"})
        )]

async def search_web(query: str, num_results: int = 5) -> List[types.TextContent]:
    """Perform a web search using Google Search."""
    try:
        # google_search is already a tool instance
        result = await google_search.run_async(
            args={"query": query, "num_results": num_results},
            tool_context=None
        )
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"Search failed: {str(e)}"})
        )]

async def load_webpage_content(url: str) -> List[types.TextContent]:
    """Load and extract content from a webpage."""
    try:
        # Import and wrap the load_web_page function
        from google.adk.tools.load_web_page import load_web_page as load_web_page_func
        webpage_tool = FunctionTool(load_web_page_func)
        result = await webpage_tool.run_async(
            args={"url": url},
            tool_context=None
        )
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"Failed to load webpage: {str(e)}"})
        )]

async def get_adk_documentation(topic: str) -> List[types.TextContent]:
    """Get information about ADK features and capabilities."""
    docs = {
        "agents": {
            "description": "ADK supports multiple types of agents",
            "types": [
                "LlmAgent - Basic LLM-powered agent",
                "SequentialAgent - Runs sub-agents in sequence", 
                "ParallelAgent - Runs sub-agents in parallel",
                "LoopAgent - Runs sub-agents in a loop until condition met",
                "CustomAgent - Build your own agent logic"
            ],
            "features": [
                "Multi-agent systems",
                "Tool integration",
                "Memory and state management",
                "Streaming support",
                "Evaluation capabilities"
            ]
        },
        "tools": {
            "description": "ADK provides a rich ecosystem of tools",
            "categories": [
                "Built-in tools (google_search, load_web_page, etc.)",
                "Google Cloud tools (BigQuery, Vertex AI, etc.)",
                "Third-party tools (LangChain, CrewAI)",
                "MCP tools (Model Context Protocol)",
                "OpenAPI tools",
                "Custom function tools"
            ],
            "features": [
                "Authentication support",
                "Async execution",
                "Tool context and state",
                "Error handling"
            ]
        },
        "deployment": {
            "description": "ADK supports multiple deployment options",
            "options": [
                "Local development with 'adk web'",
                "Google Cloud Run",
                "Google Kubernetes Engine (GKE)",
                "Vertex AI Agent Engine"
            ],
            "features": [
                "Containerization support",
                "Environment configuration",
                "Scaling capabilities",
                "Monitoring and logging"
            ]
        },
        "evaluation": {
            "description": "ADK provides comprehensive evaluation capabilities",
            "features": [
                "Automated testing with test datasets",
                "Performance metrics",
                "Comparison between agent versions",
                "Custom evaluation criteria",
                "Integration with development workflow"
            ]
        }
    }
    
    if topic.lower() in docs:
        result = {
            "status": "success",
            "topic": topic,
            "documentation": docs[topic.lower()]
        }
    else:
        result = {
            "status": "success",
            "available_topics": list(docs.keys()),
            "message": f"Topic '{topic}' not found. Available topics listed above."
        }
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def get_server_version() -> List[types.TextContent]:
    """Get version information for the Google ADK MCP Server."""
    try:
        from version import get_version_info
        version_info = get_version_info()
    except ImportError:
        version_info = {
            "major": 1,
            "minor": 0,
            "patch": 0
        }
    
    result = {
        "status": "success",
        "server_name": "Google ADK MCP Server",
        "version": __version__,
        "version_info": version_info,
        "mcp_protocol": "1.0",
        "description": "MCP server exposing Google Agent Development Kit functionality",
        "capabilities": [
            "Agent creation and management",
            "Multi-agent systems",
            "Tool integration (Google Search, web scraping, MCP tools)",
            "Agent evaluation",
            "Session management",
            "Real-time agent execution"
        ],
        "supported_models": [
            "gemini-2.0-flash",
            "gemini-1.5-pro", 
            "gemini-1.5-flash"
        ],
        "documentation": "https://github.com/your-username/google-adk-mcp-server"
    }
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def main():
    """Main function to run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Google ADK MCP Server starting...")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="google-adk-mcp-server",
                server_version=__version__,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1) 