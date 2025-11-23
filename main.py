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
	# 4. Parse requirements

    # 5. Generate code

    # 6. Generate tests

    # 7. Optionally run tests automatically

    # 8. Save usage report (only need to save one used from demo)
	pass

def main():
	# 1. Initialize MCP client & tracker

    # 2️. Initialize agents

    # 3️. Launch UI
	mcp = MCPClient()
	output = mcp.call_model("Write a Python function that adds two numbers.")
	print(output)
	tracking = TrackingAgent()
	tracking.record_agent_call("input_agent", output) #input bc the method called is from input_agent
	tracking.save_report()

if __name__ == '__main__':
	main()