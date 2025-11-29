# Authors: Emily Liang 79453973, Angie Xetey 44067973
# Purpose: Ties all 4 agents together and runs the UI

from agents.input_agent import InputAgent
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.tracking_agent import TrackingAgent
from client.mcp_client import MCPClient
from gui.ui import UI
import sys, subprocess

def run_workflow(reqs: str, input_agent: InputAgent, code_agent: CodeAgent, 
                 test_agent: TestAgent, tracking_agent: TrackingAgent) -> dict:
    """
    Method to execute the full workflow. Agents are tracked in each individual 
    agent file and saved to the usage_report automatically.
    """
	
    # Parse requirements
    parsed_requirements = input_agent.parse_requirements(reqs)

    # Generate code
    generated_code = code_agent.generate_code(parsed_requirements)

    # Generate tests
    generated_tests = test_agent.generate_tests(generated_code)
    
	# Run tests
    cmd = ["python", "-m", "generated_tests.test_generated_app"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    test_output = stdout + "\n" + stderr
    passed = test_output.count(".")
    failed = test_output.count("FAIL") + test_output.count("ERROR")
    total = passed + failed
    summary_md = f"""
	### Test Summary
	- **Total tests:** {total}
	- **Passed:** {passed}
	- **Failed:** {failed}
	- **Status:** {"Pass threshold met (≥8)" if passed >= 8 else "Not enough passing tests"}
	"""

    # Get usage report (only need to save one used from demo)
    usage_report = tracking_agent.get_report()

    # Return everything for UI
    return {
        "parsed_requirements": parsed_requirements,
        "generated_code": generated_code,
        "generated_tests": generated_tests,
        "test_summary": summary_md,
        "test_output": test_output,
        "usage_report": usage_report
    }


def main():
    reqs = """CyberDefender is a security software application that detects and defends 
    against cyber threats by proactively monitoring network traffic and system logs. 
    It utilizes artificial intelligence algorithms to identify potential security breaches, 
    malware attacks, and suspicious activities in real-time. CyberDefender provides immediate 
    alerts and takes necessary actions to neutralize threats, ensuring the privacy and security 
    of user data. It also includes a password manager and encryption feature to enhance data protection.
    """
    
    # Initialize MCP client & tracker
    mcp_client = MCPClient()
    tracker = TrackingAgent()

    # Initialize agents
    input_agent = InputAgent(mcp_client, tracker)
    code_agent = CodeAgent(mcp_client, tracker)
    test_agent = TestAgent(mcp_client, tracker)

	# run workflow
    resuts = run_workflow(reqs, input_agent, code_agent, test_agent, tracker)

    # Launch UI
    ui = UI(resuts)
    ui.launch_ui()


if __name__ == '__main__':
    main()