'''
NOTE: This is a demo on how to use openai container to analyze a csv file.
(Rather than analyze the data, the demo is more towards how to use openai container to do anything i mean run python code and stuff)
'''


from openai import OpenAI
import os
import requests
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Check existing containers and find active ones
print("Checking existing containers...")
containers = client.containers.list()

# Find first active (running) container
active_container = None
for container in containers.data:
    print(f"Container {container.id}: {container.status}")
    if container.status == "running":
        active_container = container
        break

if active_container:
    container_id = active_container.id
    print(f"Using active container: {container_id}")
else:
    print("No active containers found. Creating new one...")
    container = client.containers.create(name="data-analysis-container")
    container_id = container.id
    print(f"Created new container: {container_id}")

# Step 2: Upload file
url = f"https://api.openai.com/v1/containers/{container_id}/files"
headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
files = {'file': ('data.csv', open('data.csv', 'rb'))}

response = requests.post(url, headers=headers, files=files)
file_path = response.json()['path']
print(f"File uploaded: {file_path}")

# Step 3: Analyze with code interpreter
response = client.responses.create(
    model="gpt-4.1-mini",
    tools=[{"type": "code_interpreter", "container": container_id}],
    tool_choice="required",
    input=f"Analyze CSV at '{file_path}'. How many rows?"
)

# Results
print(f"Answer: {response.output_text}")
print(f"Code executed:\n{response.output[0].code}")
print(f"Tokens used: {response.usage.total_tokens}")