# ================================
# agents/news_scanner.py - News Relevance Analysis Agent
# ================================

import json
from datetime import datetime
from typing import List, Dict
from ..config.azure_config import AzureAIConfig

class NewsScanner:
    def __init__(self, azure_config: AzureAIConfig):
        self.azure_config = azure_config
        self.client = azure_config.get_client("news_scanner")
        self.prompt_template = self._load_prompt("prompts/news_scanner.txt")
        self.brand_voice = self._load_prompt("prompts/ing_brand_voice.txt")
    
    def _load_prompt(self, filepath: str) -> str:
        """Load prompt from text file"""
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return self._get_fallback_prompt(filepath)
    
    async def analyze_relevance(self, rss_articles: List[Dict], tracked_keywords: List[str]) -> List[Dict]:
        """Analyze RSS articles for ING content relevance"""
        
        prompt = self.prompt_template.format(
            rss_articles=json.dumps(rss_articles, indent=2),
            tracked_keywords=", ".join(tracked_keywords),
            ing_brand_voice=self.brand_voice,
            analysis_timestamp=datetime.now().isoformat()
        )
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500
        )
        
        # Parse JSON response
        result = json.loads(response.choices[0].message.content)
        return result.get("relevant_articles", [])