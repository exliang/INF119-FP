# Authors: Emily Liang 79453973, 
# Purpose: centralize LLM integration between agents

class MCPClient:
	def __init__(self, api_key=None):
		self.api_key = api_key
	
	def call_model(self, prompt: str, model="replacewithactualmodelname") -> dict:
		"""
        Sends a prompt to LLM & returns structured data for usage tracking.
        
        Args:
            prompt: the text prompt to send to the LLM
            model: the model name to use
        
        Returns: (dict)
            {
                "model": model,
                "tokens": estimated_token_count,
                "response": generated_text
            }
		"""
		pass