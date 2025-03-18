import openai
import logging
from ..utils.config import OPENAI_API_KEY, TARGET_CHAR_COUNT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

class ContentGenerator:
    """Generates SEO-optimized content using OpenAI API."""
    
    def __init__(self):
        pass
    
    def generate_article(self, theme, seo_analysis):
        """Generate an SEO-optimized article based on theme and SEO analysis."""
        try:
            logger.info(f"Generating article for theme: {theme}")
            
            # Extract SEO insights
            top_keywords = list(seo_analysis["top_keywords"].keys())[:15]
            keywords_str = ", ".join(top_keywords)
            
            # Create heading structure based on competitor analysis
            heading_structure = self._generate_heading_structure(theme, seo_analysis)
            
            # Generate article content
            system_prompt = f"""
            You are an expert content writer specializing in SEO-optimized articles for the Japanese platform note.com.
            Your task is to write a comprehensive, engaging, and SEO-optimized article about {theme}.
            
            The article should:
            1. Be approximately {TARGET_CHAR_COUNT} characters long (Japanese characters)
            2. Include the following keywords naturally throughout the text: {keywords_str}
            3. Follow this heading structure: {heading_structure}
            4. Include approximately {int(seo_analysis["structure"]["avg_paragraphs"])} paragraphs
            5. Include approximately {int(seo_analysis["structure"]["avg_lists"])} lists
            6. Include approximately {int(seo_analysis["structure"]["avg_links"])} relevant links
            7. Suggest places where {int(seo_analysis["structure"]["avg_images"])} images could be added
            8. Be written in Japanese, with a friendly but professional tone
            9. Include a compelling introduction and conclusion
            10. Provide actionable insights and valuable information
            
            Format the article with proper HTML tags for headings (h1, h2, h3, etc.), paragraphs (p), lists (ul, li), and other elements.
            """
            
            user_prompt = f"Write a comprehensive article about {theme} that will outperform competitors in SEO rankings."
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            article_content = response.choices[0].message.content
            
            # Generate title
            title = self._generate_title(theme, seo_analysis)
            
            # Generate tags
            tags = self._generate_tags(theme, seo_analysis)
            
            return {
                "title": title,
                "content": article_content,
                "tags": tags
            }
        except Exception as e:
            logger.error(f"Failed to generate article: {str(e)}")
            raise
    
    def _generate_heading_structure(self, theme, seo_analysis):
        """Generate heading structure based on SEO analysis."""
        try:
            system_prompt = f"""
            You are an SEO expert. Based on the following analysis of successful articles about {theme},
            generate an optimal heading structure (H1, H2, H3) for a new article that will outperform competitors.
            
            The heading structure should:
            1. Include approximately {len(seo_analysis["heading_patterns"][0]) if seo_analysis["heading_patterns"] else 5} headings
            2. Follow a logical hierarchy
            3. Include important keywords naturally
            4. Be engaging and click-worthy
            
            Top keywords: {list(seo_analysis["top_keywords"].keys())[:10]}
            """
            
            user_prompt = f"Generate an optimal heading structure for an article about {theme}."
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            heading_structure = response.choices[0].message.content
            return heading_structure
        except Exception as e:
            logger.error(f"Failed to generate heading structure: {str(e)}")
            raise
    
    def _generate_title(self, theme, seo_analysis):
        """Generate an SEO-optimized title."""
        try:
            system_prompt = f"""
            You are an SEO expert. Generate an engaging, click-worthy title for an article about {theme}.
            
            The title should:
            1. Include important keywords
            2. Be approximately 40-60 characters long
            3. Be engaging and spark curiosity
            4. Outperform competitor titles in SEO rankings
            
            Top keywords: {list(seo_analysis["top_keywords"].keys())[:5]}
            Most successful competitor titles:
            - {seo_analysis["most_successful"]["most_viewed"]}
            - {seo_analysis["most_successful"]["most_liked"]}
            """
            
            user_prompt = f"Generate an SEO-optimized title for an article about {theme}."
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            title = response.choices[0].message.content.strip().replace('"', '')
            return title
        except Exception as e:
            logger.error(f"Failed to generate title: {str(e)}")
            raise
    
    def _generate_tags(self, theme, seo_analysis):
        """Generate SEO-optimized tags."""
        try:
            # Use top keywords as tags
            tags = list(seo_analysis["top_keywords"].keys())[:10]
            return tags
        except Exception as e:
            logger.error(f"Failed to generate tags: {str(e)}")
            raise
