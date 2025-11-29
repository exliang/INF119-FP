# Authors: Emily Liang 79453973, Angie Xetey 44067973
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
    # Parse requirements & track input agent
    parsed_requirements = input_agent.process(reqs)
    tracking_agent.log("InputAgent", tokens_used=120)

    # Generate code & track code agent

    generated_code = code_agent.generate_code(parsed_requirements)
    tracking_agent.log("CodeAgent", tokens_used=350)

    # Generate tests & track test agent

    generated_tests = code_agent.generate_tests(generated_code)
    tracking_agent.log("TestAgent_Generation", tokens_used=200)

    # Optionally run tests automatically

    test_results = test_agent.run_tests(
        code_str=generated_code,
        test_str=generated_tests
    )
    tracking_agent.log("TestAgent_Execution", tokens_used=180)

    # Save usage report (only need to save one used from demo)

    usage_report = tracking_agent.generate_report()

    # Return everything for UI
    return {
        "parsed_requirements": parsed_requirements,
        "generated_code": generated_code,
        "generated_tests": generated_tests,
        "test_results": test_results,
        "usage_report": usage_report
    }

    pass

def main():
    # Initialize MCP client & tracker
    mcp_client = MCPClient()
    tracker = TrackingAgent()

    # Initialize agents
    reqs = """CyberDefender is a security software application that detects and defends 
    against cyber threats by proactively monitoring network traffic and system logs. 
    It utilizes artificial intelligence algorithms to identify potential security breaches, 
    malware attacks, and suspicious activities in real-time. CyberDefender provides immediate 
    alerts and takes necessary actions to neutralize threats, ensuring the privacy and security 
    of user data. It also includes a password manager and encryption feature to enhance data protection.
    """

    input_agent = InputAgent(mcp_client, tracker)
    req_dict = input_agent.parse_requirements(reqs)

    code_agent = CodeAgent(mcp_client, tracker)
    app_code = code_agent.generate_code(req_dict)
    code_agent.save_code_to_file(app_code)

    test_agent = TestAgent(mcp_client, tracker)
    tests = test_agent.generate_tests(app_code)
    test_agent.save_tests_to_file(tests)

    # Launch UI

    ui = UI(input_agent, code_agent,test_agent, tracker)
    ui.launch_ui()
    # RUN TEST CASES: python -m generated_tests.test_generated_app


if __name__ == '__main__':
    main()