import logging
from typing import Any, List, Mapping, Optional, Sequence
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core.tools import Workbench, ToolSchema, ToolResult, BaseTool, TextResultContent
from framework.mcp_config.mcp_config import McpConfig

logger = logging.getLogger(__name__)

class LocalToolWorkbench(Workbench):
    """
    A local workbench to wrap standard AutoGen tools.
    """
    def __init__(self, tools: Optional[List[BaseTool]] = None):
        super().__init__()
        self._tools = {tool.name: tool for tool in (tools or [])}

    async def list_tools(self) -> List[ToolSchema]:
        """List the tool schemas in this workbench."""
        return [tool.schema for tool in self._tools.values()]

    async def call_tool(
        self,
        name: str,
        arguments: Mapping[str, Any] | None = None,
        cancellation_token: Optional[CancellationToken] = None,
        call_id: str | None = None,
    ) -> ToolResult:
        """Call a tool in the local workbench."""
        if name not in self._tools:
            raise ValueError(f"Tool {name} not found")
        
        tool = self._tools[name]
        if cancellation_token is None:
            cancellation_token = CancellationToken()
            
        # Run the tool and wrap the result in a ToolResult if it isn't one already
        try:
            result = await tool.run_json(arguments or {}, cancellation_token)
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return ToolResult(
                name=name,
                result=[TextResultContent(content=str(e))],
                is_error=True
            )
        
        if isinstance(result, ToolResult):
            return result
            
        return ToolResult(
            name=name,
            result=[TextResultContent(content=str(result))],
            is_error=False
        )

    async def start(self) -> None: pass
    async def stop(self) -> None: pass
    async def reset(self) -> None: pass
    async def save_state(self) -> Mapping[str, Any]: return {}
    async def load_state(self, state: Mapping[str, Any]) -> None: pass

class AgentFactory:
    """
    Factory class for creating specialized agents with appropriate workbenches.
    """

    def __init__(self, model_client):
        self.model_client = model_client

    async def create_automation_agent(self, system_message: str) -> AssistantAgent:
        """Create an Automation agent with Playwright and Local workbenches."""
        playwright_workbench = McpConfig.get_playwright_workbench()
        local_workbench = LocalToolWorkbench()

        return AssistantAgent(
            name="AutomationAgent",
            model_client=self.model_client,
            workbench=[playwright_workbench, local_workbench],
            system_message=system_message
        )

    async def create_database_agent(self, system_message: str) -> AssistantAgent:
        """Create a Database agent with PostgreSQL workbench."""
        postgres_workbench = McpConfig.get_postgres_workbench()
        return AssistantAgent( 
            name="DatabaseAgent", 
            model_client=self.model_client,
            workbench=postgres_workbench,
            system_message=system_message 
        )

    async def create_api_agent(self, system_message: str) -> AssistantAgent:
        """Create an API agent with REST and SOAP workbenches."""
        rest_api_workbench = McpConfig.get_rest_api_workbench()
        soap_api_workbench = McpConfig.get_soap_api_workbench()
        
        return AssistantAgent(
            name="APIAgent",
            model_client=self.model_client,
            workbench=[rest_api_workbench, soap_api_workbench],
            system_message=system_message
        )
