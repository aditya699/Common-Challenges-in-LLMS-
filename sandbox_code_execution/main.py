'''
NOTE: This will show you how to create a simple app that can execute code (in a sandboxed environment).
This is a "Chat with your data" app: ask questions about your CSV and get Python code to answer them.
'''
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
client = OpenAI()

# Paths
SANDBOX_PATH = os.path.abspath("sandbox")
CODE_FILE = os.path.join(SANDBOX_PATH, "code.py")
DATA_FILE = os.path.join(SANDBOX_PATH, "data.csv")

print("🔗 Connected to OpenAI. Ready to generate code.")

# Get column names and a sample of the data to help the model
def get_data_overview(data_path, sample_rows=3):
    try:
        df = pd.read_csv(data_path)
        columns = list(df.columns)
        sample = df.head(sample_rows).to_dict(orient="records")
        return columns, sample
    except Exception as e:
        return [], []

while True:
    question = input("\n💬 Ask a question about your data (type 'exit' to quit): ")
    if question.lower() == "exit":
        break

    # Get data structure info
    columns, sample = get_data_overview(DATA_FILE)
    columns_str = ", ".join([f"'{col}'" for col in columns])
    sample_str = ""
    if sample:
        sample_str = "\nSample rows:\n" + "\n".join([str(row) for row in sample])

    # Improved prompt for a chat-with-data experience, now with data structure
    prompt = f"""
You are a helpful Python data analyst. The user will ask questions about the CSV file 'data.csv' in the current folder.
Here is information about the data:
- Columns: [{columns_str}]
{sample_str if sample_str else ''}

Your job is to write a single, complete Python script that:
- Imports pandas
- Loads 'data.csv'
- Answers the user's question below
- Uses only print() to show results (no display(), no markdown, no comments)

User's question: "{question}"

Example:
If the user asks: "What is the average value in the 'price' column?"
You should output:
import pandas as pd
df = pd.read_csv('data.csv')
print(df['price'].mean())

Remember:
- Do not use display(), markdown, or comments.
- Only output the code, nothing else.
"""

    # Send to OpenAI
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # use any GPT-4 model available
        messages=[{"role": "user", "content": prompt}]
    )

    # Get the code part
    code = response.choices[0].message.content.strip()

    # Save to code.py
    with open(CODE_FILE, "w") as f:
        f.write(code)

    print("\n✅ Code saved to sandbox/code.py")
    print("📄 Code Preview:\n")
    print(code)

    import subprocess

    print("\n🚀 Running code in Docker...")

    try:
        result = subprocess.run([
            "docker", "run",
            "--cpus=1.0", "--memory=512m",
            "-v", f"{SANDBOX_PATH}:/app",
            "--workdir", "/app",
            "sandbox-runner"
        ], capture_output=True, text=True, timeout=20)

        # Print the result
        print("\n📤 Output:\n")
        print(result.stdout)

        if result.stderr:
            print("\n Stderr (Warnings or Errors):\n")
            print(result.stderr)

    except subprocess.TimeoutExpired:
        print("\nExecution timed out.")

