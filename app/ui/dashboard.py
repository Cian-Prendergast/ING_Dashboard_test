# ================================
# ui/dashboard.py - MonsterUI Dashboard Layout
# ================================

def create_ing_dashboard():
    """Main ING dashboard with MonsterUI styling"""
    return Div(
        # ING Brand Header
        NavBar(
            DivLAligned(
                Img(src="/static/ing-logo.png", cls="h-10 mr-4"),
                Div(
                    H1("Content Intelligence", cls=TextT.bold + TextT.xl + "text-white"),
                    P("AI-Powered Content Strategy Platform", cls=TextT.sm + "text-white opacity-90")
                )
            ),
            DivLAligned(
                Alert("🔴 Live", cls=AlertT.success + "badge-sm mr-3"),
                Button("⚡ Generate", cls="btn-ing-primary btn-sm", 
                       hx_get="/api/trigger-content-generation",
                       hx_target="#content-workspace")
            ),
            cls="bg-ing-orange shadow-lg"
        ),
        
        # Main Dashboard Container
        Container(
            # Key Metrics Row
            Div(
                H2("Intelligence Overview", cls=TextT.xl + TextT.bold + "text-gray-900 mb-6 mt-8"),
                Grid(
                    MetricCard("AI Overview Wins", "12", "📈 +3 this week", AlertT.success),
                    MetricCard("Active Optimizations", "8", "⚙️ Processing", AlertT.info),
                    MetricCard("RSS Alerts", "2", "🚨 Breaking news", AlertT.warning), 
                    MetricCard("Content Pipeline", "15", "📝 Ready to publish", AlertT.info),
                    cols_lg=4, gap=6
                ),
                cls="mb-8"
            ),
            
            # Main Workspace - 3-Column Layout  
            Grid(
                # Left: News Intelligence Panel
                Card(
                    CardHeader(
                        DivFullySpaced(
                            H3("News Intelligence", cls=TextT.lg + TextT.bold),
                            DivLAligned(
                                Loading(cls=LoadingT.ring + LoadingT.sm + "htmx-indicator"),
                                Button("🔄", cls="btn-ghost btn-sm",
                                       hx_get="/api/news-intelligence",
                                       hx_target="#news-intel-content")
                            )
                        )
                    ),
                    CardBody(
                        Div(
                            id="news-intel-content",
                            hx_get="/api/news-intelligence",
                            hx_trigger="load, every 90s",
                            hx_swap="innerHTML",
                            cls="space-y-3"
                        )
                    ),
                    cls="ing-card-news h-96 overflow-y-auto"
                ),
                
                # Center: GEO Optimization Panel
                Card(
                    CardHeader(
                        DivFullySpaced(
                            H3("GEO Optimization", cls=TextT.lg + TextT.bold),
                            Button("🎯 Optimize", cls="btn-ing-primary btn-sm",
                                   hx_get="/api/geo-optimization",
                                   hx_target="#geo-content")
                        )
                    ),
                    CardBody(
                        Div(
                            id="geo-content",
                            hx_get="/api/geo-optimization",
                            hx_trigger="load, every 300s",  # 5 min updates
                            hx_swap="innerHTML",
                            cls="space-y-3"
                        )
                    ),
                    cls="ing-card-geo h-96 overflow-y-auto"
                ),
                
                # Right: Content Workspace
                Card(
                    CardHeader(
                        DivFullySpaced(
                            H3("Content Pipeline", cls=TextT.lg + TextT.bold),
                            Button("📝 Create", cls="btn-ing-secondary btn-sm")
                        )
                    ),
                    CardBody(
                        Div(
                            id="content-workspace",
                            hx_get="/api/content-pipeline",
                            hx_trigger="load",
                            hx_swap="innerHTML",
                            cls="space-y-3"
                        )
                    ),
                    cls="ing-card-content h-96 overflow-y-auto"
                ),
                
                cols_lg=3, gap=8, cls="mb-8"
            ),
            
            # Competitive Intelligence Section
            Card(
                CardHeader(
                    H3("Competitive Intelligence", cls=TextT.lg + TextT.bold)
                ),
                CardBody(
                    Div(
                        id="competitive-alerts",
                        hx_get="/api/competitive-alerts",
                        hx_trigger="load, every 600s",  # 10 min updates
                        hx_swap="innerHTML"
                    )
                ),
                cls="ing-card-competitive"
            ),
            
            cls=ContainerT.xl + " py-6"
        ),
        
        # Custom ING styling
        Style("""
        .btn-ing-primary { 
            background: #ff6200; 
            border-color: #ff6200; 
            color: white; 
        }
        .btn-ing-primary:hover { 
            background: #e55a00; 
            border-color: #e55a00; 
        }
        .btn-ing-secondary {
            background: #233142;
            border-color: #233142; 
            color: white;
        }
        .bg-ing-orange { background-color: #ff6200; }
        .text-ing-orange { color: #ff6200; }
        .ing-card-news { border-left: 4px solid #ff6200; }
        .ing-card-geo { border-left: 4px solid #233142; }
        .ing-card-content { border-left: 4px solid #12b981; }
        .ing-card-competitive { border-left: 4px solid #f59e0b; }
        """),
        
        cls="min-h-screen bg-gray-50"
    )