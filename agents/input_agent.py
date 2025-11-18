# Authors: Emily Liang 79453973, 
# Purpose: Receives requirements from UI and sends them to CodeAgent.

class InputAgent:
	def __init__(self, mcp_client):
		self.mcp = mcp_client

	def parse_requirements(self, raw_text: str) -> dict:
		"""
		Parse the raw user requirements text into a structured spec.

		Args: 
			raw_text: unstructured functional reqs from UI
		Returns:
			a dict including the structured requirement text
		"""
		return {"requirements": raw_text.strip()}