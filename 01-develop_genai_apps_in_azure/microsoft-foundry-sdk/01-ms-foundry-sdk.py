"""
Display all service connections available from the ms foundry project using ms foundry sdk (AIProjectClient) and DefaultAzureCredential
"""
# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
import os

load_dotenv()

# Microsoft Foundry project endpoint and model name
project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")

try:
    project_client = AIProjectClient(
        credential=DefaultAzureCredential(),
        endpoint=project_endpoint
    )

    connections = project_client.connections

    for con in connections.list():
        print(f"{con.name} and {con.type}")

except Exception as e:
    print(f"Error:{e}")