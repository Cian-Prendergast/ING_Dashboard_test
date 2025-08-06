# ================================
# ui/components.py - Reusable MonsterUI Components
# ================================

from fasthtml.common import *
from monsterui.all import *
import json
from typing import List, Dict

def MetricCard(title: str, value: str, change: str, alert_type):
    """ING-themed metric card"""
    return Card(
        CardBody(
            DivFullySpaced(
                Div(
                    H4(value, cls=TextT.xl + TextT.bold + "text-gray-900"),
                    P(title, cls=TextT.sm + TextT.muted)
                ),
                Alert(change, cls=alert_type + "badge-sm")
            )
        ),
        cls="ing-metric-card hover:shadow-md transition-all"
    )

def NewsIntelCard(headline: str, summary: str, relevance_score: int, urgency: str):
    """News intelligence card component"""
    urgency_styles = {
        "urgent": AlertT.error,
        "high": AlertT.warning, 
        "medium": AlertT.info,
        "low": AlertT.success
    }
    
    return Card(
        CardHeader(
            DivFullySpaced(
                H4(headline, cls=TextT.sm + TextT.bold + "text-gray-900"),
                Alert(f"{relevance_score}%", cls=urgency_styles.get(urgency, AlertT.info) + "badge-sm")
            )
        ),
        CardBody(
            P(summary, cls=TextT.xs + TextT.muted + "line-clamp-3 mb-3"),
            DivFullySpaced(
                Button("🔍 Analyze", cls="btn-ghost btn-xs"),
                Button("🚀 Generate", cls="btn-ing-primary btn-xs",
                       hx_post="/api/generate-from-news",
                       hx_vals=json.dumps({"headline": headline}))
            )
        ),
        cls="ing-news-item hover:bg-orange-50 transition-colors mb-2"
    )

def GEOOptimizationCard(keyword: str, current_position: int, ai_overview_probability: int, status: str):
    """GEO optimization status card"""
    prob_color = "success" if ai_overview_probability > 70 else "warning" if ai_overview_probability > 40 else "error"
    
    return Card(
        CardHeader(
            DivFullySpaced(
                Strong(keyword, cls=TextT.sm),
                Alert(f"#{current_position}", cls="badge-neutral badge-sm")
            )
        ),
        CardBody(
            DivFullySpaced(
                Div(
                    P("AI Overview Probability", cls=TextT.xs + TextT.muted),
                    Progress(value=ai_overview_probability, max=100, cls=f"progress progress-{prob_color}")
                ),
                Alert(f"{ai_overview_probability}%", cls=f"badge-{prob_color}")
            ),
            P(f"Status: {status}", cls=TextT.xs + TextT.muted + "mt-2")
        ),
        CardFooter(
            Button("🎯 Optimize", cls="btn-ing-primary btn-sm w-full",
                   hx_post="/api/trigger-geo-optimization", 
                   hx_vals=json.dumps({"keyword": keyword}))
        ),
        cls="ing-geo-card mb-3"
    )

def render_news_intel_cards(result: Dict) -> Div:
    """Render news intelligence analysis results"""
    opportunities = result.get("content_opportunities", [])
    
    if not opportunities:
        return DivCentered(
            Div("📰", cls="text-4xl opacity-30 mb-3"),
            P("No urgent opportunities detected", cls=TextT.muted),
            cls="py-8"
        )
    
    cards = []
    for opp in opportunities:
        cards.append(NewsIntelCard(
            headline=opp["headline"],
            summary=opp.get("content_angle", ""),
            relevance_score=opp.get("priority", 50),
            urgency=opp.get("urgency_level", "medium")
        ))
    
    return Div(*cards, cls="space-y-2")

def render_geo_optimization_cards(result: Dict) -> Div:
    """Render GEO optimization status"""
    optimizations = result.get("optimization_results", [])
    
    cards = []
    for opt in optimizations:
        cards.append(GEOOptimizationCard(
            keyword=opt["keyword"],
            current_position=opt.get("current_position", 50),
            ai_overview_probability=opt.get("inclusion_probability", 0),
            status=opt.get("optimization_status", "analyzing")
        ))
    
    return Div(*cards, cls="space-y-2")

def render_competitive_alerts(alerts: List[Dict]) -> Div:
    """Render competitive intelligence alerts"""
    if not alerts:
        return P("No competitive changes detected", cls=TextT.muted + "text-center py-4")
    
    alert_items = []
    for alert in alerts:
        alert_items.append(
            Alert(
                DivFullySpaced(
                    Div(
                        Strong(alert["competitor"], cls=TextT.sm),
                        P(alert["change_description"], cls=TextT.xs + TextT.muted)
                    ),
                    Button("📊 Analyze", cls="btn-xs")
                ),
                cls=AlertT.warning + "mb-2"
            )
        )
    
    return Div(*alert_items)