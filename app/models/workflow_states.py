# ================================
# models/workflow_states.py - LangGraph State Definitions
# ================================

from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class NewsIntelState(TypedDict):
    """State for news intelligence workflow"""
    rss_articles: List[Dict[str, Any]]
    tracked_keywords: List[str]
    relevant_news: List[Dict[str, Any]]
    extracted_intents: List[Dict[str, Any]]
    content_opportunities: List[Dict[str, Any]]
    competitive_gaps: List[Dict[str, Any]]
    priority_level: str
    timestamp: str
    workflow_id: str

class GEOState(TypedDict):
    """State for GEO optimization workflow"""
    target_keywords: List[str]
    ai_overview_data: Dict[str, Any]
    competitor_snippets: List[Dict[str, Any]]
    ing_content_analysis: Dict[str, Any]
    optimization_strategy: str
    optimized_content: Dict[str, Any]
    inclusion_predictions: Dict[str, Any]
    timestamp: str
    workflow_id: str

class ContentGenState(TypedDict):
    """State for content generation workflow"""
    opportunity_id: str
    content_brief: Dict[str, Any]
    generated_content: str
    brand_compliance: Dict[str, Any]
    seo_optimization: Dict[str, Any]
    final_article: Dict[str, Any]
    timestamp: str
    workflow_id: str