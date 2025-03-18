import requests
from bs4 import BeautifulSoup
import logging
import re
from collections import Counter
from ..api.note_api import NoteAPI
from ..utils.config import COMPETITOR_ANALYSIS_COUNT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SEOAnalyzer:
    """Analyzes competitor content for SEO optimization."""
    
    def __init__(self, note_api):
        self.note_api = note_api
    
    def analyze_competitors(self, category):
        """Analyze competitor content in the specified category."""
        try:
            # Get top notes in the category
            logger.info(f"Analyzing top {COMPETITOR_ANALYSIS_COUNT} notes in category: {category}")
            notes_data = self.note_api.get_notes_by_category(category, COMPETITOR_ANALYSIS_COUNT)
            
            if not notes_data or "data" not in notes_data or "notes" not in notes_data["data"]:
                logger.error("Failed to get competitor notes")
                return None
            
            notes = notes_data["data"]["notes"]
            
            # Analyze each note
            analysis_results = []
            for note in notes:
                analysis = self._analyze_note(note)
                analysis_results.append(analysis)
            
            # Aggregate analysis results
            aggregated_analysis = self._aggregate_analysis(analysis_results)
            
            return aggregated_analysis
        except Exception as e:
            logger.error(f"Failed to analyze competitors: {str(e)}")
            raise
    
    def _analyze_note(self, note):
        """Analyze a single note for SEO factors."""
        try:
            # Extract text content
            soup = BeautifulSoup(note["body"], "html.parser")
            text_content = soup.get_text()
            
            # Count words
            words = re.findall(r'\w+', text_content.lower())
            word_count = len(words)
            
            # Count characters
            char_count = len(text_content)
            
            # Analyze keyword density
            word_freq = Counter(words)
            total_words = len(words)
            keyword_density = {word: count/total_words for word, count in word_freq.most_common(20)}
            
            # Analyze headings
            headings = []
            for i in range(1, 7):
                h_tags = soup.find_all(f'h{i}')
                for tag in h_tags:
                    headings.append({
                        "level": i,
                        "text": tag.get_text().strip()
                    })
            
            # Analyze structure
            paragraphs = len(soup.find_all('p'))
            lists = len(soup.find_all(['ul', 'ol']))
            images = len(soup.find_all('img'))
            links = len(soup.find_all('a'))
            
            return {
                "id": note["id"],
                "title": note["title"],
                "word_count": word_count,
                "char_count": char_count,
                "keyword_density": keyword_density,
                "headings": headings,
                "structure": {
                    "paragraphs": paragraphs,
                    "lists": lists,
                    "images": images,
                    "links": links
                },
                "engagement": {
                    "likes": note["likeCount"],
                    "views": note["viewCount"],
                    "comments": note["commentCount"]
                }
            }
        except Exception as e:
            logger.error(f"Failed to analyze note: {str(e)}")
            return None
    
    def _aggregate_analysis(self, analysis_results):
        """Aggregate analysis results from multiple notes."""
        if not analysis_results:
            return None
        
        # Filter out None results
        valid_results = [r for r in analysis_results if r is not None]
        if not valid_results:
            return None
        
        # Calculate averages
        avg_word_count = sum(r["word_count"] for r in valid_results) / len(valid_results)
        avg_char_count = sum(r["char_count"] for r in valid_results) / len(valid_results)
        
        # Aggregate keyword density
        all_keywords = {}
        for result in valid_results:
            for keyword, density in result["keyword_density"].items():
                if keyword in all_keywords:
                    all_keywords[keyword] += density
                else:
                    all_keywords[keyword] = density
        
        # Average keyword density
        for keyword in all_keywords:
            all_keywords[keyword] /= len(valid_results)
        
        # Sort by density
        top_keywords = dict(sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:30])
        
        # Analyze heading patterns
        heading_patterns = []
        for result in valid_results:
            if "headings" in result and result["headings"]:
                heading_pattern = [h["level"] for h in result["headings"]]
                heading_patterns.append(heading_pattern)
        
        # Analyze structure patterns
        avg_paragraphs = sum(r["structure"]["paragraphs"] for r in valid_results) / len(valid_results)
        avg_lists = sum(r["structure"]["lists"] for r in valid_results) / len(valid_results)
        avg_images = sum(r["structure"]["images"] for r in valid_results) / len(valid_results)
        avg_links = sum(r["structure"]["links"] for r in valid_results) / len(valid_results)
        
        # Analyze engagement metrics
        avg_likes = sum(r["engagement"]["likes"] for r in valid_results) / len(valid_results)
        avg_views = sum(r["engagement"]["views"] for r in valid_results) / len(valid_results)
        avg_comments = sum(r["engagement"]["comments"] for r in valid_results) / len(valid_results)
        
        # Find most successful article
        most_viewed = max(valid_results, key=lambda x: x["engagement"]["views"])
        most_liked = max(valid_results, key=lambda x: x["engagement"]["likes"])
        
        return {
            "avg_word_count": avg_word_count,
            "avg_char_count": avg_char_count,
            "target_char_count": 10000,  # Our target
            "top_keywords": top_keywords,
            "heading_patterns": heading_patterns,
            "structure": {
                "avg_paragraphs": avg_paragraphs,
                "avg_lists": avg_lists,
                "avg_images": avg_images,
                "avg_links": avg_links
            },
            "engagement": {
                "avg_likes": avg_likes,
                "avg_views": avg_views,
                "avg_comments": avg_comments
            },
            "most_successful": {
                "most_viewed": most_viewed["title"],
                "most_liked": most_liked["title"]
            }
        }
