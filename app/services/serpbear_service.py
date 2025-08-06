# ================================
# services/serpbear_service.py - Enhanced SERP Tracking
# ================================

import os
import aiohttp
from typing import List

class SerpBearService:
    def __init__(self):
        self.base_url = os.getenv("SERPBEAR_BASE_URL")
        self.api_key = os.getenv("SERPBEAR_API_KEY")
    
    async def get_tracked_keywords(self) -> List[str]:
        """Get currently tracked keywords from SerpBear"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                async with session.get(f"{self.base_url}/api/keywords", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [kw["keyword"] for kw in data.get("keywords", [])]
        except Exception as e:
            print(f"SerpBear API error: {e}")
            return ["mortgage rates", "digital banking", "investment options"]  # Fallback
    
    async def get_priority_keywords(self) -> List[str]:
        """Get high-priority keywords for optimization"""
        all_keywords = await self.get_tracked_keywords()
        # Logic to prioritize based on performance, competition, etc.
        return all_keywords[:10]  # Top 10 for optimization