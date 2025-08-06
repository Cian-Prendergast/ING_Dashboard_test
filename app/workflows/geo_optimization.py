# ================================
# workflows/geo_optimization.py - LangGraph GEO Workflow  
# ================================

from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from app.config.azure_config import AzureAIConfig
from app.agents.content_evaluator import ContentEvaluator
from app.agents.content_optimizer import ContentOptimizer

class GEOState(TypedDict):
    target_keywords: List[str]
    ai_overview_data: Dict
    competitor_snippets: List[Dict]
    ing_content_analysis: Dict
    optimization_strategy: str
    optimized_content: Dict
    inclusion_predictions: Dict
    timestamp: str

class GEOOptimizationWorkflow:
    def __init__(self, azure_config: AzureAIConfig):
        self.azure_config = azure_config
        self.content_evaluator = ContentEvaluator(azure_config)
        self.content_optimizer = ContentOptimizer(azure_config)
        self.workflow = self._create_workflow()
    
    def _create_workflow(self):
        """Create LangGraph workflow for GEO optimization"""
        workflow = StateGraph(GEOState)
        
        # Parallel analysis nodes
        workflow.add_node("scrape_ai_overview", self._scrape_ai_overview)
        workflow.add_node("analyze_competitors", self._analyze_competitor_snippets)
        workflow.add_node("evaluate_ing_content", self._evaluate_ing_content)
        
        # Conditional optimization
        workflow.add_conditional_edges(
            "evaluate_ing_content",
            self._determine_optimization_strategy,
            {
                "already_winning": "monitor_only",
                "minor_optimization": "targeted_optimization", 
                "major_optimization": "comprehensive_rewrite"
            }
        )
        
        # Optimization nodes
        workflow.add_node("monitor_only", self._monitor_only)
        workflow.add_node("targeted_optimization", self._targeted_optimization)
        workflow.add_node("comprehensive_rewrite", self._comprehensive_rewrite)
        
        # All paths lead to prediction
        workflow.add_edge("monitor_only", "predict_inclusion")
        workflow.add_edge("targeted_optimization", "predict_inclusion")
        workflow.add_edge("comprehensive_rewrite", "predict_inclusion")
        
        workflow.add_node("predict_inclusion", self._predict_ai_overview_inclusion)
        workflow.add_edge("predict_inclusion", END)
        
        workflow.set_entry_point("scrape_ai_overview")
        workflow.add_edge("scrape_ai_overview", "analyze_competitors")
        workflow.add_edge("analyze_competitors", "evaluate_ing_content")
        
        return workflow.compile()
    
    async def _scrape_ai_overview(self, state: GEOState) -> GEOState:
        """Scrape current AI Overview results for target keywords"""
        ai_overview_data = {}
        
        for keyword in state["target_keywords"]:
            # Use existing SERP scraping infrastructure
            serp_data = await self._scrape_serp_for_keyword(keyword)
            ai_overview_data[keyword] = serp_data.get("ai_overview", {})
        
        state["ai_overview_data"] = ai_overview_data
        return state
    
    async def _analyze_competitor_snippets(self, state: GEOState) -> GEOState:
        """Extract and analyze competitor snippets from AI Overview"""
        competitor_snippets = []
        
        for keyword, ai_data in state["ai_overview_data"].items():
            snippets = await self._extract_competitor_snippets(ai_data)
            competitor_snippets.extend(snippets)
        
        state["competitor_snippets"] = competitor_snippets
        return state
    
    async def _evaluate_ing_content(self, state: GEOState) -> GEOState:
        """Evaluate ING's current content against AI Overview winners"""
        analysis = await self.content_evaluator.evaluate_content(
            state["target_keywords"],
            state["competitor_snippets"]
        )
        state["ing_content_analysis"] = analysis
        return state
    
    def _determine_optimization_strategy(self, state: GEOState) -> str:
        """Decide optimization approach based on content analysis"""
        analysis = state["ing_content_analysis"]
        avg_score = analysis.get("average_inclusion_score", 0)
        
        if avg_score >= 85:
            return "already_winning"
        elif avg_score >= 60:
            return "minor_optimization"
        else:
            return "major_optimization"
    
    async def _targeted_optimization(self, state: GEOState) -> GEOState:
        """Minor content optimizations"""
        optimized = await self.content_optimizer.targeted_optimize(
            state["ing_content_analysis"],
            state["competitor_snippets"]
        )
        state["optimized_content"] = optimized
        state["optimization_strategy"] = "targeted"
        return state
    
    async def _comprehensive_rewrite(self, state: GEOState) -> GEOState:
        """Major content rewrite for AI Overview inclusion"""
        optimized = await self.content_optimizer.comprehensive_rewrite(
            state["target_keywords"],
            state["competitor_snippets"],
            state["ing_content_analysis"]
        )
        state["optimized_content"] = optimized
        state["optimization_strategy"] = "comprehensive"
        return state
    
    async def _monitor_only(self, state: GEOState) -> GEOState:
        """Content is already performing well - just monitor"""
        state["optimization_strategy"] = "monitor"
        state["optimized_content"] = {"status": "no_changes_needed"}
        return state
    
    async def _predict_ai_overview_inclusion(self, state: GEOState) -> GEOState:
        """Predict AI Overview inclusion using LLM reasoning"""
        predictions = await self.content_evaluator.predict_inclusion_probability(
            state["optimized_content"],
            state["competitor_snippets"],
            state["target_keywords"]
        )
        state["inclusion_predictions"] = predictions
        return state
    
    async def optimize_for_ai_overview(self, input_state: Dict) -> Dict:
        """Main entry point for GEO optimization"""
        return await self.workflow.ainvoke(input_state)