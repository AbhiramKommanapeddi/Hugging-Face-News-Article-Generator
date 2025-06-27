#!/usr/bin/env python3
"""
Streamlit web interface for the Hugging Face News Article Generator.
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime
import plotly.express as px
import pandas as pd

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.news_generator import NewsGenerator
from src.style_manager import StyleManager
from src.fact_checker import FactChecker
from src.quality_metrics import QualityMetrics
from src.utils import (
    load_sample_topics, save_article_to_file, 
    create_article_summary, validate_article_data
)

# Configure Streamlit page
st.set_page_config(
    page_title="News Article Generator",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'generated_articles' not in st.session_state:
    st.session_state.generated_articles = []

def main():
    """Main Streamlit application."""
    st.title("📰 Hugging Face News Article Generator")
    st.markdown("Generate professional news articles using state-of-the-art AI models")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Article Generator", "Sample Articles", "Analytics Dashboard", "Style Guides"]
    )
    
    if page == "Article Generator":
        article_generator_page()
    elif page == "Sample Articles":
        sample_articles_page()
    elif page == "Analytics Dashboard":
        analytics_dashboard_page()
    elif page == "Style Guides":
        style_guides_page()

def article_generator_page():
    """Article generation interface."""
    st.header("Generate News Article")
    
    # Article input form
    with st.form("article_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            headline = st.text_input(
                "Article Headline",
                placeholder="Enter your news headline here..."
            )
            
            facts = st.text_area(
                "Key Facts (one per line)",
                placeholder="Enter key facts, one per line...",
                height=150
            )
            
            quotes_input = st.text_area(
                "Quotes (JSON format)",
                placeholder='[{"quote": "Quote text", "speaker": "Speaker Name", "title": "Speaker Title"}]',
                height=100
            )
        
        with col2:
            style = st.selectbox(
                "Article Style",
                ["news", "blog", "social", "newsletter"]
            )
            
            target_length = st.slider(
                "Target Word Count",
                min_value=200,
                max_value=1500,
                value=500,
                step=50
            )
            
            location = st.text_input(
                "Location",
                placeholder="City, State"
            )
            
            category = st.selectbox(
                "Category",
                ["Technology", "Business", "Sports", "Health", "Politics", 
                 "Environment", "Education", "Entertainment", "Science", "General"]
            )
        
        # Analysis options
        st.subheader("Analysis Options")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            fact_check = st.checkbox("Fact Checking", value=True)
        with col4:
            quality_check = st.checkbox("Quality Analysis", value=True)
        with col5:
            style_check = st.checkbox("Style Compliance", value=True)
        
        submit_button = st.form_submit_button("Generate Article")
    
    if submit_button and headline:
        generate_article(
            headline, facts, quotes_input, style, target_length,
            location, category, fact_check, quality_check, style_check
        )
    elif submit_button:
        st.error("Please enter a headline to generate an article.")

def generate_article(headline, facts, quotes_input, style, target_length,
                    location, category, fact_check, quality_check, style_check):
    """Generate article with user inputs."""
    
    with st.spinner("Generating article..."):
        try:
            # Parse inputs
            facts_list = [fact.strip() for fact in facts.split('\n') if fact.strip()]
            
            quotes_list = []
            if quotes_input.strip():
                try:
                    quotes_list = json.loads(quotes_input)
                except json.JSONDecodeError:
                    st.warning("Invalid quotes JSON format. Proceeding without quotes.")
            
            # Initialize generators
            news_gen = NewsGenerator()
            style_mgr = StyleManager()
            fact_checker = FactChecker()
            quality_checker = QualityMetrics()
            
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
            
            # Perform analysis
            if fact_check:
                with st.spinner("Performing fact check..."):
                    article_data['fact_check'] = fact_checker.verify_facts(
                        article_data['full_article'], facts_list
                    )
            
            if quality_check:
                with st.spinner("Analyzing quality..."):
                    article_data['quality_evaluation'] = quality_checker.evaluate_article(article_data)
            
            if style_check:
                with st.spinner("Checking style compliance..."):
                    article_data['style_compliance'] = style_mgr.validate_style_compliance(
                        article_data['full_article'], style
                    )
            
            # Display results
            display_article_results(article_data)
            
            # Save to session state
            st.session_state.generated_articles.append(article_data)
            
        except Exception as e:
            st.error(f"Error generating article: {str(e)}")

def display_article_results(article_data):
    """Display generated article and analysis results."""
    
    # Article content
    st.subheader("Generated Article")
    
    # Article metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Word Count", article_data['word_count'])
    with col2:
        if 'quality_evaluation' in article_data:
            st.metric("Quality Score", f"{article_data['quality_evaluation']['overall_score']}/100")
    with col3:
        if 'fact_check' in article_data:
            st.metric("Fact Check Score", f"{article_data['fact_check']['overall_score']}/100")
    with col4:
        if 'style_compliance' in article_data:
            st.metric("Style Compliance", f"{article_data['style_compliance']['score']}/100")
    
    # Article text
    st.text_area(
        "Article Content",
        value=article_data['full_article'],
        height=400,
        disabled=True
    )
    
    # Analysis tabs
    if any(key in article_data for key in ['fact_check', 'quality_evaluation', 'style_compliance']):
        tabs = st.tabs(["Fact Check", "Quality Analysis", "Style Compliance"])
        
        if 'fact_check' in article_data:
            with tabs[0]:
                display_fact_check_results(article_data['fact_check'])
        
        if 'quality_evaluation' in article_data:
            with tabs[1]:
                display_quality_results(article_data['quality_evaluation'])
        
        if 'style_compliance' in article_data:
            with tabs[2]:
                display_style_results(article_data['style_compliance'])
    
    # Download options
    st.subheader("Download Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Save as JSON"):
            filepath = save_article_to_file(article_data)
            if filepath:
                st.success(f"Article saved to {filepath}")
    
    with col2:
        if st.button("Download Text"):
            st.download_button(
                label="Download Article Text",
                data=article_data['full_article'],
                file_name=f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("Download Analysis"):
            analysis_text = create_analysis_report(article_data)
            st.download_button(
                label="Download Full Report",
                data=analysis_text,
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

def display_fact_check_results(fact_check):
    """Display fact checking results."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fact Check Scores")
        scores = {
            'Overall': fact_check['overall_score'],
            'Objectivity': fact_check['objectivity_score'],
            'Source Attribution': fact_check['source_attribution_score'],
            'Fact Consistency': fact_check['fact_consistency_score'],
            'Credibility': fact_check['credibility_score']
        }
        
        for score_name, score_value in scores.items():
            st.metric(score_name, f"{score_value}/100")
    
    with col2:
        st.subheader("Recommendations")
        if fact_check.get('recommendations'):
            for rec in fact_check['recommendations']:
                st.write(f"• {rec}")
        else:
            st.write("No specific recommendations.")
    
    if fact_check.get('flagged_content'):
        st.subheader("Flagged Content")
        for item in fact_check['flagged_content']:
            st.warning(f"{item['type']}: {item['content']} (Severity: {item['severity']})")

def display_quality_results(quality_eval):
    """Display quality evaluation results."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quality Scores")
        category_scores = quality_eval['category_scores']
        for category, data in category_scores.items():
            score = data['score'] if isinstance(data, dict) else data
            st.metric(category.replace('_', ' ').title(), f"{score}/100")
    
    with col2:
        st.subheader("Professional Rating")
        st.info(quality_eval['professional_rating'])
        
        if quality_eval.get('strengths'):
            st.subheader("Strengths")
            for strength in quality_eval['strengths']:
                st.success(f"✓ {strength}")
    
    if quality_eval.get('areas_for_improvement'):
        st.subheader("Areas for Improvement")
        for improvement in quality_eval['areas_for_improvement']:
            st.warning(f"• {improvement}")

def display_style_results(style_compliance):
    """Display style compliance results."""
    st.subheader("Style Compliance Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Compliance Score", f"{style_compliance['score']}/100")
        st.write(f"**Style:** {style_compliance['style']}")
    
    with col2:
        if style_compliance.get('issues'):
            st.subheader("Issues Found")
            for issue in style_compliance['issues']:
                st.warning(f"• {issue}")
        
        if style_compliance.get('suggestions'):
            st.subheader("Suggestions")
            for suggestion in style_compliance['suggestions']:
                st.info(f"• {suggestion}")

def sample_articles_page():
    """Sample articles showcase page."""
    st.header("Sample Articles")
    st.markdown("Explore pre-generated articles demonstrating different styles and topics.")
    
    # Generate sample articles button
    if st.button("Generate New Sample Articles"):
        generate_sample_articles()
    
    # Display existing articles
    if st.session_state.generated_articles:
        st.subheader("Generated Articles")
        
        for i, article in enumerate(st.session_state.generated_articles):
            with st.expander(f"Article {i+1}: {article['headline'][:50]}..."):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Category:** {article.get('topic_category', 'N/A')}")
                    st.write(f"**Word Count:** {article['word_count']}")
                
                with col2:
                    if 'quality_evaluation' in article:
                        st.write(f"**Quality Score:** {article['quality_evaluation']['overall_score']}/100")
                    if 'fact_check' in article:
                        st.write(f"**Fact Check:** {article['fact_check']['overall_score']}/100")
                
                with col3:
                    st.write(f"**Generated:** {article['timestamp'][:10]}")
                
                st.text_area(
                    "Content",
                    value=article['full_article'][:500] + "..." if len(article['full_article']) > 500 else article['full_article'],
                    height=200,
                    disabled=True,
                    key=f"article_content_{i}"
                )
    else:
        st.info("No articles generated yet. Use the Article Generator to create some!")

def generate_sample_articles():
    """Generate sample articles from predefined topics."""
    with st.spinner("Generating sample articles..."):
        sample_topics = load_sample_topics()[:5]  # Generate first 5 samples
        
        news_gen = NewsGenerator()
        
        for topic in sample_topics:
            try:
                article_data = news_gen.generate_article(
                    headline=topic['headline'],
                    facts=topic['facts'],
                    quotes=topic.get('quotes', []),
                    style='news'
                )
                
                article_data['topic_category'] = topic.get('category', 'General')
                article_data['location'] = topic.get('location', 'Unknown')
                
                st.session_state.generated_articles.append(article_data)
                
            except Exception as e:
                st.error(f"Error generating sample for {topic['headline']}: {e}")
        
        st.success(f"Generated {len(sample_topics)} sample articles!")

def analytics_dashboard_page():
    """Analytics dashboard page."""
    st.header("Analytics Dashboard")
    
    if not st.session_state.generated_articles:
        st.info("No articles available for analysis. Generate some articles first!")
        return
    
    # Create analytics data
    articles_data = []
    for article in st.session_state.generated_articles:
        data = {
            'headline': article['headline'][:30] + "...",
            'word_count': article['word_count'],
            'category': article.get('topic_category', 'General'),
            'quality_score': article.get('quality_evaluation', {}).get('overall_score', 0),
            'fact_check_score': article.get('fact_check', {}).get('overall_score', 0),
            'timestamp': article['timestamp']
        }
        articles_data.append(data)
    
    df = pd.DataFrame(articles_data)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Articles", len(df))
    with col2:
        st.metric("Avg Word Count", f"{df['word_count'].mean():.0f}")
    with col3:
        st.metric("Avg Quality Score", f"{df['quality_score'].mean():.1f}")
    with col4:
        st.metric("Avg Fact Check", f"{df['fact_check_score'].mean():.1f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Category distribution
        fig_category = px.pie(df, names='category', title="Articles by Category")
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        # Quality vs Fact Check scores
        fig_scores = px.scatter(
            df, x='quality_score', y='fact_check_score',
            title="Quality vs Fact Check Scores",
            labels={'quality_score': 'Quality Score', 'fact_check_score': 'Fact Check Score'}
        )
        st.plotly_chart(fig_scores, use_container_width=True)
    
    # Word count distribution
    fig_words = px.histogram(df, x='word_count', title="Word Count Distribution")
    st.plotly_chart(fig_words, use_container_width=True)

def style_guides_page():
    """Style guides and templates page."""
    st.header("Style Guides & Templates")
    
    # Style guide tabs
    tabs = st.tabs(["AP Style Guide", "Blog Writing", "Social Media", "Newsletter"])
    
    with tabs[0]:
        st.subheader("Associated Press (AP) Style Guide")
        st.markdown("""
        ### Key AP Style Rules for News Writing
        
        **Datelines:**
        - Use city name in ALL CAPS followed by state abbreviation
        - Format: WASHINGTON - Article content begins here...
        
        **Attribution:**
        - Always attribute information to sources
        - Use "according to" or "said" for attribution
        - Include full names and titles on first reference
        
        **Numbers:**
        - Spell out numbers one through nine
        - Use figures for 10 and above
        - Always spell out numbers that begin sentences
        
        **Dates and Times:**
        - Use month abbreviations except March, April, May, June, July
        - Format: Jan. 15, 2025
        - Use lowercase for a.m. and p.m.
        """)
    
    with tabs[1]:
        st.subheader("Blog Writing Style")
        st.markdown("""
        ### Blog Writing Best Practices
        
        **Headlines:**
        - Use compelling, descriptive headlines
        - Include keywords for SEO
        - Keep under 60 characters when possible
        
        **Structure:**
        - Use subheadings (H2, H3) to break up content
        - Keep paragraphs short (2-4 sentences)
        - Use bullet points and numbered lists
        
        **Tone:**
        - Conversational and engaging
        - Address readers directly using "you"
        - Show personality while maintaining professionalism
        """)
    
    with tabs[2]:
        st.subheader("Social Media Guidelines")
        st.markdown("""
        ### Platform-Specific Guidelines
        
        **Twitter/X (280 characters):**
        - Lead with the most important information
        - Use relevant hashtags (2-3 maximum)
        - Include engaging questions
        
        **LinkedIn (Professional):**
        - Professional tone and language
        - Include industry insights
        - Use relevant professional hashtags
        
        **Facebook (Casual):**
        - More conversational tone
        - Encourage comments and shares
        - Use emojis appropriately
        """)
    
    with tabs[3]:
        st.subheader("Newsletter Format")
        st.markdown("""
        ### Newsletter Best Practices
        
        **Structure:**
        - Header with newsletter branding
        - Personal greeting
        - Quick summary box
        - Main content with clear sections
        - Call-to-action
        - Footer with contact information
        
        **Tone:**
        - Personal and friendly
        - Direct communication style
        - Use "you" to address readers
        - Include personal insights
        """)

def create_analysis_report(article_data):
    """Create comprehensive analysis report."""
    report = f"""
COMPREHENSIVE ARTICLE ANALYSIS REPORT
===================================

Article: {article_data['headline']}
Generated: {article_data['timestamp']}
Word Count: {article_data['word_count']}

ARTICLE CONTENT:
{article_data['full_article']}

"""
    
    if 'fact_check' in article_data:
        fc = article_data['fact_check']
        report += f"""
FACT CHECK ANALYSIS:
Overall Score: {fc['overall_score']}/100
- Objectivity: {fc['objectivity_score']}/100
- Source Attribution: {fc['source_attribution_score']}/100
- Fact Consistency: {fc['fact_consistency_score']}/100
- Credibility: {fc['credibility_score']}/100

Recommendations:
"""
        for rec in fc.get('recommendations', []):
            report += f"- {rec}\n"
    
    if 'quality_evaluation' in article_data:
        qe = article_data['quality_evaluation']
        report += f"""
QUALITY EVALUATION:
Overall Score: {qe['overall_score']}/100
Professional Rating: {qe['professional_rating']}

Category Scores:
"""
        for category, data in qe['category_scores'].items():
            score = data['score'] if isinstance(data, dict) else data
            report += f"- {category.replace('_', ' ').title()}: {score}/100\n"
        
        report += "\nStrengths:\n"
        for strength in qe.get('strengths', []):
            report += f"✓ {strength}\n"
        
        report += "\nAreas for Improvement:\n"
        for improvement in qe.get('areas_for_improvement', []):
            report += f"• {improvement}\n"
    
    return report

if __name__ == "__main__":
    main()
