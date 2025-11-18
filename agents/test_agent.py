# Authors: Emily Liang 79453973, 
# Purpose: Produces at least 10 test cases, aiming for ≥80% pass rate

class TestAgent:
	def __init__(self, mcp_client, usage_tracker):
		self.mcp = mcp_client
		self.usage_tracker = usage_tracker
	
	def generate_tests(self, code_text: str) -> str:
		"""
		Calls LLM to generate at least 10 test cases for the generated code.

		Args:
			code_text: the generated app code from CodeAgent
		Returns:
			the whole test file content as a str
		"""
		# build the prompt
		# get prompt response
		# return the text
		pass

	def save_tests_to_file(self, test_text: str, file_path="generated_tests/test_generated_app.py") -> None:
		"""
        Writes the generated tests into a file for later execution.
        """
		pass