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
        system_message="You are an integration specialist. Use SOAP tools to perform requests."
    )
    
    # 4. Execute SOAP POST request
    endpoint = ConfigReader.get_soap_endpoint_url()
    soap_body = ConfigReader.get_soap_payload()
    
    if not endpoint or not soap_body:
        print("Error: SOAP_ENDPOINT_URL or SOAP_PAYLOAD not found in config.properties")
        return

    print(f"Executing SOAP POST request to: {endpoint}")
    
    prompt = f"""Perform a SOAP POST request to {endpoint}.
Use the following SOAP envelope:
{soap_body}

Verify if the request was successful and report the response."""

    response = await api_agent.on_messages(
        [TextMessage(content=prompt, source="user")],
        cancellation_token=CancellationToken()
    )
    
    print("\n--- Agent Response ---")
    print(response.inner_messages[-1].content if response.inner_messages else response)
    
    # 5. Validation Section
    print("\n--- Validation Section ---")
    validation_passed = False
    for msg in response.inner_messages:
        content = getattr(msg, "content", "")
        # The tool output for soap_post should contain Status Code: 200
        if "Status Code: 200" in str(content):
            validation_passed = True
            print("Validation SUCCESS: Received HTTP 200 OK.")
            break
    
    if not validation_passed:
        print("Validation FAILED: Did not receive HTTP 200 OK.")
    
    print("----------------------\n")
    print("Scenario SOAP POST completed.")

if __name__ == "__main__":
    asyncio.run(main())
