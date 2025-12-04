# Authors: Emily Liang 79453973
# Purpose: maintain structured control over requests and responses 

from client.mcp_client import MCPClient

class MCPServer:
	def __init__(self, api_key=None):
		"""Initializes the mcp server with the mcp client & default tools"""
		self.client = MCPClient(api_key=api_key)
		self.tools = {"input_agent": "", "code_agent": "", "test_agent": ""} #{agent_name: tool}

	def set_tools(self, agent: str, tool: str) -> None:
		"""Set the tools for each agent."""
		self.tools[agent] = tool

	def call_tool(self, agent: str, tool: str, prompt: str) -> dict:
		"""Call the specific tool for a specific agent. """
		if tool not in self.tools[agent]: #if tool doesn't exist in tools dict
			raise ValueError(f"Tool '{tool}' not available for {agent}.")
		return self.client.call_model(prompt) #output 