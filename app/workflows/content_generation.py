# ================================
# workflows/content_generation.py - Content Creation Workflow
# ================================

from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
from app.config.azure_config import AzureAIConfig
from app.agents.content_optimizer import ContentOptimizer
from app.agents.brand_enforcer import BrandEnforcer

class ContentGenState(TypedDict):
    opportunity_id: str
    content_brief: Dict
    generated_content: str
    brand_compliance: Dict
    seo_optimization: Dict
    final_article: Dict
    timestamp: str

class ContentGenerationWorkflow:
    def __init__(self, azure_config: AzureAIConfig):
        self.azure_config = azure_config
        self.content_optimizer = ContentOptimizer(azure_config)
        self.brand_enforcer = BrandEnforcer(azure_config)
        self.workflow = self._create_workflow()
    
    def _create_workflow(self):
        workflow = StateGraph(ContentGenState)
        
        workflow.add_node("create_brief", self._create_content_brief)
        workflow.add_node("generate_content", self._generate_initial_content)
        workflow.add_node("enforce_brand", self._enforce_brand_voice)
        workflow.add_node("optimize_seo", self._optimize_for_seo)
        workflow.add_node("final_review", self._final_quality_review)
        
        workflow.set_entry_point("create_brief")
        workflow.add_edge("create_brief", "generate_content")
        workflow.add_edge("generate_content", "enforce_brand")
        workflow.add_edge("enforce_brand", "optimize_seo") 
        workflow.add_edge("optimize_seo", "final_review")
        workflow.add_edge("final_review", END)
        
        return workflow.compile()
    
    async def generate_optimized_article(self, input_state: Dict) -> Dict:
        """Generate complete optimized article"""
        return await self.workflow.ainvoke(input_state)