# Authors: Emily Liang 79453973, 
# Purpose: Logs API calls and token usage per model, outputs the JSON report

import json
import os

class TrackingAgent:
	def __init__(self, file_path="usage_report.json"):
		"""
		Tracks the num of API calls & total tokens per model.
		"""
		self.file_path = file_path
		if os.path.exists(self.file_path): # if file exists, load its data
			with open(self.file_path, "r") as file:
				self.data = json.load(file)
		else: # file doesn't exist, create data structure
			self.data = {} #{"model1": {"numApiCalls": number, "totalTokens": number}, …}
	
	def record_model_call(self, mcp_output: dict) -> None:
		"""
		Gets the MCP model response & updates the tracker.

		Args:
			mcp_output: model output returned from call_model in mcp_client
		"""
		# update self.data with model name, numApiCalls, & totalTokens
		model_name = mcp_output["model"]
		total_tokens = mcp_output["tokens"]

		if model_name not in self.data:
			self.data[model_name] = {"numApiCalls": 0, "totalTokens": 0}
		
		self.data[model_name]["numApiCalls"] += 1
		self.data[model_name]["totalTokens"] += total_tokens

	def get_report(self) -> dict:
		"""
		Method to get the JSON-formatted report.
		"""
		return self.data

	def save_report(self) -> None:
		"""
		Save the model usage report in a JSON file.
		"""
		with open(self.file_path, "w") as file:
			json.dump(self.data, file, indent=4)

# test methods (copy into main.py)
# mcp = MCPClient()
# output = mcp.call_model("Write a Python function that adds two numbers.")
# print(output)
# tracking = TrackingAgent()
# tracking.record_model_call(output)
# tracking.save_report()

