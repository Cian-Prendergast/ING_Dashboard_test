# ================================
# agents/intent_extractor.py - Search Intent Analysis Agent
# ================================

import json
from datetime import datetime
from typing import List, Dict
from app.config.azure_config import AzureAIConfig

class IntentExtractor:
    def __init__(self, azure_config: AzureAIConfig):
        self.azure_config = azure_config
        self.client = azure_config.get_client("intent_extractor")
        self.prompt_template = self._load_prompt("prompts/intent_extractor.txt")
    
    def _load_prompt(self, filepath: str) -> str:
        """Load prompt from text file"""
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return f"Default prompt for {filepath}"
    
    async def extract_from_news(self, relevant_news: List[Dict]) -> List[Dict]:
        """Extract search intents from relevant news articles"""
        
        prompt = self.prompt_template.format(
            news_articles=json.dumps(relevant_news, indent=2),
            current_date=datetime.now().strftime("%Y-%m-%d"),
            market_context="Dutch banking market"
        )
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1200
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("extracted_intents", [])