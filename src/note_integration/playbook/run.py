#!/usr/bin/env python3
"""
Command-line interface for note.com integration system playbook.
"""
import os
import sys
import json
import logging
import argparse
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.note_integration.playbook.executor import PlaybookExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to run the playbook."""
    parser = argparse.ArgumentParser(description="Run note.com integration system playbook")
    parser.add_argument("--theme", type=str, help="Theme for the article")
    parser.add_argument("--genre", type=str, help="Genre for the article")
    parser.add_argument("--input", type=str, help="Additional input for the article")
    parser.add_argument("--use-mock", action="store_true", help="Use mock data instead of real API")
    parser.add_argument("--no-mock", action="store_true", help="Don't use mock data")
    parser.add_argument("--output", type=str, default="results.json", help="Path to save the results")
    parser.add_argument("--playbook-output", type=str, default="playbook.md", help="Path to save the playbook")
    args = parser.parse_args()
    
    # Interactive mode if theme or genre not provided
    if not args.theme:
        args.theme = input("テーマを入力してください: ")
    
    if not args.genre:
        args.genre = input("ジャンルを入力してください: ")
    
    if not args.input:
        args.input = input("追加入力（任意）: ")
    
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
    logger.info(f"Playbook saved to {args.playbook_output}")
    
    # Execute the playbook
    import asyncio
    results = asyncio.run(executor.execute(args.theme, args.genre, args.input))
    
    # Save the results
    executor.save_results(results, args.output)
    
    # Print the results
    print("\n" + "="*50)
    print("プレイブック実行結果")
    print("="*50)
    
    print(f"初期化: {'成功' if '❌' not in results.get('initialization', '') else '失敗'}")
    print(f"SEO分析: {'成功' if '❌' not in results.get('seo_analysis', '') else '失敗'}")
    print(f"記事生成: {'成功' if '❌' not in results.get('article_generation', '') else '失敗'}")
    print(f"記事投稿: {'成功' if '❌' not in results.get('article_posting', '') else '失敗'}")
    
    if "article_url" in results:
        print(f"\n記事URL: {results['article_url']}")
    
    print(f"\n詳細結果は {args.output} に保存されました。")
    print(f"プレイブックは {args.playbook_output} に保存されました。")

if __name__ == "__main__":
    main()
