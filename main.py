# Authors: Emily Liang 79453973, 
# Purpose: Ties all 4 agents together and runs the UI

from agents.input_agent import InputAgent
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.tracking_agent import TrackingAgent
from client.mcp_client import MCPClient
from gui.ui import UI

def run_workflow(reqs: dict, input_agent: InputAgent, code_agent: CodeAgent, 
				 test_agent: TestAgent, tracking_agent: TrackingAgent) -> None:
	"""
	Method to execute the full workflow.
	"""
	# 4. Parse requirements & track input agent

    # 5. Generate code & track code agent

    # 6. Generate tests & track test agent

    # 7. Optionally run tests automatically

    # 8. Save usage report (only need to save one used from demo)
	pass

def main():
	# 1. Initialize MCP client & tracker

    # 2️. Initialize agents

    # 3️. Launch UI
	reqs = """CyberDefender is a security software application that detects and defends 
	against cyber threats by proactively monitoring network traffic and system logs. 
	It utilizes artificial intelligence algorithms to identify potential security breaches, 
	malware attacks, and suspicious activities in real-time. CyberDefender provides immediate 
	alerts and takes necessary actions to neutralize threats, ensuring the privacy and security 
	of user data. It also includes a password manager and encryption feature to enhance data protection.
	"""
	mcp_client = MCPClient()
	tracker = TrackingAgent()
	input_agent = InputAgent(mcp_client, tracker)
	req_dict = input_agent.parse_requirements(reqs)
	code_agent = CodeAgent(mcp_client, tracker)
	app_code = code_agent.generate_code(req_dict)
	code_agent.save_code_to_file(app_code)
	test_agent = TestAgent(mcp_client, tracker)
	tests = test_agent.generate_tests(app_code)
	test_agent.save_tests_to_file(tests)
	# RUN TEST CASES: python -m generated_tests.test_generated_app


if __name__ == '__main__':
	main()