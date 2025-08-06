import json
from typing import List, Dict
from app.config.azure_config import AzureAIConfig

class ContentOptimizer:
    def __init__(self, azure_config: AzureAIConfig):
        self.azure_config = azure_config
        self.client = azure_config.get_client("content_optimizer")
        self.prompt_template = self._load_prompt("prompts/content_optimizer.txt")
        self.brand_voice = self._load_prompt("prompts/ing_brand_voice.txt")
    
    def _load_prompt(self, filepath: str) -> str:
        """Load prompt from text file"""
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return f"Default prompt for {filepath}"
    
    async def targeted_optimize(self, content_analysis: Dict, competitor_snippets: List[Dict]) -> Dict:
        """Perform targeted content optimization"""
        
        prompt = self.prompt_template.format(
            optimization_type="targeted",
            current_content=json.dumps(content_analysis, indent=2),
            competitor_analysis=json.dumps(competitor_snippets, indent=2),
            brand_guidelines=self.brand_voice,
            optimization_goal="Improve AI Overview inclusion while maintaining ING brand voice"
        )
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",  # Use full model for content generation
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=2500
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def comprehensive_rewrite(self, keywords: List[str], competitor_snippets: List[Dict], analysis: Dict) -> Dict:
        """Comprehensive content rewrite for major optimization"""
        
        prompt = f"""
        Comprehensive content rewrite for ING Bank:
        
        TARGET KEYWORDS: {', '.join(keywords)}
        COMPETITOR ANALYSIS: {json.dumps(competitor_snippets, indent=2)}
        CURRENT CONTENT GAPS: {json.dumps(analysis, indent=2)}
        
        BRAND VOICE: {self.brand_voice}
        
        Create comprehensive, AI Overview-optimized content that:
        1. Addresses all identified sub-intents
        2. Outperforms competitor snippets
        3. Maintains authentic ING brand voice
        4. Provides genuine customer value
        
        Return complete optimized content with metadata.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=3000
        )
        
        return json.loads(response.choices[0].message.content)