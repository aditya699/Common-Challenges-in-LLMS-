'''
Before actually coding the agentic solution , we need a  sandbox enviornment to run it.

(FOR ROUTING AGENT)
NOTE:
1.We need a router to classify the user query into one of the following categories:
- 0: No code needed, answerable via LLM directly.
- 1: Simple code like top 5 rows, mean, count.(Only for data analysis tasks like top 5 rows, mean, count, etc.)
- 2: Large file, plotting, joins, or longer pandas processing.(Only for data analysis tasks like plotting, joins, etc.)
- 3: Requires web browsing and detailed report creation.(Only for tasks like creating a detailed report, etc.)

2.We should use Runner.run since we want overflow to be async.

3.Model choice is gpt-4.1-nano.(extremely cheap,fast and good for routing(You might want to fine tune it for this task in production))

4.Along with user prompt, we can pass metadata like file size, etc will help the llm choice better.

5.Note:This router is task specific and not general purpose.(This is foundation for my project every project needs a different router)

6.Your router can have a fallback mechanism to handle unexpected errors.

7.GPT 4.1 Nano is just a router do not use it for any other task.(even basic chat or code generation)
'''

import os
import asyncio
from dotenv import load_dotenv
from schemas import UserQuery
from prompts import ROUTER_PROMPT,GENERAL_PROMPT
from agents import Agent,Runner

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

agent = Agent(
    name="Router",
    instructions=ROUTER_PROMPT,
    output_type=UserQuery,
    model="gpt-4.1-nano"
)

agent_general=Agent(
    name="General",
    instructions=GENERAL_PROMPT,
    model="gpt-4o-mini"
)

async def main():
    history = ""
    print("Welcome to the AI Assistant. Type 'exit' to quit.")
    
    while True:
        # Get user input
        user_prompt = input("\nYou: ")
        
        # Update history with user input
        history += f"User: {user_prompt}\n"
        
        # Exit condition
        if user_prompt.lower() == "exit":
            print("Goodbye!")
            break
        
        # Implement retry logic (up to 3 attempts)
        max_retries = 3
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            try:
                # Route the query
                result = await Runner.run(agent, input=user_prompt + "\n\nPrevious conversation:\n" + history if history else user_prompt)
                history += f"Agent_Router: {result.final_output.output_type}\n"
                print("history: ",history)
                
                # Process based on output type
                if result.final_output.output_type == 0:
                    response = await Runner.run(agent_general, input=user_prompt + "\n\nPrevious conversation:\n" + history if history else user_prompt)
                    print(f"\nAI: {response.final_output}")
                    history += f"Agent_General: {response.final_output}\n"
                elif result.final_output.output_type == 1:
                    response = "I can help with simple data analysis like top 5 rows, mean, count. This feature is under development."
                    print(f"\nAI: {response}")
                    history += f"Agent_Simple_Analysis: {response}\n"
                elif result.final_output.output_type == 2:
                    response = "I can help with complex data analysis like plotting, joins, or longer pandas processing. This feature is under development."
                    print(f"\nAI: {response}")
                    history += f"Agent_Complex_Analysis: {response}\n"
                elif result.final_output.output_type == 3:
                    response = "I can help with web browsing and detailed report creation. This feature is under development."
                    print(f"\nAI: {response}")
                    history += f"Agent_Detailed_Report: {response}\n"
                else:
                    print("\nAI: I'm not sure how to handle that request.")
                    raise ValueError("Invalid output type received")
                
                success = True
                
            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"\nAI: I encountered an error. Let me try again...")
                else:
                    print(f"\nAI: I'm sorry, I couldn't process your request after {max_retries} attempts. Error: {e}")


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())