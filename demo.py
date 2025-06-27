#!/usr/bin/env python3
"""
Demonstration script for the Hugging Face News Article Generator.
Generates sample articles to showcase all features and capabilities.
"""

import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.news_generator import NewsGenerator
from src.style_manager import StyleManager
from src.fact_checker import FactChecker
from src.quality_metrics import QualityMetrics
from src.utils import (
    load_sample_topics, save_article_to_file, 
    create_article_summary, setup_logging
)

def main():
    """Run comprehensive demonstration."""
    print("🚀 HUGGING FACE NEWS ARTICLE GENERATOR DEMO")
    print("=" * 60)
    
    # Setup logging
    setup_logging("INFO")
    
    # Initialize all components
    print("📡 Initializing AI models and components...")
    news_gen = NewsGenerator()
    style_mgr = StyleManager()
    fact_checker = FactChecker()
    quality_checker = QualityMetrics()
    print("✅ All components initialized successfully!")
    
    # Load sample topics
    sample_topics = load_sample_topics()
    print(f"📋 Loaded {len(sample_topics)} sample topics")
    
    # Demonstrate different styles
    styles = ['news', 'blog', 'social', 'newsletter']
    demo_results = []
    
    for i, style in enumerate(styles):
        print(f"\n🎨 DEMONSTRATING {style.upper()} STYLE")
        print("-" * 40)
        
        # Select a topic for this style
        topic = sample_topics[i % len(sample_topics)]
        print(f"Topic: {topic['headline']}")
        
        try:
            # Generate article
            print(f"🔄 Generating {style} article...")
            article_data = news_gen.generate_article(
                headline=topic['headline'],
                facts=topic['facts'],
                quotes=topic.get('quotes', []),
                style=style,
                target_length=500
            )
            
            # Add metadata
            article_data['topic_category'] = topic.get('category', 'General')
            article_data['location'] = topic.get('location', 'Unknown')
            
            # Perform comprehensive analysis
            print("🔍 Performing fact checking...")
            article_data['fact_check'] = fact_checker.verify_facts(
                article_data['full_article'], topic['facts']
            )
            
            print("📊 Analyzing article quality...")
            article_data['quality_evaluation'] = quality_checker.evaluate_article(article_data)
            
            print("✏️  Checking style compliance...")
            article_data['style_compliance'] = style_mgr.validate_style_compliance(
                article_data['full_article'], style
            )
            
            # Display results
            display_demo_results(article_data, style)
            
            # Save article
            output_dir = os.path.join('sample_articles', style)
            filepath = save_article_to_file(article_data, output_dir)
            print(f"💾 Article saved to: {filepath}")
            
            demo_results.append(article_data)
            
        except Exception as e:
            print(f"❌ Error generating {style} article: {e}")
            continue
    
    # Generate comprehensive report
    print(f"\n📈 GENERATING COMPREHENSIVE DEMO REPORT")
    print("=" * 50)
    generate_demo_report(demo_results)
    
    # Create style guides
    print(f"\n📚 CREATING STYLE GUIDE TEMPLATES")
    print("=" * 40)
    create_style_guide_files()
    
    print(f"\n🎉 DEMO COMPLETED SUCCESSFULLY!")
    print(f"📁 Check the 'sample_articles' directory for generated content")
    print(f"📖 Check the 'style_guides' directory for writing templates")
    print(f"📊 Check 'demo_report.json' for comprehensive analysis")

def display_demo_results(article_data, style):
    """Display demonstration results for an article."""
    print(f"\n📰 ARTICLE PREVIEW ({style.upper()}):")
    print("-" * 30)
    
    # Basic metrics
    print(f"Word Count: {article_data['word_count']}")
    print(f"Category: {article_data.get('topic_category', 'N/A')}")
    print(f"Location: {article_data.get('location', 'N/A')}")
    
    # Analysis scores
    if 'fact_check' in article_data:
        fc_score = article_data['fact_check']['overall_score']
        print(f"Fact Check Score: {fc_score}/100")
    
    if 'quality_evaluation' in article_data:
        quality_score = article_data['quality_evaluation']['overall_score']
        print(f"Quality Score: {quality_score}/100")
        print(f"Professional Rating: {article_data['quality_evaluation']['professional_rating']}")
    
    if 'style_compliance' in article_data:
        style_score = article_data['style_compliance']['score']
        print(f"Style Compliance: {style_score}/100")
    
    # Article preview
    preview = article_data['full_article'][:200] + "..." if len(article_data['full_article']) > 200 else article_data['full_article']
    print(f"\nPreview:\n{preview}")

def generate_demo_report(demo_results):
    """Generate comprehensive demonstration report."""
    
    report = {
        'demo_timestamp': datetime.now().isoformat(),
        'total_articles_generated': len(demo_results),
        'styles_demonstrated': [],
        'overall_metrics': {},
        'articles_summary': [],
        'performance_analysis': {}
    }
    
    # Calculate overall metrics
    total_words = sum(article['word_count'] for article in demo_results)
    avg_word_count = total_words / len(demo_results) if demo_results else 0
    
    fact_check_scores = [article.get('fact_check', {}).get('overall_score', 0) for article in demo_results]
    quality_scores = [article.get('quality_evaluation', {}).get('overall_score', 0) for article in demo_results]
    style_scores = [article.get('style_compliance', {}).get('score', 0) for article in demo_results]
    
    report['overall_metrics'] = {
        'total_word_count': total_words,
        'average_word_count': round(avg_word_count, 1),
        'average_fact_check_score': round(sum(fact_check_scores) / len(fact_check_scores), 1) if fact_check_scores else 0,
        'average_quality_score': round(sum(quality_scores) / len(quality_scores), 1) if quality_scores else 0,
        'average_style_score': round(sum(style_scores) / len(style_scores), 1) if style_scores else 0
    }
    
    # Article summaries
    for i, article in enumerate(demo_results):
        summary = {
            'index': i + 1,
            'headline': article['headline'],
            'style': article.get('style', 'unknown'),
            'category': article.get('topic_category', 'General'),
            'word_count': article['word_count'],
            'fact_check_score': article.get('fact_check', {}).get('overall_score', 0),
            'quality_score': article.get('quality_evaluation', {}).get('overall_score', 0),
            'style_compliance_score': article.get('style_compliance', {}).get('score', 0)
        }
        report['articles_summary'].append(summary)
    
    # Performance analysis
    report['performance_analysis'] = {
        'highest_quality_article': max(demo_results, key=lambda x: x.get('quality_evaluation', {}).get('overall_score', 0))['headline'] if demo_results else None,
        'most_fact_compliant': max(demo_results, key=lambda x: x.get('fact_check', {}).get('overall_score', 0))['headline'] if demo_results else None,
        'best_style_compliance': max(demo_results, key=lambda x: x.get('style_compliance', {}).get('score', 0))['headline'] if demo_results else None
    }
    
    # Save report
    with open('demo_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    # Display summary
    print(f"📊 DEMO STATISTICS:")
    print(f"   Articles Generated: {report['total_articles_generated']}")
    print(f"   Total Words: {report['overall_metrics']['total_word_count']:,}")
    print(f"   Average Quality Score: {report['overall_metrics']['average_quality_score']}/100")
    print(f"   Average Fact Check Score: {report['overall_metrics']['average_fact_check_score']}/100")
    print(f"   Average Style Compliance: {report['overall_metrics']['average_style_score']}/100")

def create_style_guide_files():
    """Create style guide template files."""
    from src.utils import create_style_guide_templates
    
    templates = create_style_guide_templates()
    
    for template_name, content in templates.items():
        filename = f"{template_name}.txt"
        filepath = os.path.join('style_guides', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📄 Created: {filepath}")

def demonstrate_advanced_features():
    """Demonstrate advanced features like multi-format generation."""
    print(f"\n🔬 ADVANCED FEATURES DEMONSTRATION")
    print("=" * 40)
    
    # Initialize components
    news_gen = NewsGenerator()
    style_mgr = StyleManager()
    
    # Select a topic
    sample_topics = load_sample_topics()
    topic = sample_topics[0]
    
    print(f"📰 Generating multi-format article for: {topic['headline']}")
    
    # Generate base article
    base_article = news_gen.generate_article(
        headline=topic['headline'],
        facts=topic['facts'],
        quotes=topic.get('quotes', []),
        style='news'
    )
    
    # Generate different format versions
    formats = {
        'news_wire': style_mgr.format_news_wire,
        'blog': style_mgr.format_blog_style,
        'newsletter': style_mgr.format_newsletter
    }
    
    for format_name, format_func in formats.items():
        try:
            formatted_article = format_func(base_article)
            
            # Save formatted version
            output_file = f"sample_articles/advanced_{format_name}_demo.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_article)
            
            print(f"✅ Created {format_name} format: {output_file}")
            
        except Exception as e:
            print(f"❌ Error creating {format_name} format: {e}")

if __name__ == "__main__":
    try:
        main()
        demonstrate_advanced_features()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
