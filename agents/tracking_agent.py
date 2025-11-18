# Authors: Emily Liang 79453973, 
# Purpose: Logs API calls and token usage per model, outputs the JSON report

class TrackingAgent:
	def __init__(self):
		"""
		Tracks the num of API calls & total tokens per model.
		"""
		self.data = {} #{"model1": {"numApiCalls": number, "totalTokens": number}, …}
	
	def record_model_call(self, mcp_output: dict) -> None:
		"""
		Gets the MCP model response & updates the tracker.

		Args:
			mcp_output: model output, including the name & usage data
		"""
		# get model response
		# update self.data with model name, numApiCalls, & totalTokens
		pass

	def get_report(self) -> dict:
		"""
		Method to get the JSON-formatted report.
		"""
		return self.data

	def save_report(self, file_path="usage_report.json"):
		"""
		Save the model usage report in a JSON file.
		"""
		pass