# Authors: Emily Liang 79453973, Kristen Chung 42617410
# Purpose: Produces at least 10 test cases, aiming for ≥ 80% pass rate

import os
import re

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
		
		# validate input
		if not code_text or not code_text.strip():
			raise ValueError("Code text must be non-empty to generate tests.")
		
		prompt = (
			"You are the CyberDefender TestAgent. Generate a COMPLETE Python unittest file "
			"that tests the provided module.\n\n"
			"REQUIREMENTS:\n"
			"- Output ONLY valid Python code (NO markdown, NO backticks).\n"
			"- Import the module under test using: import generated_app\n"
			"- Use Python's unittest framework.\n"
			"- Include AT LEAST 10 distinct test methods.\n"
			"- Tests must be deterministic (no external I/O, no randomness unless seeded).\n"
			"- Focus tests on likely behaviors from the code: threat detection, alerting, "
			"password manager operations, and encryption/decryption.\n"
			"- File must be self-contained and runnable.\n"
			"- Add a top comment: '# Run with: python testing.py'\n\n"
			"Module under test:\n"
			f"{code_text}\n"
		)

		# get prompt response & track agent usage
		mcp_output = self.mcp.call_model(prompt)
		self.usage_tracker.record_agent_call("test_agent", mcp_output)
		self.usage_tracker.save_report()

		raw_response = mcp_output.get("response", "")
		test_text = self._extract_code_from_response(raw_response)

		if not test_text or not test_text.strip():
			raise ValueError("LLM returned empty test text.")

		# return the text
		return test_text

	def save_tests_to_file(self, test_text: str, file_path="generated_tests/test_generated_app.py") -> None:
		"""
        Writes the generated tests into a file for later execution.
        """

		if not test_text or not test_text.strip():
			raise ValueError("Cannot save empty test text.")

		directory = os.path.dirname(file_path)
		if directory:
			os.makedirs(directory, exist_ok=True)

		with open(file_path, "w", encoding="utf-8") as file:
			file.write(test_text)
	
	def _extract_code_from_response(self, response_text: str) -> str:
		"""
		Standardizes the LLM's response by removing markdown fences or surrounding whitespace.
		Mirrors the behavior in CodeAgent._extract_code_from_response.
		"""

		if not isinstance(response_text, str):
			return ""

		response_text = response_text.strip()

		# strip ```python ... ``` or ``` ... ``` fences if the model accidentally adds them
		code_fence_pattern = r"```(?:python)?\s*([\s\S]*?)```"
		match = re.search(code_fence_pattern, response_text, re.IGNORECASE)
		if match:
			return match.group(1).strip()

		return response_text
	
# test methods
# (include test code from code_agent)
# test_agent = TestAgent(mcp_client)
# tests = test_agent.generate_tests(app_code)
# test_agent.save_tests_to_file(tests)
# RUN TEST CASES: python -m generated_tests.test_generated_app