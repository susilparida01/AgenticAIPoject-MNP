# Agentic Automation Project (MNP)

A modular framework for building specialized AI agents using AutoGen and the Model Context Protocol (MCP). This project enables agents to interact with PostgreSQL databases, REST APIs, SOAP services, and web browsers (via Playwright).

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Node.js & npm** (Required for MCP servers via `npx`)
- **uv** (Recommended for fast Python package management)

### 2. Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AgenticAIPoject-MNP
   ```

2. **Set up Virtual Environment:**
   Using `uv` (recommended):
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```
   Or using standard `venv`:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Playwright Browsers:**
   ```bash
   playwright install chromium
   ```

### 3. Configuration

1. **Configure Environment:**
   The project uses `config/config.properties` for configuration. This file is ignored by git for security.
   
   Create `config/config.properties` with the following template:
   ```properties
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   MODEL_NAME=gpt-4o

   # PostgreSQL Configuration
   POSTGRES_URL=postgresql://user:password@localhost:5432/database

   # REST API Configuration
   REST_BASE_URL=https://api.example.com

   # SOAP API Configuration
   SOAP_WSDL_URL=https://webservice.example.com/service?wsdl

   # Browser Configuration
   PLAYWRIGHT_HEADLESS=true
   ```

### 4. Project Structure

- `framework/agentfactory/`: Contains `AgentFactory` for creating specialized agents.
- `framework/mcp_config/`: MCP server configurations for Database, REST, and SOAP.
- `libs/`: Core utility classes like `ConfigReader`.
- `config/`: Configuration files (properties).

### 5. Basic Usage

```python
from framework.agentfactory.agentFactory import AgentFactory
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    # 1. Initialize Model Client
    client = OpenAIChatCompletionClient(model="gpt-4o")

    # 2. Create Factory
    factory = AgentFactory(model_client=client)

    # 3. Create a Database Agent
    db_agent = await factory.create_database_agent(
        system_message="You are a data analyst. Use the database to answer questions."
    )

    # 4. Create an API Agent
    api_agent = await factory.create_api_agent(
        system_message="You are an integration specialist. Use REST and SOAP tools."
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 🛠️ Development

- **Adding Tools:** Add new MCP servers in `framework/mcp_config/mcp_config.py`.
- **Custom Agents:** Define new agent creation logic in `framework/agentfactory/agentFactory.py`.
- **Config:** Update `libs/config_reader.py` if adding new keys to `config.properties`.
