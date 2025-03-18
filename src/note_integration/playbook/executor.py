#!/usr/bin/env python3
"""
Executor for note.com integration system playbook.
"""
import os
import sys
import json
import logging
import argparse
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.note_integration.web.app import NoteWebUI
from src.note_integration.playbook.template import generate_playbook, DEFAULT_PLAYBOOK_DATA

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlaybookExecutor:
    """
    Executor for note.com integration system playbook.
    """
    def __init__(self, use_mock: bool = None):
        """
        Initialize the playbook executor.
        
        Args:
            use_mock: Whether to use mock data. If None, determined from environment variables.
        """
        self.ui = NoteWebUI(use_mock=use_mock)
        self.playbook_data = DEFAULT_PLAYBOOK_DATA.copy()
        
    async def execute(self, theme: str, genre: str, additional_input: str = "") -> Dict[str, Any]:
        """
        Execute the playbook with the given theme and genre.
        
        Args:
            theme: Theme for the article
            genre: Genre for the article
            additional_input: Additional input for the article
            
        Returns:
            Dict[str, Any]: Results of the execution
        """
        results = {}
        
        # Update user input in playbook data
        user_input = f"テーマ: {theme}\nジャンル: {genre}"
        if additional_input:
            user_input += f"\n追加入力: {additional_input}"
        self.playbook_data["user_input"] = user_input
        
        # Step 1: Initialize system
        logger.info("Step 1: Initializing system...")
        init_result = await self.ui.initialize()
        results["initialization"] = init_result
        
        # Step 2: Analyze SEO
        logger.info("Step 2: Analyzing SEO...")
        category = f"{theme} {genre}"
        seo_result = await self.ui.analyze_seo(category)
        results["seo_analysis"] = seo_result
        
        # Step 3: Generate article
        logger.info("Step 3: Generating article...")
        article_result = await self.ui.generate_article(theme, genre, additional_input)
        results["article_generation"] = article_result
        
        # Step 4: Post article
        logger.info("Step 4: Posting article...")
        post_result = await self.ui.post_article()
        results["article_posting"] = post_result
        
        # Step 5: Report results
        logger.info("Step 5: Reporting results...")
        if "url" in post_result:
            results["article_url"] = post_result["url"]
        
        return results
    
    def generate_playbook(self) -> str:
        """
        Generate a playbook from the current playbook data.
        
        Returns:
            str: Generated playbook
        """
        return generate_playbook(self.playbook_data)
    
    def save_results(self, results: Dict[str, Any], filepath: str) -> None:
        """
        Save the results to a file.
        
        Args:
            results: Results to save
            filepath: Path to save the results
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

def main():
    """Main function to run the playbook executor."""
    parser = argparse.ArgumentParser(description="Execute note.com integration system playbook")
    parser.add_argument("--theme", type=str, required=True, help="Theme for the article")
    parser.add_argument("--genre", type=str, required=True, help="Genre for the article")
    parser.add_argument("--additional-input", type=str, default="", help="Additional input for the article")
    parser.add_argument("--use-mock", action="store_true", help="Use mock data instead of real API")
    parser.add_argument("--no-mock", action="store_true", help="Don't use mock data")
    parser.add_argument("--output", type=str, default="results.json", help="Path to save the results")
    parser.add_argument("--playbook-output", type=str, default="playbook.md", help="Path to save the playbook")
    args = parser.parse_args()
    
    # Set environment variables if not already set
    if not os.environ.get("NOTE_USERNAME"):
        os.environ["NOTE_USERNAME"] = "shunsuke_ai"
    
    if not os.environ.get("NOTE_PASSWORD"):
        os.environ["NOTE_PASSWORD"] = "Jin156762syun@"
    
    if not os.environ.get("OPENAI_API_KEY") and os.environ.get("API_Key"):
        api_key = os.environ.get("API_Key")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    
    # Determine mock mode
    use_mock = None
    if args.use_mock:
        use_mock = True
    elif args.no_mock:
        use_mock = False
    
    # Create and execute the playbook
    executor = PlaybookExecutor(use_mock=use_mock)
    
    # Generate and save the playbook
    playbook = executor.generate_playbook()
    with open(args.playbook_output, 'w', encoding='utf-8') as f:
        f.write(playbook)
    
    # Execute the playbook
    results = asyncio.run(executor.execute(args.theme, args.genre, args.additional_input))
    
    # Save the results
    executor.save_results(results, args.output)
    
    # Print the results
    print(f"Playbook execution completed. Results saved to {args.output}")
    if "article_url" in results:
        print(f"Article URL: {results['article_url']}")

if __name__ == "__main__":
    main()
