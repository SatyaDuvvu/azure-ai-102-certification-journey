"""
build a chat app using ms foundry sdk leveraging open ai model and authentication as DefaultAzureCredential
"""
# Add refernces
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Microsoft Foundry project endpoint and model name
project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_NAME")


project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint
)


# Get a chat client
openai_client = project_client.get_openai_client(api_version="2024-10-21")

response = openai_client.chat.completions.create(
    messages=[ 
        {"role": "system", "content": "You are a helpful AI assistant that answers questions."},
        {"role": "user", "content": "which season is best to visit Spain?"}
        ],
        model=model_deployment,
        max_tokens=1024,
        temperature=1.0,
        top_p=1.0

)

completion = response.choices[0].message.content

print(f"Response: {completion}")

