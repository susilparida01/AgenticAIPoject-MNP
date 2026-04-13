"""
This module provides a configuration class for creating McpWorkbench instances.

The McpConfig class contains static methods for creating McpWorkbench instances 
for different tools like PostgreSQL, REST API and SOAP API. Each method 
configures the necessary parameters for the StdioServer and returns a 
McpWorkbench instance.
"""
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench
from libs.config_reader import ConfigReader

class McpConfig:
    """
    A configuration class for creating McpWorkbench instances.
    """
    @staticmethod
    def get_postgres_workbench():
        """
        Get a PostgreSQL MCP workbench instance.
        """
        postgres_server_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-postgres",
                ConfigReader.get_postgres_url()
            ] )
        return McpWorkbench( server_params=postgres_server_params )

    @staticmethod
    def get_rest_api_workbench():
        """
        Get a REST API MCP workbench instance.
        """
        rest_api_server_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "dkmaker-mcp-rest-api"
            ],
            env={
                "REST_BASE_URL": ConfigReader.get_rest_base_url(),
                "HEADER_Accept": "application/json"
            } )
        return McpWorkbench( server_params=rest_api_server_params )

    @staticmethod
    def get_soap_api_workbench():
        """
        Get a SOAP API MCP workbench instance.
        """
        soap_api_server_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "mcp-soap-server"
            ],
            env={
                "SOAP_WSDL_URL": ConfigReader.get_soap_wsdl_url()
            } )
        return McpWorkbench( server_params=soap_api_server_params )

    @staticmethod
    def get_playwright_workbench():
        """
        Get a Playwright MCP workbench instance.
        """
        headless = ConfigReader.get_playwright_headless()
        headless_str = "true" if headless else "false"
        print(f"[McpConfig] PLAYWRIGHT_HEADLESS={headless_str} (from config.properties)")

        playwright_server_params = StdioServerParams(
            command="npx",
            args=["-y", "@playwright/mcp@latest", "--browser", "chrome", "--no-sandbox"],
            env={
                "PLAYWRIGHT_HEADLESS": headless_str
            },
            read_timeout_seconds=60
        )
        return McpWorkbench( server_params=playwright_server_params )


####################################################################################

# mcp =  McpConfig()
# postgres_workbench = mcp.get_postgres_workbench()
# rest_api_workbench = mcp.get_rest_api_workbench()
# soap_api_workbench = mcp.get_soap_api_workbench()
# playwright_workbench = mcp.get_playwright_workbench()
