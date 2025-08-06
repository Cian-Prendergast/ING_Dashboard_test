# ================================
# services/rss_service.py - Enhanced RSS Management
# ================================

import aiohttp
import feedparser
from typing import List, Dict

class RSSService:
    def __init__(self):
        self.rss_sources = {
            "yahoo_finance": "https://feeds.yahoo.com/rss/markets",
            "marketwatch": "https://feeds.marketwatch.com/marketwatch/topstories/",
            "dnb_news": "https://www.dnb.nl/en/rss/",
            "afm_news": "https://www.afm.nl/en/rss",
            "ecb_press": "https://www.ecb.europa.eu/press/pressreleases/rss.xml",
            "fd_banking": "https://fd.nl/rss/banking"  # Het Financieele Dagblad
        }
    
    async def fetch_all_feeds(self) -> List[Dict]:
        """Fetch articles from all RSS sources"""
        all_articles = []
        
        async with aiohttp.ClientSession() as session:
            for source_name, rss_url in self.rss_sources.items():
                try:
                    articles = await self._fetch_single_feed(session, rss_url, source_name)
                    all_articles.extend(articles)
                except Exception as e:
                    print(f"RSS fetch failed for {source_name}: {e}")
                    continue
        
        return sorted(all_articles, key=lambda x: x.get('published_date', ''), reverse=True)[:20]
    
    async def _fetch_single_feed(self, session: aiohttp.ClientSession, url: str, source: str) -> List[Dict]:
        """Fetch single RSS feed"""
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                content = await response.text()
                feed = feedparser.parse(content)
                
                articles = []
                for entry in feed.entries[:5]:
                    articles.append({
                        'headline': entry.get('title', ''),
                        'summary': entry.get('summary', ''),
                        'url': entry.get('link', ''),
                        'published_date': entry.get('published', ''),
                        'source': source,
                        'raw_entry': entry
                    })
                return articles
        return []