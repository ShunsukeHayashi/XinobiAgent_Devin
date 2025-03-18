import gradio as gr
import asyncio
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.note_integration.main import NoteIntegration
from src.note_integration.utils.config import NOTE_USERNAME, NOTE_PASSWORD, OPENAI_API_KEY
from src.note_integration.auth.authenticator import NoteAuthenticator
from src.note_integration.api.note_api import NoteAPI
from src.note_integration.seo.analyzer import SEOAnalyzer
from src.note_integration.content.generator import ContentGenerator
from src.note_integration.posting.poster import NotePoster
from src.note_integration.web.mock_data import MOCK_SEO_ANALYSIS, MOCK_ARTICLE, MOCK_ARTICLE_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NoteWebUI:
    """Web UI for note.com integration using Gradio."""
    
    def __init__(self, use_mock=True):
        self.integration = NoteIntegration()
        self.initialized = False
        self.auth_token = None
        self.note_api = None
        self.seo_analyzer = None
        self.content_generator = None
        self.note_poster = None
        self.use_mock = use_mock
    
    async def initialize(self):
        """Initialize the note.com integration."""
        try:
            if self.initialized:
                return "✅ すでに初期化されています。"
            
            logger.info("Initializing note.com integration")
            
            if self.use_mock:
                logger.info("Using mock data for demonstration")
                self.initialized = True
                return "✅ 初期化成功: デモモードで初期化しました。実際のnote.comへの接続は行いません。"
            
            # Initialize components manually to have more control
            # Authenticate with note.com
            authenticator = NoteAuthenticator()
            self.auth_token = await authenticator.login()
            
            if not self.auth_token:
                return "❌ 認証失敗: note.comへのログインに失敗しました。"
            
            # Initialize API client
            self.note_api = NoteAPI(self.auth_token)
            
            # Initialize SEO analyzer
            self.seo_analyzer = SEOAnalyzer(self.note_api)
            
            # Initialize content generator
            self.content_generator = ContentGenerator()
            
            # Initialize note poster
            self.note_poster = NotePoster(self.auth_token)
            
            # Set initialized flag
            self.initialized = True
            
            return "✅ 初期化成功: note.comへの認証とAPIの初期化が完了しました。"
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            return f"❌ エラー: {str(e)}"
    
    async def generate_and_post_article(self, theme, category):
        """Generate and post an article to note.com."""
        try:
            if not self.initialized:
                init_message = await self.initialize()
                if "❌" in init_message:
                    return init_message
            
            if not theme or not category:
                return "❌ テーマとカテゴリーを入力してください。"
            
            logger.info(f"Generating and posting article for theme: {theme}, category: {category}")
            
            if self.use_mock:
                # Use mock data for demonstration
                logger.info("Using mock data for article generation and posting")
                await asyncio.sleep(2)  # Simulate processing time
                return f"✅ 記事投稿成功 (デモモード): {MOCK_ARTICLE_URL}"
            
            # Get creator info
            creator_info = self.note_api.get_creator_info(NOTE_USERNAME)
            if not creator_info or "data" not in creator_info or "id" not in creator_info["data"]:
                return "❌ クリエイター情報の取得に失敗しました。"
            
            # Analyze competitors
            seo_analysis = self.seo_analyzer.analyze_competitors(category)
            if not seo_analysis:
                return "❌ SEO分析に失敗しました。"
            
            # Generate article
            article = self.content_generator.generate_article(theme, seo_analysis)
            if not article:
                return "❌ 記事生成に失敗しました。"
            
            # Post article
            article_url = await self.note_poster.post_article(article)
            if not article_url:
                return "❌ 記事投稿に失敗しました。"
            
            return f"✅ 記事投稿成功: {article_url}"
        except Exception as e:
            logger.error(f"Article generation and posting failed: {str(e)}")
            return f"❌ エラー: {str(e)}"
    
    async def analyze_seo(self, category):
        """Analyze SEO for a category."""
        try:
            if not self.initialized:
                init_message = await self.initialize()
                if "❌" in init_message:
                    return init_message
            
            if not category:
                return "❌ カテゴリーを入力してください。"
            
            logger.info(f"Analyzing SEO for category: {category}")
            
            if self.use_mock:
                # Use mock data for demonstration
                logger.info("Using mock data for SEO analysis")
                await asyncio.sleep(2)  # Simulate processing time
                seo_analysis = MOCK_SEO_ANALYSIS
            else:
                # Analyze competitors
                seo_analysis = self.seo_analyzer.analyze_competitors(category)
            
            if seo_analysis:
                # Format the analysis results
                top_keywords = list(seo_analysis["top_keywords"].keys())[:10]
                most_viewed = seo_analysis["most_successful"]["most_viewed"]
                most_liked = seo_analysis["most_successful"]["most_liked"]
                
                result = f"""
                ## SEO分析結果: {category}
                
                ### トップキーワード
                {', '.join(top_keywords)}
                
                ### 最も閲覧された記事
                {most_viewed}
                
                ### 最も「いいね」された記事
                {most_liked}
                
                ### 記事構造の分析
                - 平均段落数: {seo_analysis["structure"]["avg_paragraphs"]}
                - 平均リスト数: {seo_analysis["structure"]["avg_lists"]}
                - 平均リンク数: {seo_analysis["structure"]["avg_links"]}
                - 平均画像数: {seo_analysis["structure"]["avg_images"]}
                """
                
                return result
            else:
                return "❌ SEO分析に失敗しました。"
        except Exception as e:
            logger.error(f"SEO analysis failed: {str(e)}")
            return f"❌ エラー: {str(e)}"
    
    def preview_article(self, theme, category):
        """Preview a generated article."""
        try:
            if not theme or not category:
                return "❌ テーマとカテゴリーを入力してください。"
            
            logger.info(f"Previewing article for theme: {theme}, category: {category}")
            
            # Use mock data for demonstration
            article = MOCK_ARTICLE
            
            return f"""
            # プレビュー: {article['title']}
            
            ## タグ
            {', '.join(article['tags'])}
            
            ## 本文
            {article['content']}
            """
        except Exception as e:
            logger.error(f"Article preview failed: {str(e)}")
            return f"❌ エラー: {str(e)}"
    
    def check_env_vars(self):
        """Check if environment variables are set."""
        missing_vars = []
        
        if not NOTE_USERNAME:
            missing_vars.append("NOTE_USERNAME")
        
        if not NOTE_PASSWORD:
            missing_vars.append("NOTE_PASSWORD")
        
        if not OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")
        
        if missing_vars:
            return f"❌ 以下の環境変数が設定されていません: {', '.join(missing_vars)}"
        else:
            return "✅ すべての環境変数が設定されています。"
    
    def create_ui(self):
        """Create the Gradio UI."""
        with gr.Blocks(title="note.com自動投稿システム") as app:
            gr.Markdown("# note.com自動投稿システム")
            gr.Markdown("このシステムは、SEO分析に基づいて最適化された記事を自動的に生成し、note.comに投稿します。")
            
            if self.use_mock:
                gr.Markdown("### ℹ️ デモモード: 実際のnote.comへの接続は行わず、モックデータを使用します。")
            
            env_check = self.check_env_vars()
            if "❌" in env_check and not self.use_mock:
                gr.Markdown(f"### ⚠️ 警告: {env_check}")
                gr.Markdown("""
                環境変数または.envファイルで以下の変数を設定してください：
                
                ```
                NOTE_USERNAME=あなたのnote.comユーザー名
                NOTE_PASSWORD=あなたのnote.comパスワード
                OPENAI_API_KEY=あなたのOpenAI APIキー
                ```
                """)
            
            with gr.Tab("初期化"):
                init_button = gr.Button("システムを初期化", variant="primary")
                init_output = gr.Textbox(label="初期化結果", lines=2)
                
                init_button.click(
                    fn=lambda: asyncio.run(self.initialize()),
                    outputs=init_output
                )
            
            with gr.Tab("SEO分析"):
                category_input = gr.Textbox(label="カテゴリー", placeholder="例: programming, business, lifestyle")
                analyze_button = gr.Button("SEO分析を実行", variant="primary")
                analysis_output = gr.Markdown(label="分析結果")
                
                analyze_button.click(
                    fn=lambda category: asyncio.run(self.analyze_seo(category)),
                    inputs=category_input,
                    outputs=analysis_output
                )
            
            with gr.Tab("記事プレビュー"):
                theme_input_preview = gr.Textbox(label="テーマ", placeholder="例: Pythonプログラミングのコツ")
                category_input_preview = gr.Textbox(label="カテゴリー", placeholder="例: programming")
                preview_button = gr.Button("記事をプレビュー", variant="primary")
                preview_output = gr.Markdown(label="プレビュー")
                
                preview_button.click(
                    fn=self.preview_article,
                    inputs=[theme_input_preview, category_input_preview],
                    outputs=preview_output
                )
            
            with gr.Tab("記事生成と投稿"):
                theme_input = gr.Textbox(label="テーマ", placeholder="例: Pythonプログラミングのコツ")
                category_input2 = gr.Textbox(label="カテゴリー", placeholder="例: programming")
                post_button = gr.Button("記事を生成して投稿", variant="primary")
                post_output = gr.Textbox(label="投稿結果", lines=2)
                
                post_button.click(
                    fn=lambda theme, category: asyncio.run(self.generate_and_post_article(theme, category)),
                    inputs=[theme_input, category_input2],
                    outputs=post_output
                )
            
            with gr.Tab("設定情報"):
                gr.Markdown("## 現在の設定")
                
                username_display = gr.Textbox(label="note.comユーザー名", value=NOTE_USERNAME or "未設定")
                password_display = gr.Textbox(label="note.comパスワード", value="*****" if NOTE_PASSWORD else "未設定")
                openai_display = gr.Textbox(label="OpenAI APIキー", value="*****" if OPENAI_API_KEY else "未設定")
                
                if self.use_mock:
                    gr.Markdown("""
                    ## デモモード情報
                    
                    現在、デモモードで実行しています。実際のnote.comへの接続は行わず、モックデータを使用します。
                    本番環境で使用する場合は、以下の環境変数を設定してください。
                    """)
                
                gr.Markdown("""
                ## 設定方法
                
                環境変数または.envファイルで以下の変数を設定してください：
                
                ```
                NOTE_USERNAME=あなたのnote.comユーザー名
                NOTE_PASSWORD=あなたのnote.comパスワード
                OPENAI_API_KEY=あなたのOpenAI APIキー
                ```
                """)
        
        return app

def main():
    """Main function to run the web UI."""
    ui = NoteWebUI(use_mock=True)  # Use mock data by default
    app = ui.create_ui()
    app.launch(share=True)

if __name__ == "__main__":
    main()
