from framework.agentfactory.agentFactory import AgentFactory
from autogen_ext.models.openai import OpenAIChatCompletionClient
from libs.config_reader import ConfigReader

async def main():
    # 0. Load Configuration
    print("Loading configuration...")
    ConfigReader.load_to_environ()
    
    # 1. Initialize Model Client
    print("Initializing Model Client...")
    client = OpenAIChatCompletionClient(model="gpt-4o")

    # 2. Create Factory
    print("Creating Agent Factory...")
    factory = AgentFactory(model_client=client)

    # 3. Create an API Agent
    print("Creating API Agent...")
    api_agent = await factory.create_api_agent(
        system_message="You are an integration specialist. Use REST and SOAP tools."
    )
    
    print("Scenario 01 completed successfully. Agents are ready.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())