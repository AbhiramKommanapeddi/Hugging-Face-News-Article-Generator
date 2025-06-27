#!/usr/bin/env python3
"""
Main CLI application for the Hugging Face News Article Generator.
"""

import argparse
import sys
import os
import json
from datetime import datetime
from typing import List, Dict

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.news_generator import NewsGenerator
from src.style_manager import StyleManager
from src.fact_checker import FactChecker
from src.quality_metrics import QualityMetrics
from src.utils import (
    setup_logging, load_sample_topics,
    create_style_guide_templates, validate_article_data,
    create_article_summary
)

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Generate professional news articles using Hugging Face models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --headline "Tech Company Launches New Product" --facts "fact1,fact2,fact3"
  python main.py --sample --count 5 --style blog
  python main.py --generate-samples --output-dir my_articles
        """
    )
    
    # Article generation options
    parser.add_argument('--headline', type=str, help='Article headline')
    parser.add_argument('--facts', type=str, help='Comma-separated list of facts')
    parser.add_argument('--quotes', type=str, help='JSON string of quotes with attribution')
    parser.add_argument('--style', choices=['news', 'blog', 'social', 'newsletter'], 
                       default='news', help='Article style format')
    parser.add_argument('--length', type=int, default=500, help='Target word count')
    
    # Sample generation options
    parser.add_argument('--sample', action='store_true', 
                       help='Generate article from sample topics')
    parser.add_argument('--generate-samples', action='store_true',
                       help='Generate multiple sample articles')
    parser.add_argument('--count', type=int, default=1, 
                       help='Number of articles to generate')
    
    # Output options
    parser.add_argument('--output-dir', type=str, default='sample_articles',
                       help='Output directory for generated articles')
    parser.add_argument('--save', action='store_true', default=True,
                       help='Save articles to files')
    parser.add_argument('--print-only', action='store_true',
                       help='Only print to console, don\'t save files')
    
    # Analysis options
    parser.add_argument('--fact-check', action='store_true', default=True,
                       help='Perform fact checking analysis')
    parser.add_argument('--quality-check', action='store_true', default=True,
                       help='Perform quality analysis')
    parser.add_argument('--style-check', action='store_true', default=True,
                       help='Check style compliance')
    
    # Utility options
    parser.add_argument('--create-templates', action='store_true',
                       help='Create style guide templates')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Logging level')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    try:
        if args.create_templates:
            create_templates(args.output_dir)
            return
        
        if args.generate_samples:
            generate_sample_articles(args)
            return
        
        if args.sample:
            generate_from_sample(args)
            return
        
        if args.headline:
            generate_custom_article(args)
            return
        
        print("No generation option specified. Use --help for usage information.")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def generate_custom_article(args):
    """Generate article from custom input."""
    print(f"Generating article: {args.headline}")
    print("-" * 50)
    
    # Parse facts
    facts = []
    if args.facts:
        facts = [fact.strip() for fact in args.facts.split(',')]
    
    # Parse quotes
    quotes = []
    if args.quotes:
        try:
            quotes = json.loads(args.quotes)
        except json.JSONDecodeError:
            print("Warning: Invalid quotes JSON format. Ignoring quotes.")
    
    # Initialize generators
    news_gen = NewsGenerator()
    style_mgr = StyleManager()
    fact_checker = FactChecker()
    quality_checker = QualityMetrics()
    
    # Generate article
    article_data = news_gen.generate_article(
        headline=args.headline,
        facts=facts,
        quotes=quotes,
        style=args.style,
        target_length=args.length
    )
    
    # Perform analysis
    if args.fact_check:
        print("Performing fact check...")
        article_data['fact_check'] = fact_checker.verify_facts(
            article_data['full_article'], facts
        )
    
    if args.quality_check:
        print("Performing quality analysis...")
        article_data['quality_evaluation'] = quality_checker.evaluate_article(article_data)
    
    if args.style_check:
        print("Checking style compliance...")
        article_data['style_compliance'] = style_mgr.validate_style_compliance(
            article_data['full_article'], args.style
        )
    
    # Output results
    display_article(article_data, args.style)
    
    if not args.print_only:
        # Save article
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_headline = "".join(c if c.isalnum() or c in ' -_' else '' for c in article_data['headline'])
        safe_headline = safe_headline.replace(' ', '_').lower()[:50]
        filename = f"{safe_headline}_{timestamp}.json"
        filepath = os.path.join(args.output_dir, filename)
        
        os.makedirs(args.output_dir, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, indent=2, ensure_ascii=False, default=str)
        
        if filepath:
            print(f"\nArticle saved to: {filepath}")

def generate_from_sample(args):
    """Generate article from sample topics."""
    sample_topics = load_sample_topics()
    
    if args.count > len(sample_topics):
        print(f"Warning: Only {len(sample_topics)} sample topics available. Generating {len(sample_topics)} articles.")
        args.count = len(sample_topics)
    
    # Select random topics
    import random
    selected_topics = random.sample(sample_topics, args.count)
    
    for i, topic in enumerate(selected_topics, 1):
        print(f"\nGenerating article {i}/{args.count}: {topic['headline']}")
        print("-" * 60)
        
        # Update args for this topic
        args.headline = topic['headline']
        args.facts = ','.join(topic['facts'])
        args.quotes = json.dumps(topic['quotes'])
        
        generate_custom_article(args)

def generate_sample_articles(args):
    """Generate all sample articles for demonstration."""
    print("Generating complete sample article collection...")
    print("=" * 60)
    
    sample_topics = load_sample_topics()
    
    # Initialize generators
    news_gen = NewsGenerator()
    style_mgr = StyleManager()
    fact_checker = FactChecker()
    quality_checker = QualityMetrics()
    
    # Generate articles in different styles
    styles = ['news', 'blog', 'social', 'newsletter']
    articles_generated = 0
    
    for style in styles:
        print(f"\nGenerating {style.upper()} format articles...")
        
        # Select topics for this style (4 articles per style)
        topics_for_style = sample_topics[articles_generated:articles_generated + 4]
        
        for topic in topics_for_style:
            try:
                print(f"  Generating: {topic['headline']}")
                
                # Generate article
                article_data = news_gen.generate_article(
                    headline=topic['headline'],
                    facts=topic['facts'],
                    quotes=topic.get('quotes', []),
                    style=style,
                    target_length=args.length
                )
                
                # Add topic metadata
                article_data['topic_category'] = topic.get('category', 'General')
                article_data['location'] = topic.get('location', 'Unknown')
                
                # Perform analysis
                if args.fact_check:
                    article_data['fact_check'] = fact_checker.verify_facts(
                        article_data['full_article'], topic['facts']
                    )
                
                if args.quality_check:
                    article_data['quality_evaluation'] = quality_checker.evaluate_article(article_data)
                
                if args.style_check:
                    article_data['style_compliance'] = style_mgr.validate_style_compliance(
                        article_data['full_article'], style
                    )
                
                # Save article
                if not args.print_only:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_headline = "".join(c if c.isalnum() or c in ' -_' else '' for c in topic['headline'])
                    safe_headline = safe_headline.replace(' ', '_').lower()[:50]
                    filename = f"{safe_headline}_{timestamp}.json"
                    style_dir = os.path.join(args.output_dir, style)
                    os.makedirs(style_dir, exist_ok=True)
                    filepath = os.path.join(style_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(article_data, f, indent=2, ensure_ascii=False, default=str)
                
                articles_generated += 1
                
            except Exception as e:
                print(f"    Error generating article: {e}")
                continue
    
    print(f"\nGenerated {articles_generated} sample articles")
    if not args.print_only:
        print(f"Articles saved to: {args.output_dir}")

def create_templates(output_dir: str):
    """Create style guide templates."""
    print("Creating style guide templates...")
    
    templates_dir = os.path.join(output_dir, 'style_guides')
    os.makedirs(templates_dir, exist_ok=True)
    
    templates = create_style_guide_templates()
    
    for template_name, content in templates.items():
        filename = f"{template_name}.txt"
        filepath = os.path.join(templates_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Created: {filepath}")
    
    print(f"\nStyle guide templates created in: {templates_dir}")

def display_article(article_data: Dict, style: str):
    """Display article in formatted output."""
    print("\n" + "=" * 80)
    print(f"GENERATED ARTICLE ({style.upper()} FORMAT)")
    print("=" * 80)
    
    print(f"\nHEADLINE: {article_data['headline']}")
    print(f"WORD COUNT: {article_data['word_count']}")
    print(f"TIMESTAMP: {article_data['timestamp']}")
    
    print("\nARTICLE CONTENT:")
    print("-" * 40)
    print(article_data['full_article'])
    
    # Display analysis results
    if 'fact_check' in article_data:
        print("\nFACT CHECK RESULTS:")
        print("-" * 20)
        fc = article_data['fact_check']
        print(f"Overall Score: {fc['overall_score']}/100")
        print(f"Objectivity: {fc['objectivity_score']}/100")
        print(f"Source Attribution: {fc['source_attribution_score']}/100")
        
        if fc.get('recommendations'):
            print("Recommendations:")
            for rec in fc['recommendations'][:3]:  # Show top 3
                print(f"  • {rec}")
    
    if 'quality_evaluation' in article_data:
        print("\nQUALITY EVALUATION:")
        print("-" * 20)
        qe = article_data['quality_evaluation']
        print(f"Overall Score: {qe['overall_score']}/100")
        print(f"Professional Rating: {qe['professional_rating']}")
        
        if qe.get('strengths'):
            print("Strengths:")
            for strength in qe['strengths'][:3]:  # Show top 3
                print(f"  ✓ {strength}")
    
    if 'style_compliance' in article_data:
        print("\nSTYLE COMPLIANCE:")
        print("-" * 20)
        sc = article_data['style_compliance']
        print(f"Compliance Score: {sc['score']}/100")
        if sc.get('issues'):
            print("Issues:")
            for issue in sc['issues'][:3]:  # Show top 3
                print(f"  ! {issue}")

def display_help():
    """Display extended help information."""
    help_text = """
HUGGING FACE NEWS ARTICLE GENERATOR
==================================

This tool generates professional news articles using state-of-the-art 
Hugging Face language models. It includes fact-checking, quality analysis,
and multiple output formats.

QUICK START:
1. Generate a custom article:
   python main.py --headline "Your headline" --facts "fact1,fact2,fact3"

2. Generate sample articles:
   python main.py --generate-samples

3. Create style guides:
   python main.py --create-templates

FEATURES:
- Professional news writing with inverted pyramid structure
- Multiple output formats (news, blog, social media, newsletter)
- Automatic fact-checking and source attribution
- Quality metrics and readability analysis
- Style compliance checking
- Batch generation of sample articles

For more information, see README.md or use --help flag.
    """
    print(help_text)

if __name__ == "__main__":
    main()
