# Authors: Emily Liang 79453973, 
# Purpose: centralize LLM integration between agents

import os
from openai import OpenAI

class MCPClient:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """
        Initialize MCPClient w/API key
        """
        # set API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please set api_key or OPENAI_API_KEY in your environment.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model # initialize model
	
    def call_model(self, prompt: str) -> dict:
        """
        Sends a prompt to LLM & returns structured data for usage tracking.
        
        Args:
            prompt: the text prompt to send to the LLM
        
        Returns: (dict)
            {
                "model": model name,
                "tokens": estimated_token_count,
                "response": generated_text
            }
        """
        try:
            response = self.client.chat.completions.create( # request to openai
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI coding assistant."},
                    {"role": "user", "content": prompt}
                ],
            )

            output = response.choices[0].message.content.strip() # get response
            num_tokens = response.usage.total_tokens # get total tokens used
        
            return { # return dict w model name, total tokens, & response
                "model": self.model,
                "tokens": num_tokens,
                "response": output
            }
        
        except Exception as e: # when calling model fails
            print(f"Error: {e}")
            return {
                "model": self.model,
                "tokens": 0,
                "response": ""
            }

# test methods
# mcp = MCPClient()
# res = mcp.call_model("Write a Python function that adds two numbers.")
# print(res)
# """{'model': 'gpt-4o-mini', 'tokens': 117, 
# 'response': 'Sure! Here is a simple Python function that adds two numbers:\n\n```python\ndef add_numbers(num1, num2):\n    return num1 + num2\n\n# Example usage:\nresult = add_numbers(5, 3)\nprint("The sum is:", result)  # Output: The sum is: 8\n```\n\nYou can call the `add_numbers` function with two numbers as arguments, and it will return their sum.'}"""