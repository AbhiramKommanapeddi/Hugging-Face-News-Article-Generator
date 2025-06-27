#!/usr/bin/env python3
"""
Gradio interface for the Hugging Face News Article Generator.
Provides an intuitive web interface for article generation.
"""

import gradio as gr
import sys
import os
import json
from typing import List, Dict, Tuple

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.news_generator import NewsGenerator
from src.style_manager import StyleManager
from src.fact_checker import FactChecker
from src.quality_metrics import QualityMetrics
from src.utils import load_sample_topics, create_article_summary

# Initialize generators (will be loaded when first used)
news_gen = None
style_mgr = None
fact_checker = None
quality_checker = None

def initialize_models():
    """Initialize models when first needed."""
    global news_gen, style_mgr, fact_checker, quality_checker
    
    if news_gen is None:
        news_gen = NewsGenerator()
        style_mgr = StyleManager()
        fact_checker = FactChecker()
        quality_checker = QualityMetrics()

def generate_article_interface(
    headline: str,
    facts: str,
    quotes: str,
    style: str,
    target_length: int,
    location: str,
    category: str,
    enable_fact_check: bool,
    enable_quality_check: bool,
    enable_style_check: bool
) -> Tuple[str, str, str, str]:
    """
    Generate article through Gradio interface.
    
    Returns:
        Tuple of (article_text, fact_check_report, quality_report, style_report)
    """
    try:
        # Initialize models if needed
        initialize_models()
        
        # Parse inputs
        facts_list = [fact.strip() for fact in facts.split('\n') if fact.strip()]
        
        quotes_list = []
        if quotes.strip():
            try:
                quotes_list = json.loads(quotes)
            except json.JSONDecodeError:
                quotes_list = []
        
        # Generate article
        article_data = news_gen.generate_article(
            headline=headline,
            facts=facts_list,
            quotes=quotes_list,
            style=style,
            target_length=target_length
        )
        
        # Add metadata
        article_data['location'] = location
        article_data['topic_category'] = category
        
        # Get article text
        article_text = article_data['full_article']
        
        # Perform analysis
        fact_check_report = ""
        if enable_fact_check:
            fact_check_result = fact_checker.verify_facts(article_text, facts_list)
            fact_check_report = format_fact_check_report(fact_check_result)
        
        quality_report = ""
        if enable_quality_check:
            quality_result = quality_checker.evaluate_article(article_data)
            quality_report = format_quality_report(quality_result)
        
        style_report = ""
        if enable_style_check:
            style_result = style_mgr.validate_style_compliance(article_text, style)
            style_report = format_style_report(style_result)
        
        return article_text, fact_check_report, quality_report, style_report
        
    except Exception as e:
        error_msg = f"Error generating article: {str(e)}"
        return error_msg, "", "", ""

def generate_sample_article() -> Tuple[str, str, str, str, str, str]:
    """
    Generate a sample article from predefined topics.
    
    Returns:
        Tuple of (headline, facts, quotes, location, category, style)
    """
    try:
        sample_topics = load_sample_topics()
        import random
        topic = random.choice(sample_topics)
        
        headline = topic['headline']
        facts = '\n'.join(topic['facts'])
        quotes = json.dumps(topic.get('quotes', []), indent=2)
        location = topic.get('location', '')
        category = topic.get('category', 'General')
        style = 'news'
        
        return headline, facts, quotes, location, category, style
        
    except Exception as e:
        return f"Error loading sample: {str(e)}", "", "", "", "", "news"

def format_fact_check_report(fact_check_result: Dict) -> str:
    """Format fact checking results for display."""
    if not fact_check_result:
        return "No fact check performed."
    
    report = f"""FACT CHECK REPORT
=================

Overall Score: {fact_check_result['overall_score']}/100

DETAILED SCORES:
• Objectivity: {fact_check_result['objectivity_score']}/100
• Source Attribution: {fact_check_result['source_attribution_score']}/100
• Fact Consistency: {fact_check_result['fact_consistency_score']}/100
• Credibility: {fact_check_result['credibility_score']}/100

RECOMMENDATIONS:
"""
    
    for rec in fact_check_result.get('recommendations', []):
        report += f"• {rec}\n"
    
    if fact_check_result.get('flagged_content'):
        report += "\nFLAGGED CONTENT:\n"
        for item in fact_check_result['flagged_content']:
            report += f"⚠️ {item['type']}: '{item['content']}' (Severity: {item['severity']})\n"
    
    return report

def format_quality_report(quality_result: Dict) -> str:
    """Format quality evaluation results for display."""
    if not quality_result:
        return "No quality evaluation performed."
    
    report = f"""QUALITY EVALUATION REPORT
========================

Overall Score: {quality_result['overall_score']}/100
Professional Rating: {quality_result['professional_rating']}

CATEGORY SCORES:
"""
    
    for category, data in quality_result['category_scores'].items():
        score = data['score'] if isinstance(data, dict) else data
        report += f"• {category.replace('_', ' ').title()}: {score}/100\n"
    
    report += "\nSTRENGTHS:\n"
    for strength in quality_result.get('strengths', []):
        report += f"✅ {strength}\n"
    
    report += "\nAREAS FOR IMPROVEMENT:\n"
    for improvement in quality_result.get('areas_for_improvement', []):
        report += f"📈 {improvement}\n"
    
    return report

def format_style_report(style_result: Dict) -> str:
    """Format style compliance results for display."""
    if not style_result:
        return "No style check performed."
    
    report = f"""STYLE COMPLIANCE REPORT
======================

Style: {style_result['style'].title()}
Compliance Score: {style_result['score']}/100

"""
    
    if style_result.get('issues'):
        report += "ISSUES FOUND:\n"
        for issue in style_result['issues']:
            report += f"❌ {issue}\n"
    
    if style_result.get('suggestions'):
        report += "\nSUGGESTIONS:\n"
        for suggestion in style_result['suggestions']:
            report += f"💡 {suggestion}\n"
    
    return report

def create_gradio_interface():
    """Create and configure the Gradio interface."""
    
    # Custom CSS for better styling
    css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .gr-button-primary {
        background: linear-gradient(45deg, #2196F3, #21CBF3);
        border: none;
    }
    .gr-textbox {
        border-radius: 8px;
    }
    """
    
    with gr.Blocks(css=css, title="News Article Generator") as interface:
        
        # Header
        gr.Markdown("""
        # 📰 Hugging Face News Article Generator
        
        Generate professional news articles using state-of-the-art AI models with built-in fact-checking and quality analysis.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Input section
                gr.Markdown("## Article Configuration")
                
                headline = gr.Textbox(
                    label="Article Headline",
                    placeholder="Enter your news headline here...",
                    lines=2
                )
                
                facts = gr.Textbox(
                    label="Key Facts (one per line)",
                    placeholder="Enter key facts, one per line...",
                    lines=8
                )
                
                quotes = gr.Textbox(
                    label="Quotes (JSON format)",
                    placeholder='[{"quote": "Quote text", "speaker": "Speaker Name", "title": "Speaker Title"}]',
                    lines=5
                )
                
                with gr.Row():
                    location = gr.Textbox(
                        label="Location",
                        placeholder="City, State"
                    )
                    category = gr.Dropdown(
                        label="Category",
                        choices=["Technology", "Business", "Sports", "Health", "Politics", 
                                "Environment", "Education", "Entertainment", "Science", "General"],
                        value="General"
                    )
                
                with gr.Row():
                    style = gr.Dropdown(
                        label="Article Style",
                        choices=["news", "blog", "social", "newsletter"],
                        value="news"
                    )
                    target_length = gr.Slider(
                        label="Target Word Count",
                        minimum=200,
                        maximum=1500,
                        value=500,
                        step=50
                    )
                
                # Analysis options
                gr.Markdown("### Analysis Options")
                with gr.Row():
                    enable_fact_check = gr.Checkbox(label="Fact Checking", value=True)
                    enable_quality_check = gr.Checkbox(label="Quality Analysis", value=True)
                    enable_style_check = gr.Checkbox(label="Style Compliance", value=True)
                
                # Buttons
                with gr.Row():
                    generate_btn = gr.Button("Generate Article", variant="primary", size="lg")
                    sample_btn = gr.Button("Load Sample Topic", variant="secondary")
                    clear_btn = gr.Button("Clear All", variant="secondary")
            
            with gr.Column(scale=1):
                # Tips and help
                gr.Markdown("""
                ## 💡 Tips for Better Articles
                
                **Headlines:**
                - Be specific and descriptive
                - Include key information
                - Keep under 10 words when possible
                
                **Facts:**
                - List one fact per line
                - Include numbers, dates, and specific details
                - Ensure facts are accurate and verifiable
                
                **Quotes:**
                - Use JSON format for structured quotes
                - Include speaker name and title
                - Keep quotes concise and relevant
                
                **Styles:**
                - **News**: AP style, objective reporting
                - **Blog**: Engaging, conversational tone
                - **Social**: Short, shareable content
                - **Newsletter**: Personal, informative
                """)
        
        # Output section
        gr.Markdown("## Generated Content")
        
        with gr.Row():
            article_output = gr.Textbox(
                label="Generated Article",
                lines=20,
                show_copy_button=True
            )
        
        # Analysis results
        with gr.Row():
            with gr.Column():
                fact_check_output = gr.Textbox(
                    label="Fact Check Report",
                    lines=15,
                    show_copy_button=True
                )
            
            with gr.Column():
                quality_output = gr.Textbox(
                    label="Quality Analysis",
                    lines=15,
                    show_copy_button=True
                )
        
        style_output = gr.Textbox(
            label="Style Compliance Report",
            lines=10,
            show_copy_button=True
        )
        
        # Examples section
        gr.Markdown("## 📋 Example Topics")
        
        gr.Examples(
            examples=[
                [
                    "Tech Company Announces Breakthrough in Quantum Computing",
                    "Company achieved 99.9% quantum error correction\nNew system processes 1000x faster than current computers\nTechnology could revolutionize cryptography and drug discovery\nResearch funded by $50 million government grant",
                    '[{"quote": "This represents a fundamental leap in quantum technology", "speaker": "Dr. Sarah Chen", "title": "Chief Scientist"}]',
                    "news",
                    500,
                    "San Francisco",
                    "Technology",
                    True,
                    True,
                    True
                ],
                [
                    "Local School District Implements AI-Powered Learning Platform",
                    "Platform personalized to each student's learning pace\n15,000 students will use the system this semester\nInitial test scores improved by 23% on average\nTeachers received 40 hours of training on the platform",
                    '[{"quote": "Our students are more engaged than ever before", "speaker": "Jennifer Walsh", "title": "Principal"}]',
                    "blog",
                    400,
                    "Springfield",
                    "Education",
                    True,
                    True,
                    True
                ]
            ],
            inputs=[headline, facts, quotes, style, target_length, location, category, 
                   enable_fact_check, enable_quality_check, enable_style_check]
        )
        
        # Event handlers
        generate_btn.click(
            fn=generate_article_interface,
            inputs=[headline, facts, quotes, style, target_length, location, category,
                   enable_fact_check, enable_quality_check, enable_style_check],
            outputs=[article_output, fact_check_output, quality_output, style_output]
        )
        
        sample_btn.click(
            fn=generate_sample_article,
            outputs=[headline, facts, quotes, location, category, style]
        )
        
        clear_btn.click(
            fn=lambda: ("", "", "", "", "General", "news", 500, "", "", ""),
            outputs=[headline, facts, quotes, location, category, style, target_length,
                    article_output, fact_check_output, quality_output]
        )
        
        # Footer
        gr.Markdown("""
        ---
        **Hugging Face News Article Generator** | Powered by state-of-the-art language models
        
        Built with ❤️ using Gradio and Hugging Face Transformers
        """)
    
    return interface

def main():
    """Launch the Gradio interface."""
    interface = create_gradio_interface()
    
    # Launch with custom settings
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()
