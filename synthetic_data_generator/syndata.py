'''
This file contains code to generate synthetic data for my Financial Sentiment Analysis Project
# NOTE: Will run this script in 3 terminals, each with different parameters to achieve parallel execution
'''

class_name=input("Enter the class for you which you want to generate data for: ")
link_to_file_for_examples=input("Enter the link to the file for examples: ")
examples=open(link_to_file_for_examples, "r")

from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List
import csv
import time
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

client=OpenAI()

class Example(BaseModel):
    example: List[str]

# Read examples once before the loop
examples_content = examples.read()
examples.close()

for iteration in range(40):
    print(f"Running iteration {iteration + 1}/40...")
    
    try:
        response = client.responses.parse(
            model="gpt-4.1-mini-2025-04-14",
            input=[
                {
                    "role": "system", 
                    "content": f"""You are an expert synthetic data generator specializing in financial sentiment analysis. 
                    
                        Your task is to generate high-quality synthetic examples for the '{class_name}' sentiment class based on the provided examples.

                        Requirements:
                        1. Generate exactly 100 diverse examples
                        2. Maintain the same sentiment polarity as the class
                        3. Vary sentence structure, length, and financial contexts
                        4. Include different financial domains (stocks, earnings, mergers, market performance, etc.)
                        5. Use realistic company names, financial figures, and market terminology
                        6. Ensure grammatical correctness and natural language flow
                        7. Avoid repetitive patterns or overly similar constructions
                        8. Cover Edge Cases along with the main cases

                        Focus on creating examples that would be challenging for sentiment analysis models while maintaining clear sentiment indicators."""
                                },
                {
                    "role": "user",
                    "content": f"""Based on these examples for the '{class_name}' class:

{examples_content}

Generate 100 new synthetic examples that follow the same sentiment pattern and financial context. 
Ensure variety in:
- Company types and industries
- Financial metrics and scenarios  
- Sentence complexity and structure
- Geographic markets and currencies
- Time periods and market conditions

Return only the examples in the specified format."""
                },
            ],
            text_format=Example,
        )

        # Pause for 10 seconds after the API call
        time.sleep(10)

        event = response.output_parsed
        # Save output to CSV file
        output_filename = f"synthetic_{class_name}_data.csv"
        file_exists = os.path.exists(output_filename)

        with open(output_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['text', 'sentiment'])  # Header row only if file doesn't exist
            for example in event.example:
                writer.writerow([example, class_name])

        print(f"Generated {len(event.example)} examples and saved to {output_filename}")

    except Exception as e:
        print(f"Error in iteration {iteration + 1}: {str(e)}")
        print("Continuing to next iteration...")
        continue

print(f"Completed all 100 iterations for {class_name} class!")
