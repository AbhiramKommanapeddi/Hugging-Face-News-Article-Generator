import re
import textstat
from typing import Dict, List
import numpy as np
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class QualityMetrics:
    """
    Comprehensive quality assessment system for news articles.
    Evaluates writing quality, accuracy, structure, and variety.
    """
    
    def __init__(self):
        self.quality_weights = {
            'writing_quality': 0.40,
            'accuracy': 0.25,
            'structure': 0.20,
            'variety': 0.15
        }
        
        self.readability_thresholds = {
            'excellent': (6, 9),      # Grade 6-9 (ideal for news)
            'good': (9, 12),          # Grade 9-12
            'fair': (12, 16),         # Grade 12-16
            'poor': (16, float('inf')) # Above grade 16
        }
        
        self.structure_elements = {
            'lead_quality': {
                'who': r'\b(?:said|announced|stated|reported|confirmed)\b',
                'what': r'\b(?:happened|occurred|took place|resulted)\b',
                'when': r'\b(?:today|yesterday|this week|on \w+day|\d{1,2}/\d{1,2})\b',
                'where': r'\b(?:in|at|from)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
                'why': r'\b(?:because|due to|as a result|following)\b'
            },
            'inverted_pyramid': {
                'lead_importance': 0.4,
                'body_importance': 0.4,
                'conclusion_importance': 0.2
            }
        }
        
        self.journalism_standards = {
            'attribution_frequency': 0.02,  # At least 2% of words should be attribution
            'quote_frequency': 0.01,        # At least 1% should be quotes
            'paragraph_length': (50, 150),  # Ideal paragraph length in words
            'sentence_length': (15, 25)     # Ideal sentence length in words
        }
    
    def evaluate_article(self, article_data: Dict) -> Dict:
        """
        Comprehensive quality evaluation of a news article.
        
        Args:
            article_data: Dictionary containing article content and metadata
            
        Returns:
            Complete quality assessment report
        """
        try:
            evaluation = {
                'overall_score': 0,
                'category_scores': {},
                'detailed_metrics': {},
                'recommendations': [],
                'strengths': [],
                'areas_for_improvement': [],
                'grade_level': None,
                'professional_rating': None
            }
            
            # Evaluate each quality category
            evaluation['category_scores']['writing_quality'] = self._evaluate_writing_quality(article_data)
            evaluation['category_scores']['accuracy'] = self._evaluate_accuracy(article_data)
            evaluation['category_scores']['structure'] = self._evaluate_structure(article_data)
            evaluation['category_scores']['variety'] = self._evaluate_variety(article_data)
            
            # Calculate overall score
            evaluation['overall_score'] = self._calculate_overall_score(evaluation['category_scores'])
            
            # Generate detailed metrics
            evaluation['detailed_metrics'] = self._generate_detailed_metrics(article_data)
            
            # Determine professional rating
            evaluation['professional_rating'] = self._get_professional_rating(evaluation['overall_score'])
            
            # Generate recommendations
            evaluation['recommendations'] = self._generate_quality_recommendations(evaluation)
            
            # Identify strengths and improvements
            evaluation['strengths'], evaluation['areas_for_improvement'] = self._identify_strengths_and_improvements(evaluation)
            
            logger.info(f"Quality evaluation completed. Overall score: {evaluation['overall_score']}")
            
        except Exception as e:
            logger.error(f"Error in quality evaluation: {e}")
            evaluation = self._create_error_evaluation(str(e))
        
        return evaluation
    
    def _evaluate_writing_quality(self, article_data: Dict) -> Dict:
        """Evaluate writing quality (40% of total score)."""
        full_text = article_data.get('full_article', '')
        
        if not full_text:
            return {'score': 0, 'details': 'No article text to evaluate'}
        
        metrics = {}
        
        # Readability analysis
        flesch_score = textstat.flesch_reading_ease(full_text)
        grade_level = textstat.flesch_kincaid_grade(full_text)
        
        # Score readability (ideal for news is 6-9th grade)
        if 6 <= grade_level <= 9:
            readability_score = 100
        elif 9 < grade_level <= 12:
            readability_score = 80
        elif 12 < grade_level <= 16:
            readability_score = 60
        else:
            readability_score = 40
        
        metrics['readability_score'] = readability_score
        metrics['grade_level'] = grade_level
        metrics['flesch_score'] = flesch_score
        
        # Sentence variety
        sentences = [s.strip() for s in full_text.split('.') if s.strip()]
        sentence_lengths = [len(s.split()) for s in sentences]
        
        if sentence_lengths:
            avg_sentence_length = np.mean(sentence_lengths)
            sentence_variety = np.std(sentence_lengths)
            
            # Score sentence structure
            if 15 <= avg_sentence_length <= 25:
                sentence_score = 100
            elif 10 <= avg_sentence_length < 15 or 25 < avg_sentence_length <= 30:
                sentence_score = 80
            else:
                sentence_score = 60
            
            # Bonus for variety
            if sentence_variety > 5:
                sentence_score = min(100, sentence_score + 10)
        else:
            sentence_score = 0
        
        metrics['sentence_score'] = sentence_score
        metrics['avg_sentence_length'] = avg_sentence_length if sentence_lengths else 0
        metrics['sentence_variety'] = sentence_variety if sentence_lengths else 0
        
        # Grammar and style check
        grammar_score = self._check_grammar_style(full_text)
        metrics['grammar_score'] = grammar_score
        
        # Professional tone
        tone_score = self._assess_professional_tone(full_text)
        metrics['tone_score'] = tone_score
        
        # Calculate overall writing quality score
        overall_score = (
            readability_score * 0.3 +
            sentence_score * 0.25 +
            grammar_score * 0.25 +
            tone_score * 0.2
        )
        
        return {
            'score': round(overall_score),
            'details': metrics
        }
    
    def _evaluate_accuracy(self, article_data: Dict) -> Dict:
        """Evaluate accuracy and fact handling (25% of total score)."""
        # Use fact-checking results if available
        fact_check = article_data.get('fact_check', {})
        
        if fact_check:
            # Use existing fact-check scores
            accuracy_score = (
                fact_check.get('fact_consistency_score', 70) * 0.4 +
                fact_check.get('source_attribution_score', 70) * 0.3 +
                fact_check.get('credibility_score', 70) * 0.3
            )
        else:
            # Basic accuracy assessment
            full_text = article_data.get('full_article', '')
            accuracy_score = self._basic_accuracy_check(full_text)
        
        # Check for fact incorporation
        source_facts = article_data.get('facts', [])
        fact_incorporation_score = self._check_fact_incorporation(
            article_data.get('full_article', ''), 
            source_facts
        )
        
        final_score = (accuracy_score * 0.7 + fact_incorporation_score * 0.3)
        
        return {
            'score': round(final_score),
            'details': {
                'fact_check_score': accuracy_score,
                'fact_incorporation_score': fact_incorporation_score,
                'verified_facts': len(source_facts) if source_facts else 0
            }
        }
    
    def _evaluate_structure(self, article_data: Dict) -> Dict:
        """Evaluate journalistic structure (20% of total score)."""
        lead = article_data.get('lead', '')
        body = article_data.get('body', '')
        conclusion = article_data.get('conclusion', '')
        full_text = article_data.get('full_article', '')
        
        metrics = {}
        
        # Lead quality (5 W's and H)
        lead_score = self._evaluate_lead_quality(lead)
        metrics['lead_score'] = lead_score
        
        # Inverted pyramid structure
        pyramid_score = self._check_inverted_pyramid(lead, body, conclusion)
        metrics['pyramid_score'] = pyramid_score
        
        # Paragraph structure
        paragraph_score = self._evaluate_paragraph_structure(full_text)
        metrics['paragraph_score'] = paragraph_score
        
        # Transition quality
        transition_score = self._evaluate_transitions(full_text)
        metrics['transition_score'] = transition_score
        
        # Overall structure score
        overall_score = (
            lead_score * 0.35 +
            pyramid_score * 0.25 +
            paragraph_score * 0.25 +
            transition_score * 0.15
        )
        
        return {
            'score': round(overall_score),
            'details': metrics
        }
    
    def _evaluate_variety(self, article_data: Dict) -> Dict:
        """Evaluate topic and style variety (15% of total score)."""
        full_text = article_data.get('full_article', '')
        metadata = article_data.get('metadata', {})
        
        metrics = {}
        
        # Vocabulary diversity
        words = re.findall(r'\b\w+\b', full_text.lower())
        unique_words = set(words)
        vocabulary_diversity = len(unique_words) / len(words) if words else 0
        
        # Score vocabulary diversity
        if vocabulary_diversity > 0.6:
            vocab_score = 100
        elif vocabulary_diversity > 0.5:
            vocab_score = 85
        elif vocabulary_diversity > 0.4:
            vocab_score = 70
        else:
            vocab_score = 50
        
        metrics['vocabulary_diversity'] = vocabulary_diversity
        metrics['vocab_score'] = vocab_score
        
        # Sentence structure variety
        structure_variety = self._analyze_sentence_structures(full_text)
        metrics['structure_variety'] = structure_variety
        
        # Content type variety (quotes, facts, analysis)
        content_variety = self._analyze_content_variety(full_text)
        metrics['content_variety'] = content_variety
        
        # Overall variety score
        overall_score = (
            vocab_score * 0.4 +
            structure_variety * 0.3 +
            content_variety * 0.3
        )
        
        return {
            'score': round(overall_score),
            'details': metrics
        }
    
    def _check_grammar_style(self, text: str) -> int:
        """Basic grammar and style checking."""
        score = 100
        
        # Check for common errors
        errors = []
        
        # Passive voice check (journalism prefers active)
        passive_patterns = [r'\bwas\s+\w+ed\b', r'\bwere\s+\w+ed\b', r'\bbeen\s+\w+ed\b']
        passive_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in passive_patterns)
        
        if passive_count > len(text.split()) * 0.1:  # More than 10% passive
            score -= 15
            errors.append("Excessive passive voice")
        
        # Check for proper capitalization
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and not sentence[0].isupper():
                score -= 5
                errors.append("Capitalization error")
                break
        
        # Check for run-on sentences (very long sentences)
        long_sentences = [s for s in sentences if len(s.split()) > 40]
        if len(long_sentences) > len(sentences) * 0.2:
            score -= 10
            errors.append("Run-on sentences")
        
        return max(0, score)
    
    def _assess_professional_tone(self, text: str) -> int:
        """Assess professional journalistic tone."""
        score = 100
        
        # Check for informal language
        informal_words = [
            'gonna', 'wanna', 'gotta', 'kinda', 'sorta',
            'yeah', 'okay', 'ok', 'wow', 'hey'
        ]
        
        informal_count = sum(1 for word in informal_words if word in text.lower())
        score -= informal_count * 10
        
        # Check for first person (should be minimal in news)
        first_person = len(re.findall(r'\b(?:i|me|my|myself|we|us|our)\b', text, re.IGNORECASE))
        if first_person > 2:
            score -= 20
        
        # Check for contractions (should be minimal in formal news)
        contractions = len(re.findall(r"\w+'\w+", text))
        score -= contractions * 5
        
        return max(0, score)
    
    def _basic_accuracy_check(self, text: str) -> int:
        """Basic accuracy indicators check."""
        score = 80  # Default score
        
        # Check for attribution
        attribution_patterns = [
            r'according to', r'sources say', r'officials confirmed',
            r'in a statement', r'told reporters'
        ]
        
        attributions = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in attribution_patterns)
        words = len(text.split())
        attribution_ratio = attributions / (words / 100) if words else 0
        
        if attribution_ratio >= 2:
            score += 10
        elif attribution_ratio >= 1:
            score += 5
        elif attribution_ratio < 0.5:
            score -= 10
        
        # Check for specific details (dates, numbers, names)
        dates = len(re.findall(r'\b\d{1,2}/\d{1,2}/\d{4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', text))
        numbers = len(re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', text))
        
        detail_score = min(20, (dates + numbers) * 2)
        score += detail_score
        
        return min(100, score)
    
    def _check_fact_incorporation(self, text: str, source_facts: List[str]) -> int:
        """Check how well source facts are incorporated."""
        if not source_facts:
            return 85  # Default score when no facts to check
        
        incorporated_facts = 0
        text_lower = text.lower()
        
        for fact in source_facts:
            # Simple keyword matching
            fact_words = set(re.findall(r'\b\w+\b', fact.lower()))
            if len(fact_words) == 0:
                continue
                
            # Check if majority of fact words appear in text
            found_words = sum(1 for word in fact_words if word in text_lower)
            if found_words >= len(fact_words) * 0.6:
                incorporated_facts += 1
        
        incorporation_rate = incorporated_facts / len(source_facts)
        return round(incorporation_rate * 100)
    
    def _evaluate_lead_quality(self, lead: str) -> int:
        """Evaluate the quality of the lead paragraph."""
        if not lead:
            return 0
        
        score = 100
        
        # Check for 5 W's and H elements
        elements_found = 0
        
        for element, pattern in self.structure_elements['lead_quality'].items():
            if re.search(pattern, lead, re.IGNORECASE):
                elements_found += 1
        
        # Score based on elements found
        element_score = (elements_found / 5) * 100
        
        # Check lead length (should be 25-35 words for news)
        word_count = len(lead.split())
        if 25 <= word_count <= 35:
            length_score = 100
        elif 20 <= word_count < 25 or 35 < word_count <= 40:
            length_score = 85
        elif 15 <= word_count < 20 or 40 < word_count <= 50:
            length_score = 70
        else:
            length_score = 50
        
        return round((element_score * 0.6 + length_score * 0.4))
    
    def _check_inverted_pyramid(self, lead: str, body: str, conclusion: str) -> int:
        """Check adherence to inverted pyramid structure."""
        # Analyze information importance distribution
        lead_words = len(lead.split()) if lead else 0
        body_words = len(body.split()) if body else 0
        conclusion_words = len(conclusion.split()) if conclusion else 0
        
        total_words = lead_words + body_words + conclusion_words
        
        if total_words == 0:
            return 0
        
        # Calculate proportions
        lead_prop = lead_words / total_words
        body_prop = body_words / total_words
        conclusion_prop = conclusion_words / total_words
        
        # Ideal proportions for inverted pyramid
        ideal_lead = 0.3
        ideal_body = 0.6
        ideal_conclusion = 0.1
        
        # Calculate deviation from ideal
        lead_dev = abs(lead_prop - ideal_lead)
        body_dev = abs(body_prop - ideal_body)
        conclusion_dev = abs(conclusion_prop - ideal_conclusion)
        
        # Score based on deviation (lower deviation = higher score)
        total_deviation = lead_dev + body_dev + conclusion_dev
        score = max(0, 100 - (total_deviation * 200))  # Scale deviation to score
        
        return round(score)
    
    def _evaluate_paragraph_structure(self, text: str) -> int:
        """Evaluate paragraph structure and length."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return 0
        
        paragraph_lengths = [len(p.split()) for p in paragraphs]
        avg_length = np.mean(paragraph_lengths)
        
        # Ideal paragraph length for news: 50-150 words
        if 50 <= avg_length <= 150:
            length_score = 100
        elif 30 <= avg_length < 50 or 150 < avg_length <= 200:
            length_score = 85
        else:
            length_score = 60
        
        # Check for variety in paragraph lengths
        length_variety = np.std(paragraph_lengths) if len(paragraph_lengths) > 1 else 0
        variety_score = min(100, length_variety * 2)  # Encourage some variety
        
        return round((length_score * 0.7 + variety_score * 0.3))
    
    def _evaluate_transitions(self, text: str) -> int:
        """Evaluate quality of transitions between paragraphs."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if len(paragraphs) < 2:
            return 100  # No transitions needed
        
        transition_words = [
            'however', 'furthermore', 'additionally', 'meanwhile',
            'consequently', 'therefore', 'moreover', 'nevertheless',
            'in addition', 'on the other hand', 'as a result'
        ]
        
        transitions_found = 0
        for paragraph in paragraphs[1:]:  # Skip first paragraph
            first_sentence = paragraph.split('.')[0].lower()
            if any(trans in first_sentence for trans in transition_words):
                transitions_found += 1
        
        transition_rate = transitions_found / (len(paragraphs) - 1)
        
        # Score based on transition usage
        if transition_rate >= 0.7:
            return 100
        elif transition_rate >= 0.5:
            return 85
        elif transition_rate >= 0.3:
            return 70
        else:
            return 50
    
    def _analyze_sentence_structures(self, text: str) -> int:
        """Analyze variety in sentence structures."""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if not sentences:
            return 0
        
        # Analyze sentence starters
        starters = []
        for sentence in sentences:
            words = sentence.split()
            if words:
                starters.append(words[0].lower())
        
        # Calculate variety in sentence starters
        starter_variety = len(set(starters)) / len(starters) if starters else 0
        
        return round(starter_variety * 100)
    
    def _analyze_content_variety(self, text: str) -> int:
        """Analyze variety in content types (quotes, facts, analysis)."""
        # Count different content types
        quotes = len(re.findall(r'"[^"]*"', text))
        numbers = len(re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', text))
        attributions = len(re.findall(r'according to|sources say|officials', text, re.IGNORECASE))
        
        total_elements = quotes + numbers + attributions
        words = len(text.split())
        
        if words == 0:
            return 0
        
        variety_ratio = total_elements / (words / 100)  # Per 100 words
        
        # Score based on variety
        if variety_ratio >= 5:
            return 100
        elif variety_ratio >= 3:
            return 85
        elif variety_ratio >= 2:
            return 70
        else:
            return 50
    
    def _calculate_overall_score(self, category_scores: Dict) -> int:
        """Calculate weighted overall quality score."""
        total_score = 0
        
        for category, weight in self.quality_weights.items():
            category_data = category_scores.get(category, {'score': 0})
            score = category_data['score'] if isinstance(category_data, dict) else category_data
            total_score += score * weight
        
        return round(total_score)
    
    def _generate_detailed_metrics(self, article_data: Dict) -> Dict:
        """Generate comprehensive detailed metrics."""
        full_text = article_data.get('full_article', '')
        
        if not full_text:
            return {}
        
        return {
            'word_count': len(full_text.split()),
            'sentence_count': len([s for s in full_text.split('.') if s.strip()]),
            'paragraph_count': len([p for p in full_text.split('\n\n') if p.strip()]),
            'readability_grade': round(textstat.flesch_kincaid_grade(full_text), 1),
            'flesch_score': round(textstat.flesch_reading_ease(full_text), 1),
            'avg_sentence_length': round(len(full_text.split()) / max(1, len([s for s in full_text.split('.') if s.strip()])), 1),
            'quote_count': len(re.findall(r'"[^"]*"', full_text)),
            'attribution_count': len(re.findall(r'according to|sources say|officials', full_text, re.IGNORECASE)),
            'passive_voice_ratio': self._calculate_passive_voice_ratio(full_text)
        }
    
    def _calculate_passive_voice_ratio(self, text: str) -> float:
        """Calculate ratio of passive voice sentences."""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        passive_patterns = [r'\bwas\s+\w+ed\b', r'\bwere\s+\w+ed\b', r'\bbeen\s+\w+ed\b']
        
        passive_sentences = 0
        for sentence in sentences:
            for pattern in passive_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    passive_sentences += 1
                    break
        
        return round(passive_sentences / max(1, len(sentences)), 3)
    
    def _get_professional_rating(self, score: int) -> str:
        """Convert numeric score to professional rating."""
        if score >= 90:
            return "Excellent - Publication Ready"
        elif score >= 80:
            return "Very Good - Minor Revisions"
        elif score >= 70:
            return "Good - Some Improvements Needed"
        elif score >= 60:
            return "Fair - Significant Revisions Required"
        else:
            return "Poor - Major Overhaul Needed"
    
    def _generate_quality_recommendations(self, evaluation: Dict) -> List[str]:
        """Generate specific quality improvement recommendations."""
        recommendations = []
        category_scores = evaluation['category_scores']
        
        # Writing quality recommendations
        writing_score = category_scores.get('writing_quality', {}).get('score', 0)
        if writing_score < 80:
            recommendations.append("Improve readability by using shorter sentences and simpler vocabulary")
            recommendations.append("Vary sentence structure to maintain reader engagement")
        
        # Accuracy recommendations
        accuracy_score = category_scores.get('accuracy', {}).get('score', 0)
        if accuracy_score < 80:
            recommendations.append("Add more source attributions and fact verification")
            recommendations.append("Ensure all claims are properly substantiated")
        
        # Structure recommendations
        structure_score = category_scores.get('structure', {}).get('score', 0)
        if structure_score < 80:
            recommendations.append("Strengthen the lead paragraph with all essential elements")
            recommendations.append("Better organize content using inverted pyramid structure")
        
        # Variety recommendations
        variety_score = category_scores.get('variety', {}).get('score', 0)
        if variety_score < 80:
            recommendations.append("Increase vocabulary diversity and sentence variety")
            recommendations.append("Include more diverse content types (quotes, statistics, analysis)")
        
        return recommendations
    
    def _identify_strengths_and_improvements(self, evaluation: Dict) -> tuple:
        """Identify specific strengths and areas for improvement."""
        strengths = []
        improvements = []
        
        category_scores = evaluation['category_scores']
        
        for category, data in category_scores.items():
            score = data['score'] if isinstance(data, dict) else data
            
            if score >= 85:
                strengths.append(f"Strong {category.replace('_', ' ')}")
            elif score < 70:
                improvements.append(f"Improve {category.replace('_', ' ')}")
        
        # Add specific strengths based on detailed metrics
        details = evaluation.get('detailed_metrics', {})
        
        if details.get('readability_grade', 20) <= 9:
            strengths.append("Excellent readability for target audience")
        
        if details.get('attribution_count', 0) >= 3:
            strengths.append("Good source attribution")
        
        if details.get('passive_voice_ratio', 1) <= 0.1:
            strengths.append("Effective use of active voice")
        
        return strengths, improvements
    
    def _create_error_evaluation(self, error_msg: str) -> Dict:
        """Create error evaluation when assessment fails."""
        return {
            'overall_score': 0,
            'category_scores': {
                'writing_quality': {'score': 0, 'details': f'Error: {error_msg}'},
                'accuracy': {'score': 0, 'details': f'Error: {error_msg}'},
                'structure': {'score': 0, 'details': f'Error: {error_msg}'},
                'variety': {'score': 0, 'details': f'Error: {error_msg}'}
            },
            'detailed_metrics': {},
            'recommendations': ['Fix evaluation error and retry assessment'],
            'strengths': [],
            'areas_for_improvement': ['Address technical evaluation issues'],
            'professional_rating': 'Assessment Failed'
        }
    
    def generate_quality_report(self, article_data: Dict) -> str:
        """Generate a formatted quality assessment report."""
        evaluation = article_data.get('quality_evaluation', {})
        
        if not evaluation:
            return "No quality evaluation data available."
        
        report = f"""
QUALITY ASSESSMENT REPORT
========================

Article: {article_data.get('headline', 'Unknown')}
Overall Score: {evaluation.get('overall_score', 0)}/100
Professional Rating: {evaluation.get('professional_rating', 'Unknown')}

CATEGORY SCORES:
"""
        
        for category, data in evaluation.get('category_scores', {}).items():
            score = data['score'] if isinstance(data, dict) else data
            report += f"- {category.replace('_', ' ').title()}: {score}/100\n"
        
        report += "\nDETAILED METRICS:\n"
        for metric, value in evaluation.get('detailed_metrics', {}).items():
            report += f"- {metric.replace('_', ' ').title()}: {value}\n"
        
        report += "\nSTRENGTHS:\n"
        for strength in evaluation.get('strengths', []):
            report += f"✓ {strength}\n"
        
        report += "\nAREAS FOR IMPROVEMENT:\n"
        for improvement in evaluation.get('areas_for_improvement', []):
            report += f"• {improvement}\n"
        
        report += "\nRECOMMENDATIONS:\n"
        for i, rec in enumerate(evaluation.get('recommendations', []), 1):
            report += f"{i}. {rec}\n"
        
        return report
