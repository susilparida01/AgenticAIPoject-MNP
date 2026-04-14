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