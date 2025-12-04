# Authors: Emily Liang 79453973, Angie Xetey 44067973, Kaomi Booker 85786904, Kristen Chung 42617410
# Purpose: Ties all 4 agents together and runs the UI

from agents.input_agent import InputAgent
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.tracking_agent import TrackingAgent
from server.mcp_server import MCPServer
from gui.ui import UI
import sys, subprocess, re

def run_workflow(reqs: str, input_agent: InputAgent, code_agent: CodeAgent, 
                 test_agent: TestAgent, tracking_agent: TrackingAgent) -> dict:
    """
    Method to execute the full workflow. Agents are tracked in each individual 
    agent file and saved to the usage_report automatically.
    """
	
    # Parse requirements
    parsed_requirements = input_agent.parse_requirements(reqs)

    # Generate code & save to file
    generated_code = code_agent.generate_code(parsed_requirements)
    code_agent.save_code_to_file(generated_code)

    # Generate tests & save to file 
    generated_tests = test_agent.generate_tests(generated_code)
    test_agent.save_tests_to_file(generated_tests)
    
	# Run tests
    cmd = [sys.executable, "-m", "generated_tests.test_generated_app"]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate()
    test_output = stdout + "\n" + stderr

    # Extract total tests in test suite
    match = re.search(r"Ran (\d+) tests?", test_output)
    total = int(match.group(1)) if match else 0

    # Extracts failures and errors from test suite
    failed = 0
    errors = 0

    fail_summary = re.search(r"FAILED \((.*?)\)", test_output)
    if fail_summary:
        text = fail_summary.group(1)

        fail_match = re.search(r"failures=(\d+)", text)
        if fail_match:
            failed = int(fail_match.group(1))

        error_match = re.search(r"errors=(\d+)", text)
        if error_match:
            errors = int(error_match.group(1))

    # Computes the total amount of tests passed
    passed = total - failed - errors

    summary_md = f"""
	### Test Summary
	- **Total tests:** {total}
	- **Passed:** {passed}
	- **Failed:** {failed}
	- **Errors:** {errors}
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
    """Entry point for cyberdefender system"""
    reqs = """"""  # empty initial reqs so user can input it
    
    # Initialize MCP server & set tools
    mcp_server = MCPServer()
    mcp_server.set_tools("input_agent", "parse_requirements")
    mcp_server.set_tools("code_agent", "generate_code")
    mcp_server.set_tools("test_agent", "generate_tests")

    # Initialize tracker & agents 
    tracker = TrackingAgent()
    input_agent = InputAgent(mcp_server, tracker)
    code_agent = CodeAgent(mcp_server, tracker)
    test_agent = TestAgent(mcp_server, tracker)

	# Launch UI (workflow runs on-demand from the Gradio callback)
    ui = UI(run_workflow, input_agent, code_agent, test_agent, tracker, reqs)
    ui.launch_ui()


if __name__ == '__main__':
    main()