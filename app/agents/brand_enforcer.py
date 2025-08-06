import json
from typing import Dict
from app.config.azure_config import AzureAIConfig

class BrandEnforcer:
    def __init__(self, azure_config: AzureAIConfig):
        self.azure_config = azure_config
        self.client = azure_config.get_client("brand_enforcer")
        self.brand_voice = self._load_prompt("prompts/ing_brand_voice.txt")
        self.enforcement_prompt = self._load_prompt("prompts/brand_enforcer.txt")
    
    def _load_prompt(self, filepath: str) -> str:
        """Load prompt from text file"""
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return f"Default prompt for {filepath}"
    
    async def validate_brand_compliance(self, content: str) -> Dict:
        """Validate content against ING brand guidelines"""
        
        prompt = self.enforcement_prompt.format(
            content_to_validate=content,
            brand_guidelines=self.brand_voice,
            validation_criteria="tone, language, product positioning, customer focus"
        )
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=800
        )
        
        return json.loads(response.choices[0].message.content)