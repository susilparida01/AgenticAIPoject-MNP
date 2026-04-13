# AGENTS.md - Agentic Automation Framework Guide

## Project Architecture

This is a **modular AI agent framework** built on AutoGen for creating specialized agents that interact with multiple data sources and services. The core pattern is: **Model Client → AgentFactory → Specialized Agents → MCP Workbenches**.

### Key Components

1. **AgentFactory** (`framework/agentfactory/agentFactory.py`): Central factory class that creates three types of specialized agents:
   - `create_database_agent()` - PostgreSQL database queries
   - `create_api_agent()` - REST & SOAP API integrations
   - `create_automation_agent()` - Browser automation (Playwright)
   
2. **McpConfig** (`framework/mcp_config/mcp_config.py`): Configures Model Context Protocol (MCP) workbenches that spawn Node.js MCP servers via `npx` commands for:
   - PostgreSQL (via `@modelcontextprotocol/server-postgres`)
   - REST APIs (via `dkmaker-mcp-rest-api`)
   - SOAP APIs (via `mcp-soap-server`)
   - Playwright (via `@playwright/mcp@latest`)

3. **ConfigReader** (`libs/config_reader.py`): Centralized configuration management that reads `config/config.properties` with typed accessors for all environment-specific values.

4. **LocalToolWorkbench** (`framework/agentfactory/agentFactory.py`): Custom Workbench wrapper for standard AutoGen tools with proper async error handling and ToolResult wrapping.

### Critical Data Flow

```
User Code (scenario_*.py)
  ↓
create OpenAIChatCompletionClient
  ↓
instantiate AgentFactory(model_client)
  ↓
call factory.create_*_agent(system_message)
  ↓
AgentFactory retrieves workbench(es) from McpConfig
  ↓
McpConfig creates StdioServerParams (configures npx + MCP server args)
  ↓
Returns AssistantAgent with configured workbench
  ↓
Agent executes tools via MCP (spawns Node.js processes)
```

## Developer Workflows

### Setting Up the Development Environment

1. **Python environment**: `uv venv` or `python -m venv .venv`
2. **Activate**: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
3. **Install dependencies**: `uv pip install -r requirements.txt`
4. **Install Playwright browsers**: `playwright install chromium`

### Configuration Pattern

All external connections and credentials are managed through `config/config.properties`. **This file is gitignored** and must be created locally. Key sections:
- **OpenAI**: `OPENAI_API_KEY`, `MODEL_NAME`
- **Database**: `POSTGRES_URL`
- **APIs**: `REST_BASE_URL`, `SOAP_WSDL_URL`
- **Browser**: `PLAYWRIGHT_HEADLESS`, `BROWSER_URL`, `BROWSER_USERNAME`, `BROWSER_PASSWORD`

Access properties via `ConfigReader.get_property()` or typed accessors like `ConfigReader.get_postgres_url()`.

### Running Scenarios

Scenarios are example implementations in `scenarios/scenario_*.py`. Pattern:
```python
# 1. Create async main()
# 2. Initialize OpenAIChatCompletionClient
# 3. Create AgentFactory
# 4. Create specific agents via factory methods
# 5. Execute agent.run() or await in conversation loops
```

## Project-Specific Conventions

### Async/Await Pattern
**All agent factory methods are async**. Always use:
```python
agent = await factory.create_database_agent(system_message="...")
```

### Workbench Selection
- Agents are created with **single or multiple workbenches** via `workbench=` parameter (can be list)
- Each specialized agent includes the **specific workbenches it needs** (DB agent gets postgres, API agent gets REST+SOAP)
- Custom tools wrapped in `LocalToolWorkbench([tool1, tool2, ...])`

### Error Handling in Workbenches
`LocalToolWorkbench.call_tool()` **automatically catches exceptions** and wraps them in error ToolResults, preventing agent crashes on tool failures.

### Configuration Management
- Use `ConfigReader.get_bool_property()` for boolean flags (handles "true/1/yes/on" normalization)
- `ConfigReader.load_to_environ()` can load properties into `os.environ` if needed
- **Site-packages resolution** built-in for Windows/Unix venv paths (used by MCP servers)

## Integration Points & External Dependencies

### Node.js MCP Servers
Each workbench spawns a Node.js process via `npx` with **timeout configuration**. The Playwright workbench uses `read_timeout_seconds=60` (longest timeout) due to browser operations being slow.

### Environment Variables for MCP Servers
Passed via `env` dict in `StdioServerParams`:
- Playwright: `PLAYWRIGHT_HEADLESS` (set to "true"/"false" string)
- REST API: `REST_BASE_URL`, `HEADER_Accept` (JSON by default)
- SOAP API: `SOAP_WSDL_URL`

### AutoGen Version Requirement
Built on **AutoGen 0.7.5** with async-first API. All agent creation and execution must use async/await patterns.

## Adding New Capabilities

### To Add a New Workbench Type
1. Create static method in `McpConfig` class (e.g., `get_custom_workbench()`)
2. Define `StdioServerParams` with command, args, and env dict
3. Return `McpWorkbench(server_params=params)`
4. Create corresponding factory method in `AgentFactory`

### To Add Configuration Properties
1. Add property to `config/config.properties` with comment
2. Add typed accessor method to `ConfigReader` (e.g., `get_custom_setting()`)
3. Use throughout framework via `ConfigReader.get_custom_setting()`

## Common Patterns to Reference 

- **Database agent setup**: `framework/agentfactory/agentFactory.py` lines 86-91
- **Multi-workbench agent**: `framework/agentfactory/agentFactory.py` lines 93-102 (API agent with REST+SOAP)
- **Tool error wrapping**: `framework/agentfactory/agentFactory.py` lines 34-48
- **Config reading with fallback**: `libs/config_reader.py` lines 60-75

