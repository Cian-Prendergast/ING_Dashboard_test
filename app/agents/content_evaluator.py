# ================================
# agents/content_evaluator.py - AI Overview Inclusion Predictor
# ================================

import json
from typing import List, Dict
from app.config.azure_config import AzureAIConfig

class ContentEvaluator:
    def __init__(self, azure_config: AzureAIConfig):
        self.azure_config = azure_config
        self.client = azure_config.get_client("content_evaluator") 
        self.prompt_template = self._load_prompt("prompts/content_evaluator.txt")
    
    def _load_prompt(self, filepath: str) -> str:
        """Load prompt from text file"""
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return f"Default prompt for {filepath}"
    
    async def evaluate_content(self, keywords: List[str], competitor_snippets: List[Dict]) -> Dict:
        """Evaluate ING content vs AI Overview winners"""
        
        # Get current ING content for keywords
        ing_content = await self._get_ing_content_for_keywords(keywords)
        
        prompt = self.prompt_template.format(
            target_keywords=", ".join(keywords),
            ing_current_content=json.dumps(ing_content, indent=2),
            competitor_snippets=json.dumps(competitor_snippets, indent=2),
            evaluation_criteria="AI Overview inclusion factors"
        )
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1800
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def predict_inclusion_probability(self, content: Dict, competitors: List[Dict], keywords: List[str]) -> Dict:
        """Predict AI Overview inclusion probability using LLM reasoning"""
        
        prediction_prompt = f"""
        Analyze this optimized content for AI Overview inclusion probability:
        
        CONTENT: {json.dumps(content, indent=2)}
        COMPETITORS: {json.dumps(competitors, indent=2)}
        TARGET KEYWORDS: {', '.join(keywords)}
        
        Provide:
        1. Inclusion probability (0-100) with detailed reasoning
        2. Specific strengths vs competitors
        3. Remaining weaknesses to address
        4. Confidence level in prediction
        
        Return structured JSON response.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prediction_prompt}],
            temperature=0.1,  # Low temperature for consistent predictions
            max_tokens=1200
        )
        
        return json.loads(response.choices[0].message.content)