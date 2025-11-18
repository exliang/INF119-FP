# Authors: Emily Liang 79453973, 
# Purpose: Creates a user interface for users to submit requirements for the app & receive the generated code and tests

class UI:
	def __init__(self, input_agent, code_agent, test_agent, tracking_agent):
		"""
		Store references to all agents.
		"""
		self.input_agent = input_agent
		self.code_agent = code_agent
		self.test_agent = test_agent
		self.tracking_agent = tracking_agent
	
	def launch_ui(self) -> None:
		"""
		Method to launch the UI for user interaction.
		"""
		#Tkinter or Gradio
		pass
