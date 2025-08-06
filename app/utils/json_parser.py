"""
Robust JSON parsing for LLM responses
"""
import json
import re
from typing import Any, Optional

def extract_json_from_response(response_text: str) -> Optional[Dict]:
    """Extract JSON from LLM response, handling markdown code blocks"""
    if not response_text:
        return None
    
    # Remove markdown code blocks
    cleaned = re.sub(r'```json\s*', '', response_text)
    cleaned = re.sub(r'```\s*', '', cleaned)
    cleaned = cleaned.strip()
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON within the text
        json_match = re.search(r'\{.*\}|\[.*\]', cleaned, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
    
    print(f"Failed to parse JSON from response: {response_text[:200]}...")
    return None