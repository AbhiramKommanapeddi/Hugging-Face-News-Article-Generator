import re
import requests
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class FactChecker:
    """
    Fact verification and source attribution system.
    Provides objectivity checks and credibility scoring.
    """
    
    def __init__(self):
        self.credible_sources = {
            'high_credibility': [
                'reuters.com', 'ap.org', 'bbc.com', 'npr.org',
                'pbs.org', 'cbc.ca', 'abc.net.au'
            ],
            'medium_credibility': [
                'cnn.com', 'foxnews.com', 'nbc.com', 'cbs.com',
                'abcnews.go.com', 'washingtonpost.com', 'nytimes.com'
            ],
            'academic': [
                'edu', 'gov', 'org'
            ]
        }
        
        self.bias_indicators = {
            'strongly_positive': [
                'amazing', 'incredible', 'fantastic', 'outstanding',
                'revolutionary', 'groundbreaking', 'miraculous'
            ],
            'strongly_negative': [
                'terrible', 'awful', 'disaster', 'catastrophic',
                'devastating', 'horrific', 'appalling'
            ],
            'loaded_language': [
                'obviously', 'clearly', 'undoubtedly', 'everyone knows',
                'it\'s clear that', 'without question'
            ]
        }
        
        self.fact_check_patterns = {
            'statistics': r'\b\d+(?:\.\d+)?%|\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand)',
            'dates': r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
            'quotes': r'"[^"]*"',
            'claims': r'\b(?:according to|reports say|sources claim|studies show|data indicates)\b',
            'numbers': r'\b\d+(?:,\d{3})*(?:\.\d+)?\b'
        }
    
    def verify_facts(self, article_text: str, source_facts: List[str] = None) -> Dict:
        """
        Perform comprehensive fact verification on article content.
        
        Args:
            article_text: The article text to verify
            source_facts: Original facts provided for the article
            
        Returns:
            Verification report with scores and recommendations
        """
        report = {
            'overall_score': 0,
            'credibility_score': 0,
            'objectivity_score': 0,
            'source_attribution_score': 0,
            'fact_consistency_score': 0,
            'issues': [],
            'recommendations': [],
            'verified_claims': [],
            'flagged_content': [],
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Check source attribution
            source_score = self._check_source_attribution(article_text)
            report['source_attribution_score'] = source_score
            
            # Check objectivity
            objectivity_score = self._check_objectivity(article_text)
            report['objectivity_score'] = objectivity_score
            
            # Check fact consistency
            if source_facts:
                consistency_score = self._check_fact_consistency(article_text, source_facts)
                report['fact_consistency_score'] = consistency_score
            else:
                report['fact_consistency_score'] = 85  # Default if no source facts
            
            # Extract and verify claims
            claims = self._extract_claims(article_text)
            report['verified_claims'] = claims
            
            # Check for bias indicators
            bias_check = self._check_bias_indicators(article_text)
            report['flagged_content'].extend(bias_check)
            
            # Calculate overall credibility
            report['credibility_score'] = self._calculate_credibility_score(article_text)
            
            # Calculate overall score
            report['overall_score'] = self._calculate_overall_score(report)
            
            # Generate recommendations
            report['recommendations'] = self._generate_recommendations(report)
            
            logger.info(f"Fact check completed. Overall score: {report['overall_score']}")
            
        except Exception as e:
            logger.error(f"Error in fact verification: {e}")
            report['issues'].append(f"Verification error: {str(e)}")
        
        return report
    
    def _check_source_attribution(self, text: str) -> int:
        """Check quality of source attribution in the text."""
        score = 100
        
        # Look for attribution patterns
        attribution_patterns = [
            r'according to \w+',
            r'sources? (?:say|claim|report)',
            r'officials? (?:said|stated|confirmed)',
            r'spokesman? (?:said|told|announced)',
            r'in a statement',
            r'told reporters',
            r'during (?:a|an) (?:interview|press conference)'
        ]
        
        attributions_found = 0
        for pattern in attribution_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            attributions_found += len(matches)
        
        # Calculate score based on attribution frequency
        words = len(text.split())
        attribution_ratio = attributions_found / (words / 100)  # Per 100 words
        
        if attribution_ratio < 0.5:
            score -= 30
        elif attribution_ratio < 1.0:
            score -= 15
        
        # Check for vague attributions
        vague_sources = re.findall(r'\b(?:sources|officials|people)\b', text, re.IGNORECASE)
        if len(vague_sources) > attributions_found * 0.7:
            score -= 20
        
        return max(0, score)
    
    def _check_objectivity(self, text: str) -> int:
        """Check text objectivity and neutrality."""
        score = 100
        
        # Check for bias indicators
        for bias_type, words in self.bias_indicators.items():
            for word in words:
                if re.search(rf'\b{re.escape(word)}\b', text, re.IGNORECASE):
                    if bias_type in ['strongly_positive', 'strongly_negative']:
                        score -= 15
                    elif bias_type == 'loaded_language':
                        score -= 10
        
        # Check for opinion markers
        opinion_markers = [
            'i think', 'i believe', 'in my opinion', 'personally',
            'it seems', 'appears to be', 'might be', 'could be'
        ]
        
        for marker in opinion_markers:
            if marker in text.lower():
                score -= 5
        
        # Check for emotional language
        emotional_words = [
            'shocking', 'stunning', 'incredible', 'unbelievable',
            'amazing', 'devastating', 'tragic', 'wonderful'
        ]
        
        emotional_count = sum(1 for word in emotional_words if word in text.lower())
        score -= emotional_count * 3
        
        return max(0, score)
    
    def _check_fact_consistency(self, text: str, source_facts: List[str]) -> int:
        """Check consistency between article and source facts."""
        if not source_facts:
            return 85  # Default score when no facts to check
        
        score = 100
        facts_incorporated = 0
        
        for fact in source_facts:
            # Simple keyword matching (in real implementation, use more sophisticated NLP)
            fact_words = set(fact.lower().split())
            text_words = set(text.lower().split())
            
            # Check if significant portion of fact words appear in text
            overlap = len(fact_words.intersection(text_words))
            if overlap >= len(fact_words) * 0.6:  # 60% overlap threshold
                facts_incorporated += 1
        
        incorporation_ratio = facts_incorporated / len(source_facts)
        
        if incorporation_ratio < 0.5:
            score -= 40
        elif incorporation_ratio < 0.7:
            score -= 20
        elif incorporation_ratio < 0.9:
            score -= 10
        
        return max(0, score)
    
    def _extract_claims(self, text: str) -> List[Dict]:
        """Extract verifiable claims from the text."""
        claims = []
        
        # Extract statistical claims
        stats = re.findall(self.fact_check_patterns['statistics'], text)
        for stat in stats:
            claims.append({
                'type': 'statistic',
                'content': stat,
                'verifiable': True,
                'confidence': 'medium'
            })
        
        # Extract date claims
        dates = re.findall(self.fact_check_patterns['dates'], text)
        for date in dates:
            claims.append({
                'type': 'date',
                'content': date,
                'verifiable': True,
                'confidence': 'high'
            })
        
        # Extract quoted statements
        quotes = re.findall(self.fact_check_patterns['quotes'], text)
        for quote in quotes:
            claims.append({
                'type': 'quote',
                'content': quote,
                'verifiable': False,  # Quotes are harder to verify
                'confidence': 'low'
            })
        
        # Extract attributed claims
        attributed_claims = re.findall(
            r'according to [^,]+,?\s*([^.]+)', 
            text, 
            re.IGNORECASE
        )
        for claim in attributed_claims:
            claims.append({
                'type': 'attributed_claim',
                'content': claim.strip(),
                'verifiable': True,
                'confidence': 'medium'
            })
        
        return claims
    
    def _check_bias_indicators(self, text: str) -> List[Dict]:
        """Identify potential bias indicators in the text."""
        flagged_content = []
        
        # Check for loaded language
        for bias_type, indicators in self.bias_indicators.items():
            for indicator in indicators:
                pattern = rf'\b{re.escape(indicator)}\b'
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    flagged_content.append({
                        'type': 'bias_indicator',
                        'subtype': bias_type,
                        'content': match.group(),
                        'position': match.start(),
                        'severity': self._get_bias_severity(bias_type),
                        'suggestion': self._get_bias_alternative(indicator)
                    })
        
        # Check for unsubstantiated claims
        unsubstantiated_patterns = [
            r'everyone knows',
            r'it\'s obvious',
            r'clearly',
            r'without a doubt'
        ]
        
        for pattern in unsubstantiated_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                flagged_content.append({
                    'type': 'unsubstantiated_claim',
                    'content': match.group(),
                    'position': match.start(),
                    'severity': 'medium',
                    'suggestion': 'Provide evidence or attribution for this claim'
                })
        
        return flagged_content
    
    def _calculate_credibility_score(self, text: str) -> int:
        """Calculate overall credibility score for the text."""
        base_score = 100
        
        # Check for credible source domains (if URLs present)
        urls = re.findall(r'https?://(?:[-\w.])+(?:\.[a-zA-Z]{2,})+(?:/[^,\s]*)?', text)
        
        credible_sources_count = 0
        total_sources_count = len(urls)
        
        for url in urls:
            domain = re.search(r'https?://(?:www\.)?([^/]+)', url)
            if domain:
                domain_name = domain.group(1).lower()
                
                if any(cred_domain in domain_name for cred_domain in self.credible_sources['high_credibility']):
                    credible_sources_count += 2
                elif any(cred_domain in domain_name for cred_domain in self.credible_sources['medium_credibility']):
                    credible_sources_count += 1
                elif domain_name.endswith('.edu') or domain_name.endswith('.gov'):
                    credible_sources_count += 2
        
        # Adjust score based on source credibility
        if total_sources_count > 0:
            credibility_ratio = credible_sources_count / total_sources_count
            if credibility_ratio < 0.3:
                base_score -= 30
            elif credibility_ratio < 0.6:
                base_score -= 15
        
        # Check for verification language
        verification_phrases = [
            'verified', 'confirmed', 'corroborated',
            'independently verified', 'fact-checked'
        ]
        
        verification_count = sum(1 for phrase in verification_phrases if phrase in text.lower())
        base_score += min(verification_count * 5, 20)  # Max 20 points bonus
        
        return max(0, min(100, base_score))
    
    def _calculate_overall_score(self, report: Dict) -> int:
        """Calculate weighted overall fact-checking score."""
        weights = {
            'source_attribution_score': 0.25,
            'objectivity_score': 0.30,
            'fact_consistency_score': 0.25,
            'credibility_score': 0.20
        }
        
        weighted_score = sum(
            report[score_type] * weight
            for score_type, weight in weights.items()
        )
        
        return round(weighted_score)
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Generate improvement recommendations based on the report."""
        recommendations = []
        
        if report['source_attribution_score'] < 70:
            recommendations.append(
                "Add more specific source attributions. Use names, titles, and organizations when possible."
            )
        
        if report['objectivity_score'] < 70:
            recommendations.append(
                "Remove emotional language and opinion markers. Stick to factual reporting."
            )
        
        if report['fact_consistency_score'] < 70:
            recommendations.append(
                "Ensure all provided facts are incorporated accurately in the article."
            )
        
        if report['credibility_score'] < 70:
            recommendations.append(
                "Include more references to credible sources and verification statements."
            )
        
        if len(report['flagged_content']) > 5:
            recommendations.append(
                "Review flagged content for potential bias and replace with neutral language."
            )
        
        if report['overall_score'] < 60:
            recommendations.append(
                "Consider major revision focusing on objectivity and source verification."
            )
        
        return recommendations
    
    def _get_bias_severity(self, bias_type: str) -> str:
        """Get severity level for bias type."""
        severity_map = {
            'strongly_positive': 'high',
            'strongly_negative': 'high',
            'loaded_language': 'medium'
        }
        return severity_map.get(bias_type, 'low')
    
    def _get_bias_alternative(self, biased_word: str) -> str:
        """Suggest neutral alternative for biased language."""
        alternatives = {
            'amazing': 'notable',
            'incredible': 'significant',
            'terrible': 'concerning',
            'devastating': 'substantial',
            'obviously': 'reportedly',
            'clearly': 'according to sources'
        }
        return alternatives.get(biased_word.lower(), 'use more neutral language')
    
    def check_source_reliability(self, source_url: str) -> Dict:
        """Check the reliability of a given source URL."""
        if not source_url:
            return {'reliability': 'unknown', 'score': 50, 'category': 'unverified'}
        
        domain = re.search(r'https?://(?:www\.)?([^/]+)', source_url)
        if not domain:
            return {'reliability': 'invalid', 'score': 0, 'category': 'invalid_url'}
        
        domain_name = domain.group(1).lower()
        
        # Check against credible source lists
        if any(cred_domain in domain_name for cred_domain in self.credible_sources['high_credibility']):
            return {'reliability': 'high', 'score': 90, 'category': 'major_news_outlet'}
        
        if any(cred_domain in domain_name for cred_domain in self.credible_sources['medium_credibility']):
            return {'reliability': 'medium', 'score': 70, 'category': 'established_media'}
        
        if domain_name.endswith('.edu'):
            return {'reliability': 'high', 'score': 85, 'category': 'academic'}
        
        if domain_name.endswith('.gov'):
            return {'reliability': 'high', 'score': 95, 'category': 'government'}
        
        if domain_name.endswith('.org'):
            return {'reliability': 'medium', 'score': 60, 'category': 'organization'}
        
        return {'reliability': 'unknown', 'score': 40, 'category': 'unverified_source'}
    
    def generate_fact_check_report(self, article_data: Dict) -> str:
        """Generate a formatted fact-checking report."""
        if 'fact_check' not in article_data:
            return "No fact-checking data available."
        
        report = article_data['fact_check']
        
        formatted_report = f"""
FACT-CHECKING REPORT
==================

Article: {article_data.get('headline', 'Unknown')}
Generated: {report.get('timestamp', 'Unknown')}

OVERALL SCORE: {report['overall_score']}/100

DETAILED SCORES:
- Source Attribution: {report['source_attribution_score']}/100
- Objectivity: {report['objectivity_score']}/100
- Fact Consistency: {report['fact_consistency_score']}/100
- Credibility: {report['credibility_score']}/100

VERIFIED CLAIMS: {len(report.get('verified_claims', []))}
FLAGGED CONTENT: {len(report.get('flagged_content', []))}

RECOMMENDATIONS:
"""
        
        for i, rec in enumerate(report.get('recommendations', []), 1):
            formatted_report += f"{i}. {rec}\n"
        
        if report.get('flagged_content'):
            formatted_report += "\nFLAGGED CONTENT:\n"
            for item in report['flagged_content']:
                formatted_report += f"- {item['type']}: '{item['content']}' (Severity: {item['severity']})\n"
        
        return formatted_report
