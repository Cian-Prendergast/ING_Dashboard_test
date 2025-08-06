# agents/competitive_gap_analyzer.py
"""
Analyzes competitor content gaps for strategic opportunities
"""
import json
from typing import List, Dict

class CompetitiveGapAnalyzer:
    def __init__(self, azure_config):
        self.azure_config = azure_config
        self.client = azure_config.get_client("competitive_analyzer")
    
    async def find_opportunities(self, extracted_intents: List[Dict], tracked_keywords: List[str]) -> List[Dict]:
        """Identify competitive content gaps"""
        
        prompt = f"""
        Analyze competitive gaps for ING Bank content strategy:
        
        EXTRACTED INTENTS: {json.dumps(extracted_intents, indent=2)}
        TRACKED KEYWORDS: {', '.join(tracked_keywords)}
        
        Identify opportunities where:
        1. High search volume but weak competitor content
        2. Trending topics with first-mover advantage
        3. Complex financial topics needing expert explanation
        4. ING has unique product/service advantages
        
        Return JSON array of opportunities with gap analysis.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1500
        )
        
        return json.loads(response.choices[0].message.content)