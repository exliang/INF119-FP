# Authors: Emily Liang 79453973, Kaomi Booker 85786904
# Purpose: Generates runnable code modules based on the parsed/structured requirements

import json
import os
import re

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
		requirements = structured_reqs.get("requirements")
		if not requirements:
			raise ValueError("Structured requirements must include a non-empty 'requirements' field.")

		reqs_text = json.dumps(requirements, indent=2)
		prompt = (
			"You are the Cyber Defender CodeAgent. "
			"Generate a single runnable Python module that satisfies ALL of the numbered requirements "
			"shown below. Follow best practices (modularity, docstrings, error handling) and rely only on "
			"Python's standard library unless the requirements explicitly mention external packages. "
			"Return code only—no explanations, markdown fences, or commentary.\n\n"
			f"Structured requirements JSON:\n{reqs_text}\n\n"
			"Expect the module to be saved directly to disk and imported by a test runner."
		)

		mcp_output = self.mcp.call_model(prompt)
		self.usage_tracker.record_model_call(mcp_output)

		code_text = self._extract_code_from_response(mcp_output.get("response", ""))
		if not code_text:
			raise ValueError("LLM returned empty code text.")

		return code_text

	def save_code_to_file(self, code_text: str, file_path="generated_code/generated_app.py") -> None:
		"""
        Writes the generated code into a file for later execution.
        """
		if not code_text.strip():
			raise ValueError("Cannot save empty code text.")

		directory = os.path.dirname(file_path)
		if directory:
			os.makedirs(directory, exist_ok=True)

		with open(file_path, "w", encoding="utf-8") as file:
			file.write(code_text)

	def _extract_code_from_response(self, response_text: str) -> str:
		"""
		Normalizes the LLM response by removing markdown fences or surrounding whitespace.
		"""
		if not isinstance(response_text, str):
			return ""

		response_text = response_text.strip()

		code_fence_pattern = r"```(?:python)?\s*([\s\S]*?)```"
		match = re.search(code_fence_pattern, response_text, re.IGNORECASE)
		if match:
			return match.group(1).strip()

		return response_text