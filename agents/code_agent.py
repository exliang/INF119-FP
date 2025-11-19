# Authors: Emily Liang 79453973, 
# Purpose: Generates runnable code modules based on the parsed/structured requirements

class CodeAgent:
	def __init__(self, mcp_client, usage_tracker):
		self.mcp = mcp_client
		self.usage_tracker = usage_tracker
	
	def generate_code(self, structured_reqs: dict) -> str:
		"""
        Calls LLM to generate code based on structured requirements 
		for the chosen software system.

        Args:
            structured_reqs: includes the parsed requirements
        Returns:
            the generated source code as plain text as a str
        """
		# build the prompt
		# get prompt response
		# return the text
		pass

	def save_code_to_file(self, code_text: str, file_path="generated_code/generated_app.py") -> None:
		"""
        Writes the generated code into a file for later execution.
        """
		pass