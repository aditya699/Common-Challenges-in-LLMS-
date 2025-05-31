"""
graph_rag_chat.py
NL question ➜ Cypher ➜ Neo4j ➜ English answer   (OpenAI Responses API)
pip install openai neo4j python-dotenv
"""

import os, json
from dotenv import load_dotenv
from neo4j import GraphDatabase
import openai

# ========= Environment / Clients =========
load_dotenv()                                              # .env → OPENAI_API_KEY, NEO4J_PASSWORD
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

NEO4J_URI      = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# ========= Neo4j helper =========
def run_cypher(query: str):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as s:
        return [r.data() for r in s.run(query)]

# ========= Tool schema (top-level) =========
TOOLS = [{
    "type": "function",
    "name": "query_graph",
    "description": "Generate a Cypher query for the Neo4j org chart.",
    "parameters": {
        "type": "object",
        "properties": {
            "cypher": {
                "type": "string",
                "description": "Cypher query that follows the schema"
            }
        },
        "required": ["cypher"],
        "additionalProperties": False
    },
    "strict": True
}]

# ========= Prompts =========
SCHEMA_PROMPT = """
You translate organisational questions into Cypher for a Neo4j graph.

Nodes
  Employee  : name, role
  Task      : name
  Initiative: name
  Team      : name
Rels
  (Employee)-[:REPORTS_TO]->(Employee)
  (Employee)-[:WORKS_ON]->(Task)
  (Task)-[:PART_OF]->(Initiative)
  (Employee)-[:MEMBER_OF]->(Team)

Return ONLY the Cypher.
"""

SUMMARY_PROMPT = """
You are a helpful assistant. Given the JSON tool output, answer the user's
question in plain English. Do NOT return Cypher or code. If the list is
empty, say you couldn’t find an answer.
"""

# ========= Main function =========
def ask(question: str):
    # ---- Round 1: get Cypher ----
    first = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SCHEMA_PROMPT},
            {"role": "user",   "content": question}
        ],
        tools=TOOLS
    )

    tool_call = next(item for item in first.output if item.type == "function_call")
    cypher = json.loads(tool_call.arguments)["cypher"]
    print("\nGenerated Cypher:\n", cypher)

    # ---- Run Cypher ----
    result = run_cypher(cypher)
    print("\nGraph result:\n", json.dumps(result, indent=2))

    # ---- Round 2: English answer ----
    second = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user",   "content": question},
            tool_call,
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(result)
            }
        ],
        tools=TOOLS
    )

    print("\nAnswer:\n", second.output_text)
    return second.output_text

# ========= Demo =========
if __name__ == "__main__":
    ask("Who is working on Foundational Modelling?")
