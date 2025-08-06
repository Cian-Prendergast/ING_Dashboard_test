from fasthtml.common import *
from monsterui.all import *
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import aiohttp
import feedparser
from dataclasses import dataclass

# Import our modules
from app.workflows.news_intelligence import NewsIntelligenceWorkflow
from app.workflows.geo_optimization import GEOOptimizationWorkflow  
from app.workflows.content_generation import ContentGenerationWorkflow
from app.services.rss_service import RSSService
from app.services.serpbear_service import SerpBearService
from app.services.content_service import ContentService
from app.ui.dashboard import create_ing_dashboard
from app.ui.components import *
from app.config.azure_config import AzureAIConfig

# FastHTML app with MonsterUI theme
app, rt = fast_app(
    hdrs=Theme.orange.headers(daisy=True, highlightjs=True),
    static_dir="static"
)

# Global services
rss_service = RSSService()
serpbear_service = SerpBearService()
content_service = ContentService()
azure_config = AzureAIConfig()

# Workflow instances
news_workflow = NewsIntelligenceWorkflow(azure_config)
geo_workflow = GEOOptimizationWorkflow(azure_config)  
content_workflow = ContentGenerationWorkflow(azure_config)

# ================================
# Main Dashboard Route
# ================================

@rt("/")
async def dashboard():
    """ING Content Intelligence Dashboard"""
    return Title("ING Content Intelligence"), create_ing_dashboard()

# ================================
# API Routes - Real-time Intelligence
# ================================

@rt("/api/news-intelligence")
async def news_intelligence():
    """Real-time news analysis using LangGraph workflow"""
    try:
        # Get fresh RSS data
        rss_articles = await rss_service.fetch_all_feeds()
        tracked_keywords = await serpbear_service.get_tracked_keywords()
        
        # Run news intelligence workflow
        result = await news_workflow.analyze_news_opportunities({
            "rss_articles": rss_articles,
            "tracked_keywords": tracked_keywords,
            "timestamp": datetime.now().isoformat()
        })
        
        # Render news intelligence cards
        return render_news_intel_cards(result)
        
    except Exception as e:
        return Alert(f"News analysis error: {str(e)}", cls=AlertT.error)

@rt("/api/geo-optimization") 
async def geo_optimization():
    """AI Overview optimization pipeline"""
    try:
        # Get optimization targets
        priority_keywords = await serpbear_service.get_priority_keywords()
        
        # Run GEO optimization workflow
        result = await geo_workflow.optimize_for_ai_overview({
            "target_keywords": priority_keywords,
            "timestamp": datetime.now().isoformat()
        })
        
        return render_geo_optimization_cards(result)
        
    except Exception as e:
        return Alert(f"GEO optimization error: {str(e)}", cls=AlertT.error)

@rt("/api/generate-content")
async def generate_content(opportunity_id: str):
    """Generate optimized content from opportunity"""
    try:
        # Run content generation workflow
        result = await content_workflow.generate_optimized_article({
            "opportunity_id": opportunity_id,
            "timestamp": datetime.now().isoformat()
        })
        
        return render_generated_content(result)
        
    except Exception as e:
        return Alert(f"Content generation error: {str(e)}", cls=AlertT.error)

@rt("/api/competitive-alerts")
async def competitive_alerts():
    """Real-time competitor AI Overview monitoring"""
    try:
        alerts = await geo_workflow.monitor_competitor_changes()
        return render_competitive_alerts(alerts)
    except Exception as e:
        return Alert(f"Monitoring error: {str(e)}", cls=AlertT.error)
    
# ================================
# Enhanced API Routes and Workflow Triggers
# ================================

@rt("/api/content-pipeline")
async def content_pipeline():
    """Content pipeline status and active projects"""
    try:
        pipeline_status = await content_service.get_pipeline_status()
        
        cards = []
        for item in pipeline_status:
            cards.append(
                Card(
                    CardHeader(
                        DivFullySpaced(
                            Strong(item["title"], cls=TextT.sm),
                            Alert(item["status"], cls="badge-info badge-sm")
                        )
                    ),
                    CardBody(
                        P(item["description"], cls=TextT.xs + TextT.muted),
                        Progress(value=item["progress"], max=100, cls="progress progress-info mt-2")
                    ),
                    cls="mb-2"
                )
            )
        
        return Div(*cards) if cards else P("No active content projects", cls=TextT.muted + "text-center py-4")
        
    except Exception as e:
        return Alert(f"Pipeline error: {str(e)}", cls=AlertT.error)

@rt("/api/trigger-geo-optimization", methods=["POST"])
async def trigger_geo_optimization(keyword: str):
    """Trigger immediate GEO optimization for specific keyword"""
    try:
        # Run GEO workflow for specific keyword
        result = await geo_workflow.optimize_single_keyword({
            "keyword": keyword,
            "priority": "urgent",
            "timestamp": datetime.now().isoformat()
        })
        
        return Alert(f"🚀 GEO optimization started for '{keyword}'", cls=AlertT.success)
        
    except Exception as e:
        return Alert(f"Optimization failed: {str(e)}", cls=AlertT.error)

@rt("/api/generate-from-news", methods=["POST"]) 
async def generate_from_news(headline: str):
    """Generate content from news opportunity"""
    try:
        # Trigger content generation workflow
        result = await content_workflow.generate_from_news_trigger({
            "news_headline": headline,
            "generation_type": "news_response",
            "timestamp": datetime.now().isoformat()
        })
        
        return render_content_generation_status(result)
        
    except Exception as e:
        return Alert(f"Generation failed: {str(e)}", cls=AlertT.error)

@rt("/api/dashboard-metrics")
async def dashboard_metrics():
    """Real-time dashboard metrics"""
    try:
        metrics = {
            "ai_overview_wins": await geo_workflow.count_ai_overview_wins(),
            "active_optimizations": await geo_workflow.count_active_optimizations(),
            "rss_alerts": await news_workflow.count_urgent_opportunities(),
            "content_pipeline": await content_workflow.count_pipeline_items()
        }
        
        return json.dumps(metrics)
        
    except Exception as e:
        return json.dumps({"error": str(e)})

# ================================
# Server Startup and Configuration
# ================================

if __name__ == "__main__":
    print("🏦 Starting ING Content Intelligence Dashboard...")
    print("🔧 Initializing LangGraph workflows...")
    print("🎨 Loading MonsterUI theme...")
    print("🚀 Dashboard ready at http://localhost:8000")
    
    serve(
        app,
        host="0.0.0.0", 
        port=8000,
        reload=True
    )