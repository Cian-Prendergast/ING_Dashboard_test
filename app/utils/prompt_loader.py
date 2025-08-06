# ================================
# utils/prompt_loader.py - Centralized Prompt Management
# ================================

import os
from typing import Dict

class PromptLoader:
    """Centralized prompt loading and management"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = prompts_dir
        self._prompt_cache = {}
    
    def load_prompt(self, prompt_name: str) -> str:
        """Load prompt from file with caching"""
        if prompt_name in self._prompt_cache:
            return self._prompt_cache[prompt_name]
        
        filepath = os.path.join(self.prompts_dir, f"{prompt_name}.txt")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self._prompt_cache[prompt_name] = content
                return content
        except FileNotFoundError:
            print(f"Warning: Prompt file {filepath} not found")
            return self._get_fallback_prompt(prompt_name)
    
    def _get_fallback_prompt(self, prompt_name: str) -> str:
        """Fallback prompts for missing files"""
        fallbacks = {
            "news_scanner": "Analyze these articles for ING Bank relevance: {rss_articles}",
            "intent_extractor": "Extract search intents from: {news_articles}",
            "content_evaluator": "Evaluate content quality: {content}",
            "content_optimizer": "Optimize content for: {target_keywords}",
            "brand_enforcer": "Check brand compliance: {content}"
        }
        return fallbacks.get(prompt_name, "Default prompt for {prompt_name}")