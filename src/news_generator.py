import torch
from transformers import (
    GPT2LMHeadModel, GPT2Tokenizer,
    T5ForConditionalGeneration, T5Tokenizer,
    pipeline
)
import re
import random
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsGenerator:
    """
    Core news article generation class using Hugging Face models.
    Implements inverted pyramid structure and journalism best practices.
    """
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Initialize models
        self._load_models()
        
        # Journalism templates
        self.lead_templates = [
            "{location} - {main_fact}",
            "In a {adjective} development, {main_fact}",
            "{main_fact}, according to {source}",
            "Breaking: {main_fact}"
        ]
        
        self.transition_phrases = [
            "According to sources,",
            "Officials confirmed that",
            "The development comes as",
            "In related news,",
            "Furthermore,",
            "Additionally,",
            "Meanwhile,",
            "This follows"
        ]
        
        self.quote_intros = [
            'said in a statement',
            'told reporters',
            'explained during a press conference',
            'commented on the situation',
            'stated publicly',
            'announced yesterday'
        ]
    
    def _load_models(self):
        """Load and initialize Hugging Face models."""
        try:
            # GPT-2 for text generation
            logger.info("Loading GPT-2 model...")
            self.gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
            self.gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
            self.gpt2_model.to(self.device)
            
            # Add padding token
            if self.gpt2_tokenizer.pad_token is None:
                self.gpt2_tokenizer.pad_token = self.gpt2_tokenizer.eos_token
            
            # T5 for summarization and rewriting
            logger.info("Loading T5 model...")
            self.t5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
            self.t5_model = T5ForConditionalGeneration.from_pretrained('t5-base')
            self.t5_model.to(self.device)
            
            # Pipeline for sentiment analysis
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("All models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def generate_article(
        self, 
        headline: str, 
        facts: List[str], 
        quotes: List[Dict] = None,
        style: str = "news",
        target_length: int = 500
    ) -> Dict:
        """
        Generate a complete news article with inverted pyramid structure.
        
        Args:
            headline: Article headline
            facts: List of key facts to include
            quotes: List of quotes with attribution
            style: Writing style (news, blog, social, newsletter)
            target_length: Target word count
            
        Returns:
            Dictionary containing article components
        """
        try:
            # Generate lead paragraph
            lead = self._generate_lead(headline, facts[:3] if facts else [])
            
            # Generate body paragraphs
            body = self._generate_body(facts, quotes or [])
            
            # Generate conclusion
            conclusion = self._generate_conclusion(headline, facts)
            
            # Combine article
            full_article = f"{lead}\n\n{body}\n\n{conclusion}"
            
            # Apply style formatting
            formatted_article = self._apply_style_formatting(full_article, style)
            
            # Generate metadata
            metadata = self._generate_metadata(headline, facts, formatted_article)
            
            return {
                'headline': headline,
                'lead': lead,
                'body': body,
                'conclusion': conclusion,
                'full_article': formatted_article,
                'metadata': metadata,
                'word_count': len(formatted_article.split()),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating article: {e}")
            raise
    
    def _generate_lead(self, headline: str, key_facts: List[str]) -> str:
        """Generate the lead paragraph using inverted pyramid structure."""
        if not key_facts:
            # Generate lead from headline only
            prompt = f"Write a compelling news lead paragraph for this headline: {headline}"
        else:
            # Incorporate key facts
            facts_text = " ".join(key_facts[:2])  # Use top 2 facts
            prompt = f"Write a news lead paragraph for headline '{headline}' incorporating these facts: {facts_text}"
        
        lead = self._generate_text_gpt2(prompt, max_length=150)
        
        # Clean and format lead
        lead = self._clean_generated_text(lead)
        lead = self._ensure_journalistic_tone(lead)
        
        return lead
    
    def _generate_body(self, facts: List[str], quotes: List[Dict]) -> str:
        """Generate body paragraphs with facts and quotes."""
        body_paragraphs = []
        
        # Process facts into paragraphs
        remaining_facts = facts[3:] if len(facts) > 3 else facts[1:]
        
        for i, fact in enumerate(remaining_facts):
            # Add transition phrase
            transition = random.choice(self.transition_phrases)
            
            # Generate paragraph expanding on the fact
            prompt = f"{transition} {fact}. Expand this into a detailed news paragraph."
            paragraph = self._generate_text_gpt2(prompt, max_length=120)
            paragraph = self._clean_generated_text(paragraph)
            
            body_paragraphs.append(paragraph)
            
            # Insert quotes periodically
            if quotes and i % 2 == 1 and i // 2 < len(quotes):
                quote_data = quotes[i // 2]
                quote_paragraph = self._format_quote(quote_data)
                body_paragraphs.append(quote_paragraph)
        
        return "\n\n".join(body_paragraphs)
    
    def _generate_conclusion(self, headline: str, facts: List[str]) -> str:
        """Generate a conclusion paragraph."""
        prompt = f"Write a concluding paragraph for a news article about '{headline}' that summarizes the key implications."
        
        conclusion = self._generate_text_gpt2(prompt, max_length=100)
        conclusion = self._clean_generated_text(conclusion)
        
        return conclusion
    
    def _generate_text_gpt2(self, prompt: str, max_length: int = 150) -> str:
        """Generate text using GPT-2 model."""
        try:
            inputs = self.gpt2_tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=512)
            inputs = inputs.to(self.device)
            
            with torch.no_grad():
                outputs = self.gpt2_model.generate(
                    inputs,
                    max_length=inputs.shape[1] + max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.gpt2_tokenizer.eos_token_id,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=3
                )
            
            generated_text = self.gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the original prompt
            if prompt in generated_text:
                generated_text = generated_text.replace(prompt, "").strip()
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error in GPT-2 generation: {e}")
            return f"[Generated content for: {prompt[:50]}...]"
    
    def _clean_generated_text(self, text: str) -> str:
        """Clean and format generated text for journalism standards."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Ensure proper sentence endings
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]
        
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            text = '.'.join(sentences[:-1]) + '.'
        
        return text
    
    def _ensure_journalistic_tone(self, text: str) -> str:
        """Ensure text maintains journalistic objectivity."""
        # Remove overly emotional language
        emotional_words = ['amazing', 'incredible', 'shocking', 'unbelievable']
        for word in emotional_words:
            text = re.sub(rf'\b{word}\b', 'notable', text, flags=re.IGNORECASE)
        
        return text
    
    def _format_quote(self, quote_data: Dict) -> str:
        """Format a quote with proper attribution."""
        quote = quote_data.get('quote', '')
        speaker = quote_data.get('speaker', 'a source')
        title = quote_data.get('title', '')
        
        intro = random.choice(self.quote_intros)
        
        if title:
            attribution = f"{speaker}, {title}, {intro}"
        else:
            attribution = f"{speaker} {intro}"
        
        return f'"{quote}," {attribution}.'
    
    def _apply_style_formatting(self, article: str, style: str) -> str:
        """Apply style-specific formatting."""
        if style == "news":
            return article
        elif style == "blog":
            return self._format_as_blog(article)
        elif style == "social":
            return self._format_as_social(article)
        elif style == "newsletter":
            return self._format_as_newsletter(article)
        else:
            return article
    
    def _format_as_blog(self, article: str) -> str:
        """Format article as blog post."""
        paragraphs = article.split('\n\n')
        
        # Add subheadings
        formatted_paragraphs = []
        for i, paragraph in enumerate(paragraphs):
            if i % 2 == 0 and i > 0:
                formatted_paragraphs.append(f"## Key Development\n\n{paragraph}")
            else:
                formatted_paragraphs.append(paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _format_as_social(self, article: str) -> str:
        """Format article for social media."""
        # Create a condensed version
        sentences = article.split('.')[:3]  # First 3 sentences
        condensed = '. '.join(sentences) + '.'
        
        # Add hashtags and social elements
        condensed += '\n\n#BreakingNews #News #Update'
        
        return condensed
    
    def _format_as_newsletter(self, article: str) -> str:
        """Format article for newsletter."""
        return f"📰 **Today's Update**\n\n{article}\n\n---\n*Stay informed with our daily newsletter*"
    
    def _generate_metadata(self, headline: str, facts: List[str], article: str) -> Dict:
        """Generate article metadata."""
        # Analyze sentiment
        sentiment = self.sentiment_pipeline(article[:500])[0]
        
        # Count key metrics
        word_count = len(article.split())
        sentence_count = len([s for s in article.split('.') if s.strip()])
        
        # Extract potential tags
        tags = self._extract_tags(headline + ' ' + ' '.join(facts))
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'sentiment': sentiment,
            'tags': tags,
            'readability_score': self._calculate_readability(article),
            'fact_count': len(facts)
        }
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text."""
        # Simple keyword extraction
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        tags = [word.lower() for word in words if word.lower() not in common_words]
        return list(set(tags))[:5]  # Return top 5 unique tags
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate simple readability score."""
        words = len(text.split())
        sentences = len([s for s in text.split('.') if s.strip()])
        
        if sentences == 0:
            return 0.0
        
        avg_sentence_length = words / sentences
        # Simple readability score (lower is easier to read)
        return round(avg_sentence_length, 2)
    
    def generate_multiple_articles(
        self, 
        topics: List[Dict], 
        style: str = "news"
    ) -> List[Dict]:
        """Generate multiple articles for different topics."""
        articles = []
        
        for topic in topics:
            try:
                article = self.generate_article(
                    headline=topic['headline'],
                    facts=topic.get('facts', []),
                    quotes=topic.get('quotes', []),
                    style=style
                )
                articles.append(article)
                logger.info(f"Generated article: {topic['headline']}")
                
            except Exception as e:
                logger.error(f"Failed to generate article for {topic['headline']}: {e}")
                continue
        
        return articles
