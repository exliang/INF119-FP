# Authors: Emily Liang 79453973, Kaomi Booker 85786904
# Purpose: Generates runnable code modules based on the parsed/structured requirements

import json
import os
import re

class CodeAgent:
	def __init__(self, mcp_server, usage_tracker):
		self.mcp_server = mcp_server
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

		mcp_output = self.mcp_server.call_tool("code_agent", "generate_code", prompt)

		# track agent call
		self.usage_tracker.record_agent_call("code_agent", mcp_output)
		self.usage_tracker.save_report()

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
	
# test methods
# reqs = """CyberDefender is a security software application that detects and defends 
# against cyber threats by proactively monitoring network traffic and system logs. 
# It utilizes artificial intelligence algorithms to identify potential security breaches, 
# malware attacks, and suspicious activities in real-time. CyberDefender provides immediate 
# alerts and takes necessary actions to neutralize threats, ensuring the privacy and security 
# of user data. It also includes a password manager and encryption feature to enhance data protection.
# """
# mcp_client = MCPClient()
# tracker = TrackingAgent()
# input_agent = InputAgent(mcp_client, tracker)
# req_dict = input_agent.parse_requirements(reqs)
# code_agent = CodeAgent(mcp_client, tracker)
# app_code = code_agent.generate_code(req_dict)
# code_agent.save_code_to_file(app_code)