#!/usr/bin/env python3
"""
Basic test version of the News Generator for demonstration purposes.
This version uses simple text generation without heavy ML dependencies.
"""

import re
import random
from typing import List, Dict, Optional
from datetime import datetime
import json

class MockNewsGenerator:
    """Mock news generator for demonstration purposes."""
    
    def __init__(self):
        self.templates = {
            'lead': [
                "{location} - {main_fact}",
                "In a significant development, {main_fact}",
                "{main_fact}, according to sources",
                "Breaking news: {main_fact}"
            ],
            'body': [
                "The development comes after extensive research and planning.",
                "Officials confirmed the details during a press conference.",
                "This represents a major step forward for the organization.",
                "The announcement has generated significant interest.",
                "Industry experts are calling this a game-changing moment."
            ],
            'conclusion': [
                "The full impact of this development remains to be seen.",
                "More details are expected to be announced in the coming weeks.",
                "This story will continue to develop as more information becomes available.",
                "The organization plans to provide updates as the situation evolves."
            ]
        }
    
    def generate_article(self, headline: str, facts: List[str], quotes: List[Dict] = None,
                        style: str = "news", target_length: int = 500) -> Dict:
        """Generate a mock article for demonstration."""
        
        # Generate lead
        if facts:
            main_fact = facts[0]
            lead_template = random.choice(self.templates['lead'])
            lead = lead_template.format(main_fact=main_fact, location="WASHINGTON")
        else:
            lead = f"A significant development has occurred regarding {headline.lower()}."
        
        # Generate body
        body_sentences = []
        for fact in facts[1:4]:  # Use facts 2-4
            body_sentences.append(f"According to reports, {fact.lower()}.")
        
        # Add some template sentences
        body_sentences.extend(random.sample(self.templates['body'], 2))
        
        # Add quotes if provided
        if quotes:
            for quote_data in quotes[:2]:  # Max 2 quotes
                quote = quote_data.get('quote', '')
                speaker = quote_data.get('speaker', 'a spokesperson')
                title = quote_data.get('title', '')
                
                if title:
                    attribution = f"{speaker}, {title}, said"
                else:
                    attribution = f"{speaker} said"
                
                body_sentences.append(f'"{quote}," {attribution}.')
        
        body = ' '.join(body_sentences)
        
        # Generate conclusion
        conclusion = random.choice(self.templates['conclusion'])
        
        # Combine full article
        full_article = f"{lead}\n\n{body}\n\n{conclusion}"
        
        return {
            'headline': headline,
            'lead': lead,
            'body': body,
            'conclusion': conclusion,
            'full_article': full_article,
            'word_count': len(full_article.split()),
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'style': style,
                'target_length': target_length,
                'fact_count': len(facts),
                'quote_count': len(quotes) if quotes else 0
            }
        }

class MockFactChecker:
    """Mock fact checker for demonstration."""
    
    def verify_facts(self, article_text: str, source_facts: List[str] = None) -> Dict:
        """Generate mock fact check results."""
        return {
            'overall_score': random.randint(75, 95),
            'objectivity_score': random.randint(80, 95),
            'source_attribution_score': random.randint(70, 90),
            'fact_consistency_score': random.randint(85, 95),
            'credibility_score': random.randint(75, 90),
            'recommendations': [
                "Consider adding more specific source attributions",
                "Verify all statistical claims with primary sources",
                "Ensure balanced perspective in reporting"
            ],
            'flagged_content': [],
            'verified_claims': len(source_facts) if source_facts else 0
        }

class MockQualityMetrics:
    """Mock quality metrics for demonstration."""
    
    def evaluate_article(self, article_data: Dict) -> Dict:
        """Generate mock quality evaluation."""
        writing_score = random.randint(75, 95)
        accuracy_score = random.randint(80, 90)
        structure_score = random.randint(85, 95)
        variety_score = random.randint(70, 85)
        
        overall_score = round((writing_score + accuracy_score + structure_score + variety_score) / 4)
        
        return {
            'overall_score': overall_score,
            'category_scores': {
                'writing_quality': {'score': writing_score},
                'accuracy': {'score': accuracy_score},
                'structure': {'score': structure_score},
                'variety': {'score': variety_score}
            },
            'professional_rating': self._get_professional_rating(overall_score),
            'strengths': [
                "Clear and engaging writing style",
                "Good use of source attribution",
                "Well-structured content"
            ],
            'areas_for_improvement': [
                "Could include more diverse sources",
                "Consider shorter paragraphs for readability"
            ],
            'detailed_metrics': {
                'word_count': article_data.get('word_count', 0),
                'sentence_count': len(article_data.get('full_article', '').split('.')),
                'readability_grade': round(random.uniform(7.5, 9.5), 1)
            }
        }
    
    def _get_professional_rating(self, score: int) -> str:
        """Convert score to professional rating."""
        if score >= 90:
            return "Excellent - Publication Ready"
        elif score >= 80:
            return "Very Good - Minor Revisions"
        elif score >= 70:
            return "Good - Some Improvements Needed"
        else:
            return "Fair - Significant Revisions Required"

class MockStyleManager:
    """Mock style manager for demonstration."""
    
    def validate_style_compliance(self, article_text: str, style: str) -> Dict:
        """Generate mock style compliance results."""
        return {
            'style': style,
            'score': random.randint(80, 95),
            'issues': [
                "Consider using more active voice",
                "Some sentences could be shorter"
            ],
            'suggestions': [
                "Follow AP style for numbers and dates",
                "Use consistent attribution format"
            ]
        }

def load_sample_topics():
    """Load sample topics for testing."""
    return [
        {
            'headline': "Tech Company Announces Revolutionary AI Breakthrough",
            'facts': [
                "Company developed new language model with 500 billion parameters",
                "Model shows 40% improvement in accuracy over previous versions",
                "Technology will be integrated into consumer products next year",
                "Research team spent three years developing the breakthrough"
            ],
            'quotes': [
                {
                    'quote': "This represents a fundamental shift in how we approach artificial intelligence",
                    'speaker': "Dr. Sarah Chen",
                    'title': "Chief Technology Officer"
                }
            ],
            'location': "San Francisco",
            'category': "Technology"
        },
        {
            'headline': "Local School District Implements Innovative STEM Program",
            'facts': [
                "Program launched in 15 elementary schools across the district",
                "Students will learn coding, robotics, and engineering principles",
                "Initial funding of $2.5 million provided by state grant",
                "Teachers completed 40 hours of specialized training"
            ],
            'quotes': [
                {
                    'quote': "We're preparing our students for the jobs of tomorrow",
                    'speaker': "Jennifer Walsh",
                    'title': "Superintendent"
                }
            ],
            'location': "Springfield",
            'category': "Education"
        }
    ]

def save_article_to_file(article_data: Dict, output_dir: str = "sample_articles") -> str:
    """Save article to file."""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    headline = article_data.get('headline', 'untitled')
    safe_filename = re.sub(r'[^\w\s-]', '', headline).strip()
    safe_filename = re.sub(r'[-\s]+', '_', safe_filename).lower()[:50]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_filename}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, indent=2, ensure_ascii=False, default=str)
    
    return filepath

def main():
    """Run basic demonstration."""
    print("🚀 NEWS ARTICLE GENERATOR - BASIC DEMO")
    print("=" * 50)
    
    # Initialize mock components
    news_gen = MockNewsGenerator()
    fact_checker = MockFactChecker()
    quality_checker = MockQualityMetrics()
    style_mgr = MockStyleManager()
    
    # Load sample topics
    sample_topics = load_sample_topics()
    
    print(f"📋 Loaded {len(sample_topics)} sample topics")
    
    # Generate articles for each topic
    for i, topic in enumerate(sample_topics, 1):
        print(f"\n📰 Generating Article {i}: {topic['headline']}")
        print("-" * 60)
        
        # Generate article
        article_data = news_gen.generate_article(
            headline=topic['headline'],
            facts=topic['facts'],
            quotes=topic['quotes'],
            style='news'
        )
        
        # Add metadata
        article_data['topic_category'] = topic['category']
        article_data['location'] = topic['location']
        
        # Perform analysis
        article_data['fact_check'] = fact_checker.verify_facts(
            article_data['full_article'], topic['facts']
        )
        
        article_data['quality_evaluation'] = quality_checker.evaluate_article(article_data)
        
        article_data['style_compliance'] = style_mgr.validate_style_compliance(
            article_data['full_article'], 'news'
        )
        
        # Display results
        print(f"Word Count: {article_data['word_count']}")
        print(f"Quality Score: {article_data['quality_evaluation']['overall_score']}/100")
        print(f"Fact Check Score: {article_data['fact_check']['overall_score']}/100")
        print(f"Style Compliance: {article_data['style_compliance']['score']}/100")
        
        print(f"\nArticle Preview:")
        preview = article_data['full_article'][:300] + "..."
        print(preview)
        
        # Save article
        filepath = save_article_to_file(article_data)
        print(f"\n💾 Article saved to: {filepath}")
    
    print(f"\n🎉 Demo completed! Generated {len(sample_topics)} articles.")
    print("📁 Check the 'sample_articles' directory for the generated content.")

if __name__ == "__main__":
    main()
