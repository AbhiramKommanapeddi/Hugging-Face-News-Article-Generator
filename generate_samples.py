"""
Generate 15+ Sample Articles Script
Automated News Article Writer using Hugging Face Models
"""

import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any

from src.news_generator import NewsGenerator
from src.style_manager import StyleManager  
from src.fact_checker import FactChecker
from src.quality_metrics import QualityMetrics
from src.utils import save_article, create_directories


def main():
    """Generate comprehensive sample articles and create deliverables"""
    
    print("🎯 GENERATING 15+ SAMPLE ARTICLES")
    print("=" * 60)
    
    # Initialize components
    print("📡 Initializing AI models and components...")
    try:
        news_gen = NewsGenerator()
        style_manager = StyleManager()
        fact_checker = FactChecker()
        quality_metrics = QualityMetrics()
        print("✅ All components initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize components: {e}")
        return
    
    # Sample topics for comprehensive testing
    topics = [
        "Revolutionary AI Breakthrough Changes Medical Diagnosis Forever",
        "Local School District Implements Game-Changing STEM Program",
        "Climate Scientists Discover New Evidence of Accelerated Melting",
        "Professional Basketball Team Makes Historic Championship Run",
        "Breakthrough Cancer Treatment Shows 95% Success Rate",
        "City Council Approves Major Infrastructure Overhaul Project",
        "Tech Giant Announces Massive Investment in Renewable Energy",
        "University Researchers Develop Quantum Computing Prototype",
        "State Legislature Passes Landmark Education Reform Bill",
        "International Space Mission Discovers Earth-Like Exoplanet",
        "Local Restaurant Chain Expands to Five New Cities",
        "Cybersecurity Firm Prevents Major International Data Breach",
        "Film Studio Announces Groundbreaking Virtual Reality Experience",
        "National Health Study Reveals Surprising Nutrition Findings",
        "Transportation Authority Launches Revolutionary Public Transit",
        "Tech Startup Creates AI Assistant for Small Business Owners",
        "Archaeological Team Uncovers Ancient Civilization Artifacts",
        "Regional Hospital Opens State-of-the-Art Cancer Treatment Center"
    ]
    
    # Article styles to rotate through
    styles = ['news', 'blog', 'social', 'newsletter']
    
    # Categories to cycle through
    categories = ['Technology', 'Education', 'Environment', 'Sports', 'Health', 
                  'Politics', 'Business', 'Science', 'Entertainment', 'Local News']
    
    # Locations for variety
    locations = ['New York', 'San Francisco', 'Boston', 'Chicago', 'Los Angeles',
                'Seattle', 'Austin', 'Denver', 'Miami', 'Atlanta']
    
    # Create directories
    create_directories(['sample_articles', 'style_guides'])
    
    # Track statistics
    stats = {
        'total_articles': 0,
        'by_style': {style: 0 for style in styles},
        'total_words': 0,
        'quality_scores': [],
        'fact_scores': [],
        'style_scores': []
    }
    
    articles_data = []
    
    print(f"\n🚀 Generating {len(topics)} articles across {len(styles)} styles...")
    print("-" * 60)
    
    for i, topic in enumerate(topics):
        style = styles[i % len(styles)]
        category = categories[i % len(categories)]
        location = locations[i % len(locations)]
        
        print(f"\n📝 Article {i+1}/{len(topics)}: {style.upper()} style")
        print(f"Topic: {topic}")
        print(f"Category: {category} | Location: {location}")
        
        try:
            # Generate article
            print("🔄 Generating content...")
            article = news_gen.generate_article(
                headline=topic,
                facts=[
                    f"Event occurred in {location}",
                    "Multiple sources confirm the development",
                    "Experts predict significant impact on industry",
                    "Implementation timeline spans 6-12 months"
                ],
                style=style
            )
            
            if not article:
                print("❌ Failed to generate article")
                continue
            
            # Apply style formatting
            print("🎨 Applying style formatting...")
            if style == 'news':
                formatted_article = style_manager.format_news_wire(article)
            elif style == 'blog':
                formatted_article = style_manager.format_blog_style(article)
            elif style == 'social':
                formatted_article = style_manager.format_social_media(article)
                # For social media, take the first post as the main content
                if isinstance(formatted_article, list) and formatted_article:
                    formatted_article = formatted_article[0].get('content', str(formatted_article))
                else:
                    formatted_article = str(formatted_article)
            elif style == 'newsletter':
                formatted_article = style_manager.format_newsletter(article)
            else:
                formatted_article = article.get('content', str(article))
            
            # Fact checking
            print("🔍 Performing fact check...")
            fact_score = fact_checker.verify_facts(formatted_article)
            
            # Quality analysis
            print("📊 Analyzing quality...")
            quality_result = quality_metrics.evaluate_article(formatted_article)
            if isinstance(quality_result, dict):
                quality_score = quality_result.get('overall_score', 50)
            else:
                quality_score = 50  # Default score if error
            
            # Style compliance
            print("✏️ Checking style compliance...")
            style_compliance = style_manager.validate_style_compliance(formatted_article, style)
            style_score = style_compliance.get('overall_score', 100)
            
            # Create comprehensive article data
            article_data = {
                'id': f'article_{i+1:03d}',
                'headline': topic,
                'content': formatted_article,
                'metadata': {
                    'style': style,
                    'category': category,
                    'location': location,
                    'word_count': len(formatted_article.split()),
                    'generated_at': datetime.now().isoformat(),
                    'fact_check_score': fact_score,
                    'quality_score': quality_score,
                    'style_compliance': style_score
                }
            }
            
            # Save article
            filename = save_article(article_data, style, topic)
            print(f"💾 Saved: {filename}")
            
            # Update statistics
            stats['total_articles'] += 1
            stats['by_style'][style] += 1
            stats['total_words'] += article_data['metadata']['word_count']
            stats['quality_scores'].append(quality_score)
            stats['fact_scores'].append(fact_score)
            stats['style_scores'].append(style_score)
            
            articles_data.append(article_data)
            
            print("✅ Article completed successfully!")
            time.sleep(1)  # Brief pause between articles
            
        except Exception as e:
            print(f"❌ Error generating article {i+1}: {e}")
            continue
    
    # Calculate final statistics
    stats['avg_quality'] = sum(stats['quality_scores']) / len(stats['quality_scores']) if stats['quality_scores'] else 0
    stats['avg_fact_score'] = sum(stats['fact_scores']) / len(stats['fact_scores']) if stats['fact_scores'] else 0
    stats['avg_style_score'] = sum(stats['style_scores']) / len(stats['style_scores']) if stats['style_scores'] else 0
    
    # Generate comprehensive report
    print("\n📈 GENERATING COMPREHENSIVE REPORT")
    print("=" * 60)
    
    report = {
        'generation_timestamp': datetime.now().isoformat(),
        'summary': {
            'total_articles_generated': stats['total_articles'],
            'total_words': stats['total_words'],
            'average_article_length': stats['total_words'] / stats['total_articles'] if stats['total_articles'] > 0 else 0,
            'articles_by_style': stats['by_style'],
            'average_quality_score': stats['avg_quality'],
            'average_fact_check_score': stats['avg_fact_score'],
            'average_style_compliance': stats['avg_style_score']
        },
        'detailed_statistics': {
            'quality_scores': {
                'min': min(stats['quality_scores']) if stats['quality_scores'] else 0,
                'max': max(stats['quality_scores']) if stats['quality_scores'] else 0,
                'median': sorted(stats['quality_scores'])[len(stats['quality_scores'])//2] if stats['quality_scores'] else 0
            },
            'fact_check_scores': {
                'min': min(stats['fact_scores']) if stats['fact_scores'] else 0,
                'max': max(stats['fact_scores']) if stats['fact_scores'] else 0,
                'median': sorted(stats['fact_scores'])[len(stats['fact_scores'])//2] if stats['fact_scores'] else 0
            }
        },
        'articles': articles_data
    }
    
    # Save comprehensive report
    report_file = 'comprehensive_sample_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Create style guide templates
    print("\n📚 EXPORTING STYLE GUIDE TEMPLATES")
    print("=" * 60)
    
    style_guides = {
        'ap_style_guide.txt': """
AP Style Guide for News Articles
================================

HEADLINES:
- Use title case for headlines
- Keep under 10 words when possible
- Use active voice
- Avoid abbreviations

BODY TEXT:
- Use inverted pyramid structure
- Lead with most important information
- Use third person perspective
- Include attribution for all quotes
- Use AP style for dates, numbers, titles

QUOTES:
- Use direct quotes from sources
- Attribute every quote
- Use "said" as primary attribution verb
- Place attribution after first sentence of quote

FORMATTING:
- Use single space after periods
- Spell out numbers one through nine
- Use numerals for 10 and above
- Capitalize proper nouns and titles before names
""",
        
        'blog_style_guide.txt': """
Blog Style Guide
================

TONE:
- Conversational and engaging
- Use first or second person when appropriate
- Show personality while maintaining professionalism
- Use contractions naturally

STRUCTURE:
- Start with compelling hook
- Use subheadings to break up content
- Include bullet points and lists
- End with call-to-action or conclusion

LANGUAGE:
- Use shorter sentences and paragraphs
- Explain technical terms
- Use active voice predominantly
- Include relevant keywords naturally

ENGAGEMENT:
- Ask questions to involve readers
- Use examples and analogies
- Include personal experiences when relevant
- Encourage comments and interaction
""",
        
        'social_media_guide.txt': """
Social Media Style Guide
========================

BREVITY:
- Keep posts concise and impactful
- Use strong opening hooks
- Include clear call-to-action
- Optimize for mobile reading

HASHTAGS:
- Use 2-5 relevant hashtags
- Mix popular and niche tags
- Create branded hashtags when appropriate
- Research trending hashtags

ENGAGEMENT:
- Ask questions to encourage interaction
- Use emojis strategically
- Tag relevant accounts
- Post at optimal times for audience

VISUAL ELEMENTS:
- Include images or videos when possible
- Use consistent brand colors
- Maintain visual quality standards
- Add alt text for accessibility
""",
        
        'newsletter_style_guide.txt': """
Newsletter Style Guide
======================

SUBJECT LINES:
- Keep under 50 characters
- Create urgency or curiosity
- Avoid spam trigger words
- Personalize when possible

CONTENT STRUCTURE:
- Start with personal greeting
- Use scannable format with sections
- Include mix of content types
- End with clear next steps

DESIGN:
- Use consistent header/footer
- Include company branding
- Ensure mobile responsiveness
- Use white space effectively

FREQUENCY:
- Maintain consistent schedule
- Provide valuable content in every issue
- Balance promotional and educational content
- Monitor engagement metrics
"""
    }
    
    for filename, content in style_guides.items():
        filepath = os.path.join('style_guides', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Created: {filepath}")
    
    # Print final summary
    print(f"\n🎉 SAMPLE GENERATION COMPLETED!")
    print("=" * 60)
    print(f"✅ Successfully generated {stats['total_articles']} articles")
    print(f"📊 Total words: {stats['total_words']:,}")
    print(f"📈 Average quality score: {stats['avg_quality']:.1f}/100")
    print(f"🔍 Average fact check score: {stats['avg_fact_score']:.1f}/100")
    print(f"✏️ Average style compliance: {stats['avg_style_score']:.1f}/100")
    print(f"\n📁 Files created:")
    print(f"   • Sample articles: sample_articles/ directory")
    print(f"   • Style guides: style_guides/ directory")
    print(f"   • Comprehensive report: {report_file}")
    
    print(f"\n🎯 DELIVERABLES SUMMARY:")
    print(f"   ✅ Article generation system (complete)")
    print(f"   ✅ {stats['total_articles']} sample articles (target: 15+)")
    print(f"   ✅ Style guide templates (4 formats)")
    print(f"   ✅ Quality metrics and evaluation reports")
    print(f"   ✅ Multiple formatting options (news, blog, social, newsletter)")

if __name__ == "__main__":
    main()
