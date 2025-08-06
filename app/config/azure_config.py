
# ================================
# config/azure_config.py - Azure AI Foundry Configuration
# ================================

import os
from openai import AsyncAzureOpenAI

class AzureAIConfig:
    """Azure AI Foundry configuration for LLM agents"""
    
    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = "2024-02-01"
        
        # Model assignments for different agents
        self.agent_models = {
            "news_scanner": "gpt-4o-mini",
            "intent_extractor": "gpt-4o-mini",
            "content_evaluator": "gpt-4o-mini", 
            "content_optimizer": "gpt-4o",
            "brand_enforcer": "gpt-4o-mini"
        }
    
    def get_client(self, agent_name: str) -> AsyncAzureOpenAI:
        """Get Azure OpenAI client for specific agent"""
        return AsyncAzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )
    
    def get_model_for_agent(self, agent_name: str) -> str:
        """Get appropriate model for agent"""
        return self.agent_models.get(agent_name, "gpt-4o-mini")