from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from semantic_kernel.functions import kernel_function
from pydantic import Field
import os
import asyncio
from  pathlib import Path
from typing import Annotated

from dotenv import load_dotenv


#main functiond definition

async def main():

     # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

     # Load the expnses data file
    script_dir = Path(__file__).parent
    file_path = script_dir / 'data.txt'
    with file_path.open('r') as file:
        data = file.read() + "\n"

     # Ask for a prompt
    user_prompt = input(f"Here is the expenses data in your file:\n\n{data}\n\nWhat would you like me to do with it?\n\n")

    print("You entered : ", user_prompt)
    
    # Run the async agent code
    await process_expenses_data (user_prompt, data)


async def process_expenses_data(prompt, expense_data):
    load_dotenv()
    ai_agent_settings = AzureAIAgentSettings()

    creds = DefaultAzureCredential(exclude_environment_credential=True,exclude_manage_identity_credential=True)
    project_client = AzureAIAgent.create_client(credential=creds)

    # define an AI Agent that sends expense claim
    expense_agent_def = await project_client.agents.create_agent(
                model = ai_agent_settings.model_deployment_name,
                name="expenses_agent",
                instructions = """ you are an AI Assistant for expense claim submission.
                                When a user submits expenses data and requests an expense claim, use the plug-in function to send an email to expense@contoso.com with the subject 'Expense Claim submitted' and the body contains the itemized expense claim with total
                                then confirm to the user that you have done so."""
        )
    
    # create a semantic kernel agent
    expenses_agent = AzureAIAgent(
            client = project_client,
            definition=expense_agent_def,
            plugins=[EmailPlugin()]
        )
    
    thread: AzureAIAgentThread | None = None
    try:
            prompt_messages = [f"{prompt}: {expense_data}"]
            response = await expenses_agent.get_response(prompt_messages, thread=thread)
            print(f"\n# {response.name}: \n {response}")
    except Exception as e:
            print(e)
    finally:
            await thread.delete() if thread else None
            await project_client.agents.delete_agent(expenses_agent.id)


# Create a tool function for the email functionality
class EmailPlugin:
    """
    to send email
    """
    @kernel_function(description="sends an email")
    def send_email(self, 
                   To: Annotated[str, "sends email to"],
                   Subject: Annotated[str, "email subject"],
                   body: Annotated[str, "email body"]):
        print("To email id: ", To)
        print("email subject: ", Subject)
        print("email body: ", body)


if __name__ == "__main__":
    asyncio.run(main())

    

