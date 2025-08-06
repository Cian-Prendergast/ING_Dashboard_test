# ================================
# workflows/news_intelligence.py - LangGraph News Workflow
# ================================

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from datetime import datetime
from app.config.azure_config import AzureAIConfig
from app.agents.news_scanner import NewsScanner
from app.agents.intent_extractor import IntentExtractor
from app.agents.competitive_gap_analyzer import CompetitiveGapAnalyzer

class NewsIntelState(TypedDict):
    rss_articles: List[Dict]
    tracked_keywords: List[str] 
    relevant_news: List[Dict]
    extracted_intents: List[Dict]
    content_opportunities: List[Dict]
    competitive_gaps: List[Dict]
    priority_level: str
    timestamp: str

class NewsIntelligenceWorkflow:
    def __init__(self, azure_config: AzureAIConfig):
        self.azure_config = azure_config
        self.news_scanner = NewsScanner(azure_config)
        self.intent_extractor = IntentExtractor(azure_config)
        self.gap_analyzer = CompetitiveGapAnalyzer(azure_config)
        self.workflow = self._create_workflow()
    
    def _create_workflow(self):
        """Create LangGraph workflow for news intelligence"""
        workflow = StateGraph(NewsIntelState)
        
        # Add nodes
        workflow.add_node("scan_news", self._scan_news_relevance)
        workflow.add_node("extract_intents", self._extract_search_intents)
        workflow.add_node("analyze_gaps", self._analyze_competitive_gaps)
        workflow.add_node("prioritize_opportunities", self._prioritize_opportunities)
        
        # Define flow
        workflow.set_entry_point("scan_news")
        workflow.add_edge("scan_news", "extract_intents")
        workflow.add_edge("extract_intents", "analyze_gaps")
        workflow.add_edge("analyze_gaps", "prioritize_opportunities")
        workflow.add_edge("prioritize_opportunities", END)
        
        return workflow.compile()
    
    async def _scan_news_relevance(self, state: NewsIntelState) -> NewsIntelState:
        """Scan RSS articles for ING relevance"""
        relevant_news = await self.news_scanner.analyze_relevance(
            state["rss_articles"], 
            state["tracked_keywords"]
        )
        state["relevant_news"] = relevant_news
        return state
    
    async def _extract_search_intents(self, state: NewsIntelState) -> NewsIntelState:
        """Extract search intents from relevant news"""
        intents = await self.intent_extractor.extract_from_news(
            state["relevant_news"]
        )
        state["extracted_intents"] = intents
        return state
    
    async def _analyze_competitive_gaps(self, state: NewsIntelState) -> NewsIntelState:
        """Identify competitive content gaps"""
        gaps = await self.gap_analyzer.find_opportunities(
            state["extracted_intents"],
            state["tracked_keywords"]
        )
        state["competitive_gaps"] = gaps
        return state
    
    async def _prioritize_opportunities(self, state: NewsIntelState) -> NewsIntelState:
        """Prioritize content opportunities by urgency and impact"""
        opportunities = []
        
        for gap in state["competitive_gaps"]:
            opportunity = {
                "headline": gap["potential_headline"],
                "priority": gap["urgency_score"],
                "keywords": gap["target_keywords"],
                "content_angle": gap["recommended_angle"],
                "ai_overview_gap": gap["competitor_weakness"],
                "estimated_traffic": gap["traffic_potential"]
            }
            opportunities.append(opportunity)
        
        # Sort by priority score
        opportunities.sort(key=lambda x: x["priority"], reverse=True)
        
        state["content_opportunities"] = opportunities[:5]  # Top 5
        state["priority_level"] = "urgent" if opportunities[0]["priority"] > 80 else "normal"
        
        return state

    async def analyze_news_opportunities(self, state: Dict) -> Dict:
        """Main workflow execution"""
        workflow_result = await self.workflow.ainvoke(state)
        
        # Post-process results for dashboard
        return {
            "content_opportunities": workflow_result["content_opportunities"],
            "urgent_count": len([op for op in workflow_result["content_opportunities"] if op["urgency_level"] == "urgent"]),
            "total_analyzed": len(state["rss_articles"]),
            "analysis_timestamp": datetime.now().isoformat()
        }