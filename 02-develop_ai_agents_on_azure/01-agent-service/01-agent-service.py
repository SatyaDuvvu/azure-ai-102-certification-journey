import os
from dotenv import load_dotenv
from typing import Any
from pathlib import Path


# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, CodeInterpreterTool, CodeInterpreterToolAuto


def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint= os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Display the data to be analyzed
    script_dir = Path(__file__).parent  # Get the directory of the script
    file_path = script_dir / 'data.txt'

    with file_path.open('r') as file:
        data = file.read() + "\n"
        print(data)

    # Connect to the AI Project and OpenAI clients
    with (
    DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True) as credential,
     AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
     project_client.get_openai_client() as openai_client
    ):
    

        # Upload the data file and create a CodeInterpreterTool
        # Upload the data file and create a CodeInterpreterTool
        file = openai_client.files.create(
            file=open(file_path, "rb"), purpose="assistants"
        )
        print(f"Uploaded {file.filename}")

        code_interpreter = CodeInterpreterTool(
            container=CodeInterpreterToolAuto(file_ids=[file.id])
        )

        

        # Define an agent that uses the CodeInterpreterTool
        # Define an agent that uses the CodeInterpreterTool
        agent = project_client.agents.create_version(
            agent_name="data-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="You are an AI agent that analyzes the data in the file that has been uploaded. Use Python to calculate statistical metrics as necessary.",
                tools=[code_interpreter],
            ),
        )
        print(f"Using agent: {agent.name}")
        

        # Create a conversation for the chat session
        # Create a conversation for the chat session # Thread
        conversation = openai_client.conversations.create()  
                

        # Loop until the user types 'quit'
        while True:
            # Get input text
            user_prompt = input("Enter a prompt (or type 'quit' to exit): ")
            if user_prompt.lower() == "quit":
                break
            if len(user_prompt) == 0:
                print("Please enter a prompt.")
                continue
            
            # Send a prompt to the agent
            # Send a prompt to the agent
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{"type": "message", "role": "user", "content": user_prompt}],
            )

            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
                input="",
            )
            

            # Check the response status for failures
            # Check the response status for failures
            if response.status == "failed":
                print(f"Response failed: {response.error}")
            

            # Show the latest response from the agent
            # Show the latest response from the agent
            print(f"Agent: {response.output_text}")
                        

        # Get the conversation history
        # Get the conversation history
        print("\nConversation Log:\n")
        items = openai_client.conversations.items.list(conversation_id=conversation.id)
        for item in items:
            if item.type == "message":
                print(f"item.content[0].type = {item.content[0].type}")
                role = item.role.upper()
                content = item.content[0].text
                print(f"{role}: {content}\n")


        # Clean up
        # Clean up
        openai_client.conversations.delete(conversation_id=conversation.id)
        print("Conversation deleted")

        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print("Agent deleted")


if __name__ == '__main__': 
    main()