# services/content_service.py (expanded)
from typing import List, Dict

class ContentService:
    async def get_pipeline_status(self) -> List[Dict]:
        """Get current content pipeline status"""
        # This would integrate with your content management system
        return [
            {
                "title": "ECB Rate Impact Analysis",
                "status": "Optimizing",
                "progress": 75,
                "description": "AI Overview optimization in progress"
            },
            {
                "title": "Digital Banking Security Guide", 
                "status": "Brand Review",
                "progress": 90,
                "description": "Final brand compliance check"
            }
        ]