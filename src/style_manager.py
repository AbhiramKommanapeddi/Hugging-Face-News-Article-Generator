from typing import Dict, List, Optional
import re
from datetime import datetime

class StyleManager:
    """
    Manages different writing styles and formats for news articles.
    Implements AP Style Guide principles and various output formats.
    """
    
    def __init__(self):
        self.ap_style_rules = {
            'dates': r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',
            'times': r'\b(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)\b',
            'numbers': r'\b(zero|one|two|three|four|five|six|seven|eight|nine)\b',
            'states': {
                'California': 'Calif.',
                'Florida': 'Fla.',
                'New York': 'N.Y.',
                'Texas': 'Texas',  # No abbreviation for Texas
            }
        }
        
        self.style_templates = {
            'news_wire': {
                'dateline_format': '{city} ({state}) - ',
                'attribution_format': 'according to {source}',
                'paragraph_length': 'short',
                'tone': 'objective'
            },
            'blog': {
                'header_format': '# {headline}\n\n*Published on {date}*\n\n',
                'subheading_format': '## {subheading}\n\n',
                'paragraph_length': 'medium',
                'tone': 'conversational'
            },
            'social_media': {
                'character_limit': 280,
                'hashtag_format': '#{tag}',
                'mention_format': '@{handle}',
                'tone': 'engaging'
            },
            'newsletter': {
                'header_format': '📰 **{headline}**\n\n',
                'footer_format': '\n\n---\n*{newsletter_name} | {date}*',
                'paragraph_length': 'medium',
                'tone': 'friendly'
            }
        }
    
    def apply_ap_style(self, text: str) -> str:
        """Apply Associated Press style guidelines to text."""
        # Fix date format (MM/DD/YYYY to Month DD, YYYY)
        text = re.sub(
            self.ap_style_rules['dates'],
            lambda m: self._format_ap_date(m.group(1), m.group(2), m.group(3)),
            text
        )
        
        # Fix time format
        text = re.sub(
            self.ap_style_rules['times'],
            lambda m: f"{int(m.group(1))}:{m.group(2)} {m.group(3).lower()}",
            text
        )
        
        # Numbers rule: spell out one through nine
        number_words = {
            '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
            '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
        }
        
        for digit, word in number_words.items():
            text = re.sub(rf'\b{digit}\b', word, text)
        
        # State abbreviations
        for state, abbrev in self.ap_style_rules['states'].items():
            text = text.replace(state, abbrev)
        
        return text
    
    def format_news_wire(self, article_data: Dict) -> str:
        """Format article in news wire style."""
        template = self.style_templates['news_wire']
        
        # Create dateline
        dateline = self._create_dateline(article_data.get('location', 'WASHINGTON'))
        
        # Format article
        formatted_article = f"{dateline}{article_data['lead']}\n\n"
        formatted_article += f"{article_data['body']}\n\n"
        formatted_article += article_data['conclusion']
        
        # Apply AP style
        formatted_article = self.apply_ap_style(formatted_article)
        
        # Add wire service formatting
        formatted_article = self._add_wire_formatting(formatted_article, article_data)
        
        return formatted_article
    
    def format_blog_style(self, article_data: Dict) -> str:
        """Format article in blog style."""
        template = self.style_templates['blog']
        
        # Create header
        header = template['header_format'].format(
            headline=article_data['headline'],
            date=datetime.now().strftime('%B %d, %Y')
        )
        
        # Add introduction
        intro = f"**{article_data['lead']}**\n\n"
        
        # Format body with subheadings
        body_paragraphs = article_data['body'].split('\n\n')
        formatted_body = ""
        
        for i, paragraph in enumerate(body_paragraphs):
            if i % 2 == 0 and i > 0:
                subheading = self._generate_subheading(paragraph)
                formatted_body += template['subheading_format'].format(subheading=subheading)
            formatted_body += f"{paragraph}\n\n"
        
        # Add conclusion
        conclusion = f"## Final Thoughts\n\n{article_data['conclusion']}\n\n"
        
        # Combine all parts
        blog_article = header + intro + formatted_body + conclusion
        
        # Add blog-specific elements
        blog_article += self._add_blog_elements(article_data)
        
        return blog_article
    
    def format_social_media(self, article_data: Dict) -> List[Dict]:
        """Format article for social media platforms."""
        posts = []
        
        # Twitter/X format
        twitter_post = self._create_twitter_post(article_data)
        posts.append({
            'platform': 'twitter',
            'content': twitter_post,
            'character_count': len(twitter_post)
        })
        
        # LinkedIn format
        linkedin_post = self._create_linkedin_post(article_data)
        posts.append({
            'platform': 'linkedin',
            'content': linkedin_post,
            'character_count': len(linkedin_post)
        })
        
        # Facebook format
        facebook_post = self._create_facebook_post(article_data)
        posts.append({
            'platform': 'facebook',
            'content': facebook_post,
            'character_count': len(facebook_post)
        })
        
        return posts
    
    def format_newsletter(self, article_data: Dict, newsletter_name: str = "Daily News") -> str:
        """Format article for newsletter distribution."""
        template = self.style_templates['newsletter']
        
        # Create header
        header = template['header_format'].format(headline=article_data['headline'])
        
        # Add summary box
        summary = self._create_newsletter_summary(article_data)
        
        # Format content
        content = f"{article_data['lead']}\n\n{article_data['body']}\n\n{article_data['conclusion']}"
        
        # Add footer
        footer = template['footer_format'].format(
            newsletter_name=newsletter_name,
            date=datetime.now().strftime('%B %d, %Y')
        )
        
        # Combine all parts
        newsletter_article = header + summary + content + footer
        
        return newsletter_article
    
    def _format_ap_date(self, month: str, day: str, year: str) -> str:
        """Format date according to AP style."""
        month_names = {
            '1': 'Jan.', '2': 'Feb.', '3': 'March', '4': 'April',
            '5': 'May', '6': 'June', '7': 'July', '8': 'Aug.',
            '9': 'Sept.', '10': 'Oct.', '11': 'Nov.', '12': 'Dec.'
        }
        
        month_name = month_names.get(month, month)
        return f"{month_name} {int(day)}, {year}"
    
    def _create_dateline(self, location: str) -> str:
        """Create AP-style dateline."""
        location = location.upper()
        return f"{location} - "
    
    def _add_wire_formatting(self, article: str, article_data: Dict) -> str:
        """Add wire service specific formatting."""
        # Add byline
        byline = "By NEWS WIRE SERVICES\n"
        
        # Add timestamp
        timestamp = f"Published: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n"
        
        # Add word count
        word_count = f"({article_data['metadata']['word_count']} words)\n\n"
        
        return byline + timestamp + word_count + article
    
    def _generate_subheading(self, paragraph: str) -> str:
        """Generate a subheading from paragraph content."""
        # Extract first meaningful phrase
        sentences = paragraph.split('.')
        if sentences:
            first_sentence = sentences[0].strip()
            # Take first 3-5 words as subheading
            words = first_sentence.split()[:4]
            return ' '.join(words).title()
        return "Key Point"
    
    def _add_blog_elements(self, article_data: Dict) -> str:
        """Add blog-specific elements like tags and sharing."""
        elements = ""
        
        # Add tags
        if article_data['metadata'].get('tags'):
            tags = ', '.join([f"#{tag}" for tag in article_data['metadata']['tags']])
            elements += f"**Tags:** {tags}\n\n"
        
        # Add reading time
        word_count = article_data['metadata']['word_count']
        reading_time = max(1, word_count // 200)  # Average 200 words per minute
        elements += f"**Reading time:** {reading_time} minute{'s' if reading_time != 1 else ''}\n\n"
        
        # Add sharing prompt
        elements += "---\n\n*Did you find this article helpful? Share it with your network!*\n"
        
        return elements
    
    def _create_twitter_post(self, article_data: Dict) -> str:
        """Create Twitter/X optimized post."""
        headline = article_data['headline']
        
        # Truncate headline if too long
        if len(headline) > 200:
            headline = headline[:197] + "..."
        
        # Add hashtags
        tags = article_data['metadata'].get('tags', [])[:2]  # Max 2 tags for Twitter
        hashtags = ' '.join([f"#{tag}" for tag in tags])
        
        post = f"{headline}\n\n{hashtags}\n\n#News #Breaking"
        
        # Ensure under character limit
        if len(post) > 280:
            # Trim headline further
            available_chars = 280 - len(hashtags) - 20  # Buffer for hashtags and spacing
            headline = headline[:available_chars-3] + "..."
            post = f"{headline}\n\n{hashtags}\n\n#News"
        
        return post
    
    def _create_linkedin_post(self, article_data: Dict) -> str:
        """Create LinkedIn optimized post."""
        headline = article_data['headline']
        lead = article_data['lead']
        
        # Create professional format
        post = f"📈 {headline}\n\n"
        post += f"{lead}\n\n"
        post += "Key insights from this development:\n"
        
        # Add bullet points from facts if available
        facts = article_data.get('facts', [])[:3]
        for fact in facts:
            post += f"• {fact}\n"
        
        post += "\nWhat are your thoughts on this development?\n\n"
        
        # Add professional hashtags
        tags = article_data['metadata'].get('tags', [])
        professional_hashtags = ' '.join([f"#{tag}" for tag in tags[:3]])
        post += f"{professional_hashtags} #Business #News #Industry"
        
        return post
    
    def _create_facebook_post(self, article_data: Dict) -> str:
        """Create Facebook optimized post."""
        headline = article_data['headline']
        lead = article_data['lead']
        
        # Create engaging format
        post = f"🔥 {headline}\n\n"
        post += f"{lead}\n\n"
        post += "This story is developing... What do you think about this?\n\n"
        post += "Share your thoughts in the comments! 👇"
        
        return post
    
    def _create_newsletter_summary(self, article_data: Dict) -> str:
        """Create newsletter summary box."""
        summary = "📋 **Quick Summary**\n\n"
        
        # Add key points
        facts = article_data.get('facts', [])[:3]
        for i, fact in enumerate(facts, 1):
            summary += f"{i}. {fact}\n"
        
        summary += f"\n**Read time:** {max(1, article_data['metadata']['word_count'] // 200)} minutes\n\n"
        summary += "---\n\n"
        
        return summary
    
    def validate_style_compliance(self, article: str, style: str) -> Dict:
        """Validate article compliance with style guidelines."""
        compliance_report = {
            'style': style,
            'issues': [],
            'score': 100,
            'suggestions': []
        }
        
        if style == 'news_wire':
            compliance_report = self._validate_ap_style(article, compliance_report)
        elif style == 'blog':
            compliance_report = self._validate_blog_style(article, compliance_report)
        elif style == 'social_media':
            compliance_report = self._validate_social_style(article, compliance_report)
        elif style == 'newsletter':
            compliance_report = self._validate_newsletter_style(article, compliance_report)
        
        return compliance_report
    
    def _validate_ap_style(self, article: str, report: Dict) -> Dict:
        """Validate AP style compliance."""
        # Check for common AP style violations
        
        # Check for Oxford comma (AP doesn't use it)
        if re.search(r',\s+and\s+\w+', article):
            report['issues'].append("Oxford comma usage detected (AP style avoids)")
            report['score'] -= 5
        
        # Check for proper state abbreviations
        full_states = ['California', 'Florida', 'New York']
        for state in full_states:
            if state in article and state not in ['Texas']:  # Texas doesn't abbreviate
                report['issues'].append(f"Use abbreviated form for {state}")
                report['score'] -= 3
        
        # Check for numbers written as digits instead of words
        digit_pattern = r'\b[1-9]\b'
        if re.search(digit_pattern, article):
            report['issues'].append("Spell out numbers one through nine")
            report['score'] -= 5
        
        return report
    
    def _validate_blog_style(self, article: str, report: Dict) -> Dict:
        """Validate blog style compliance."""
        # Check for subheadings
        if not re.search(r'^##\s+', article, re.MULTILINE):
            report['issues'].append("Blog should include subheadings")
            report['score'] -= 10
            report['suggestions'].append("Add ## subheadings to break up content")
        
        # Check for engaging elements
        if not re.search(r'[!?]', article):
            report['issues'].append("Blog could be more engaging")
            report['score'] -= 5
            report['suggestions'].append("Add questions or exclamations for engagement")
        
        return report
    
    def _validate_social_style(self, article: str, report: Dict) -> Dict:
        """Validate social media style compliance."""
        # Check character count for Twitter
        if len(article) > 280:
            report['issues'].append(f"Content too long for Twitter ({len(article)} chars)")
            report['score'] -= 20
            report['suggestions'].append("Reduce content to fit Twitter's 280 character limit")
        
        # Check for hashtags
        if not re.search(r'#\w+', article):
            report['issues'].append("No hashtags found")
            report['score'] -= 10
            report['suggestions'].append("Add relevant hashtags for better reach")
        
        return report
    
    def _validate_newsletter_style(self, article: str, report: Dict) -> Dict:
        """Validate newsletter style compliance."""
        # Check for clear structure
        if not re.search(r'📰|📋', article):
            report['issues'].append("Newsletter missing visual elements")
            report['score'] -= 5
            report['suggestions'].append("Add emojis and visual breaks")
        
        # Check for personal tone
        if not re.search(r'\byou\b|\byour\b', article, re.IGNORECASE):
            report['issues'].append("Newsletter could be more personal")
            report['score'] -= 5
            report['suggestions'].append("Use 'you' and 'your' for personal connection")
        
        return report
