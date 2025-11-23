# Authors: Emily Liang 79453973
# Purpose: Receives requirements from UI and sends them to CodeAgent.

import json, re
from client.mcp_client import MCPClient

class InputAgent:
	def __init__(self, mcp_client, usage_tracker):
		self.mcp = mcp_client
		self.usage_tracker = usage_tracker

	def parse_requirements(self, raw_text: str) -> dict:
		"""
		Parse the raw user requirements text into a structured spec using LLM.

		Args: 
			raw_text: unstructured functional reqs from UI
		Returns:
			a dict including the structured requirement text
		"""
		if not raw_text.strip(): # invalid raw text from user
			raise ValueError("Error: Requirements text is empty.")
		
		prompt = f"""
		Extract the requirements from the raw user text:{raw_text}. 
		Return in JSON format with the keys as numbered requirements 
		and values as a single requirement.
		"""
		mcp_output = self.mcp.call_model(prompt) # call LLM w/prompt
		
		# track agent call
		self.usage_tracker.record_agent_call("input_agent", mcp_output)
		self.usage_tracker.save_report()

		output_text = mcp_output["response"].strip() # get response & strip it

		# strip out any ``` and json
		output_text = re.sub(r"^```json\s*", "", output_text)
		output_text = re.sub(r"```$", "", output_text)

		if not output_text: # invalid output text from LLM
			raise ValueError("Error: LLM returned empty requirements.")

		try: # parse JSON str into dict
			requirements_dict = json.loads(output_text)
		except json.JSONDecodeError:
			raise ValueError(f"LLM output is not valid JSON: {output_text}")

		return {"requirements": requirements_dict}

# test methods (copy into main.py)
# mcp_client = MCPClient()
# input = InputAgent(mcp_client)
# raw_text = """
# The app should allow users to create an account using their email and password. 
# Users must be able to log in and log out securely. 
# There should be a password reset functionality via email. 
# The main dashboard should display user statistics like number of logins and recent activity. 
# The system should provide notifications for important events like messages or updates.
# """
# print(input.parse_requirements(raw_text))