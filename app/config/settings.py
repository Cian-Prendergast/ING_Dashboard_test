# ================================
# config/settings.py - Application Settings
# ================================

import os
from pydantic_settings import BaseSettings

class DashboardSettings(BaseSettings):
    """Application configuration settings"""
    
    # Azure AI Configuration
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_api_version: str = "2024-02-01"
    
    # SerpBear Configuration
    serpbear_base_url: str = ""
    serpbear_api_key: str = ""
    
    # RSS Configuration
    rss_fetch_interval: int = 90  # seconds
    rss_max_articles_per_source: int = 5
    
    # LangGraph Configuration
    max_workflow_timeout: int = 300  # seconds
    enable_workflow_logging: bool = True
    
    # Dashboard Configuration
    dashboard_refresh_interval: int = 60  # seconds
    enable_real_time_alerts: bool = True
    
    # Database Configuration (if using persistent storage)
    database_url: str = "sqlite:///./ing_dashboard.db"
    
    class Config:
        env_file = ".env"