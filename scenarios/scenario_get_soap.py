from framework.agentfactory.agentFactory import AgentFactory
from autogen_ext.models.openai import OpenAIChatCompletionClient
from libs.config_reader import ConfigReader
import asyncio
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

async def main():
    # 0. Load Configuration
    print("Loading configuration...")
    ConfigReader.load_to_environ()
    
    # 1. Initialize Model Client
    print("Initializing Model Client...")
    client = OpenAIChatCompletionClient(model=ConfigReader.get_model_name())

    # 2. Create Factory
    print("Creating Agent Factory...")
    factory = AgentFactory(model_client=client)

    # 3. Create an API Agent
    print("Creating API Agent...")
    api_agent = await factory.create_api_agent(
        system_message="You are an integration specialist. Use SOAP tools to interact with the WSDL."
    )
    
    # 4. Execute SOAP GET request (Fetch WSDL)
    wsdl_url = ConfigReader.get_soap_wsdl_url()
    
    if not wsdl_url:
        print("Error: SOAP_WSDL_URL not found in config.properties")
        return

    print(f"Executing SOAP GET request for: {wsdl_url}")
    
    # We ask the agent to fetch and describe the WSDL
    response = await api_agent.on_messages(
        [TextMessage(content=f"Please fetch the WSDL from {wsdl_url} and describe the available services and operations.", source="user")],
        cancellation_token=CancellationToken()
    )
    
    print("\n--- Agent Response ---")
    print(response.inner_messages[-1].content if response.inner_messages else response)
    
    # 5. Validation Section
    print("\n--- Validation Section ---")
    validation_passed = False
    for msg in response.inner_messages:
        content = getattr(msg, "content", "")
        # The tool output for soap_get should contain Status Code: 200
        if "Status Code: 200" in str(content):
            validation_passed = True
            print("Validation SUCCESS: Received HTTP 200 OK.")
            break
    
    if not validation_passed:
        print("Validation FAILED: Did not receive HTTP 200 OK.")
    
    print("----------------------\n")
    print("Scenario SOAP GET completed.")

if __name__ == "__main__":
    asyncio.run(main())
