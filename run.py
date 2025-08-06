# ================================
# run.py - Application Launcher with Health Checks
# ================================

#!/usr/bin/env python3
"""
ING Content Intelligence Dashboard Launcher
Includes health checks and service validation
"""

import sys
import os
import asyncio
import aiohttp
from app.config.settings import DashboardSettings

def check_environment():
    """Validate environment configuration"""
    settings = DashboardSettings()
    
    required_vars = [
        "azure_openai_endpoint",
        "azure_openai_api_key"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(settings, var):
            missing_vars.append(var.upper())
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("💡 Please check your .env file")
        return False
    
    print("✅ Environment configuration valid")
    return True

async def test_azure_connection():
    """Test Azure AI Foundry connection"""
    try:
        from app.config.azure_config import AzureAIConfig
        azure_config = AzureAIConfig()
        client = azure_config.get_client("test")
        
        # Simple test call
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("✅ Azure AI Foundry connection successful!")
        return True
        
    except Exception as e:
        print(f"⚠️ Azure AI connection issue: {e}")
        return False

async def test_serpbear_connection():
    """Test SerpBear API connection"""
    settings = DashboardSettings()
    
    if not settings.serpbear_base_url:
        print("⚠️ SerpBear not configured (optional)")
        return True
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {settings.serpbear_api_key}"}
            async with session.get(f"{settings.serpbear_base_url}/api/domains", 
                                 headers=headers, timeout=5) as resp:
                if resp.status in [200, 401]:  # 401 = API running but auth issue
                    print("✅ SerpBear connection successful!")
                    return True
                else:
                    print(f"⚠️ SerpBear returned status {resp.status}")
                    return False
    except Exception as e:
        print(f"⚠️ SerpBear connection failed: {e}")
        return False

def main():
    """Main application launcher"""
    print("🏦 ING Content Intelligence Dashboard")
    print("=" * 60)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Validate environment
    if not check_environment():
        sys.exit(1)
    
    # Test service connections
    print("\n🧪 Testing service connections...")
    
    try:
        # Test Azure AI
        azure_ok = asyncio.run(test_azure_connection())
        
        # Test SerpBear
        serpbear_ok = asyncio.run(test_serpbear_connection())
        
        if not azure_ok:
            print("❌ Azure AI Foundry required but not available")
            sys.exit(1)
            
    except Exception as e:
        print(f"⚠️ Connection test failed: {e}")
        print("💡 Dashboard will start but some features may be limited")
    
    print("\n🚀 Starting ING Content Intelligence Dashboard...")
    print("🔧 Initializing LangGraph workflows...")
    print("🎨 Loading MonsterUI theme...")
    print("📱 Dashboard URL: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()