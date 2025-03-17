"""
Web Interface for Canva Slide Generator

This module provides a simple web interface for the Canva Slide Generator,
allowing users to input prompts and generate presentations.
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional, List

import gradio as gr

from app.examples.canva_slide_generator.slide_generator import generate_slides_from_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_slides(
    prompt: str,
    num_slides: int,
    title: str,
    template_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate slides from a prompt using the Canva API.
    
    Args:
        prompt: Text prompt describing the desired presentation
        num_slides: Number of slides to generate
        title: Title for the presentation
        template_type: Optional template type to apply
        
    Returns:
        Dictionary containing the generated presentation details
    """
    try:
        # Get API key from environment variable
        api_key = os.environ.get("CANVA_API_KEY")
        
        if not api_key:
            logger.warning("No Canva API key found in environment variables. Using mock API responses.")
        
        # Generate slides
        result = await generate_slides_from_prompt(
            prompt=prompt,
            num_slides=num_slides,
            title=title,
            api_key=api_key,
            template_type=template_type,
        )
        
        return {
            "status": "success",
            "result": result,
        }
    except Exception as e:
        logger.exception(f"Error generating slides: {e}")
        return {
            "status": "error",
            "error": str(e),
        }

def create_web_interface():
    """
    Create a Gradio web interface for the Canva Slide Generator.
    
    Returns:
        Gradio interface
    """
    with gr.Blocks(title="Canva Slide Generator") as interface:
        gr.Markdown("# Canva Slide Generator")
        gr.Markdown("プロンプトからプレゼンテーションスライドを自動生成します。")
        
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(
                    label="プロンプト",
                    placeholder="例: AIの最新トレンドについてのビジネスプレゼンテーション",
                    lines=5,
                )
                title_input = gr.Textbox(
                    label="タイトル",
                    placeholder="例: AI最新動向 2025",
                )
                num_slides_input = gr.Slider(
                    label="スライド数",
                    minimum=1,
                    maximum=20,
                    value=5,
                    step=1,
                )
                template_input = gr.Dropdown(
                    label="テンプレートタイプ",
                    choices=[
                        "自動選択",
                        "タイムライン",
                        "フロー図",
                        "サイクル",
                        "アイコン",
                        "ボックス",
                        "箇条書き",
                    ],
                    value="自動選択",
                )
                generate_button = gr.Button("スライド生成")
            
            with gr.Column():
                output = gr.JSON(label="結果")
        
        def handle_generate(prompt, title, num_slides, template):
            """
            Handle the generate button click.
            """
            if not prompt:
                return {"error": "プロンプトを入力してください。"}
            
            if not title:
                title = f"Presentation: {prompt[:30]}..."
            
            # Map template names to types
            template_map = {
                "自動選択": None,
                "タイムライン": "timeline",
                "フロー図": "arrows",
                "サイクル": "cycle",
                "アイコン": "icons",
                "ボックス": "boxes",
                "箇条書き": "bullets",
            }
            
            template_type = template_map.get(template)
            
            # Run the async function in a new event loop
            result = asyncio.run(generate_slides(
                prompt, 
                int(num_slides), 
                title,
                template_type,
            ))
            return result
        
        generate_button.click(
            fn=handle_generate,
            inputs=[prompt_input, title_input, num_slides_input, template_input],
            outputs=[output],
        )
    
    return interface

def launch_web_interface():
    """
    Launch the web interface.
    """
    interface = create_web_interface()
    interface.launch(share=True)

if __name__ == "__main__":
    launch_web_interface()
