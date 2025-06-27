import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os

logger = logging.getLogger(__name__)

def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def create_directories(dirs: List[str]) -> None:
    """Create directories if they don't exist."""
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        # Create subdirectories for each style
        if dir_path == 'sample_articles':
            for style in ['news', 'blog', 'social', 'newsletter']:
                os.makedirs(os.path.join(dir_path, style), exist_ok=True)

def save_article(article_data: Dict, style: str, topic: str) -> str:
    """Save article to appropriate directory and return filename."""
    try:
        # Create safe filename from topic
        safe_filename = "".join(c if c.isalnum() or c in ' -_' else '' for c in topic)
        safe_filename = safe_filename.replace(' ', '_').lower()[:50]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_filename}_{timestamp}.json"
        
        # Create style-specific directory
        style_dir = os.path.join('sample_articles', style)
        os.makedirs(style_dir, exist_ok=True)
        
        filepath = os.path.join(style_dir, filename)
        
        # Save article data
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Article saved to {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error saving article: {e}")
        return ""

def load_sample_topics() -> List[Dict]:
    """Load sample topics for article generation."""
    return [
        {
            'headline': "Major Tech Company Announces Revolutionary AI Breakthrough",
            'facts': [
                "Company developed new language model with 500 billion parameters",
                "Model shows 40% improvement in accuracy over previous versions",
                "Technology will be integrated into consumer products next year",
                "Research team spent three years developing the breakthrough",
                "Initial testing shows promising results for healthcare applications"
            ],
            'quotes': [
                {
                    'quote': "This represents a fundamental shift in how we approach artificial intelligence",
                    'speaker': "Dr. Sarah Chen",
                    'title': "Chief Technology Officer"
                },
                {
                    'quote': "We believe this technology will democratize access to advanced AI capabilities",
                    'speaker': "Mark Rodriguez",
                    'title': "CEO"
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
                "Teachers completed 40 hours of specialized training",
                "Program expected to reach 3,000 students in first year"
            ],
            'quotes': [
                {
                    'quote': "We're preparing our students for the jobs of tomorrow",
                    'speaker': "Jennifer Walsh",
                    'title': "Superintendent"
                },
                {
                    'quote': "The kids are absolutely loving the hands-on learning experience",
                    'speaker': "Michael Thompson",
                    'title': "Fourth-grade teacher"
                }
            ],
            'location': "Springfield",
            'category': "Education"
        },
        {
            'headline': "Climate Change Study Reveals Alarming Arctic Ice Loss",
            'facts': [
                "Arctic sea ice declining at rate of 13% per decade",
                "Study analyzed satellite data from past 40 years",
                "Summer ice coverage now 50% less than 1980 levels",
                "Research conducted by international team of 50 scientists",
                "Findings published in Nature Climate Change journal"
            ],
            'quotes': [
                {
                    'quote': "The rate of change is unprecedented in recorded history",
                    'speaker': "Dr. Emma Larsen",
                    'title': "Lead researcher at Arctic Institute"
                },
                {
                    'quote': "We need immediate action to prevent catastrophic consequences",
                    'speaker': "Prof. James Liu",
                    'title': "Climate scientist"
                }
            ],
            'location': "Copenhagen",
            'category': "Environment"
        },
        {
            'headline': "Professional Basketball Team Trades Star Player",
            'facts': [
                "Five-time All-Star player traded to rival team",
                "Deal includes two draft picks and $15 million",
                "Player averaged 28 points per game last season",
                "Trade deadline deal completed minutes before cutoff",
                "Team rebuilding around younger players"
            ],
            'quotes': [
                {
                    'quote': "This was a difficult but necessary decision for our future",
                    'speaker': "Tom Bradley",
                    'title': "General Manager"
                },
                {
                    'quote': "I'm excited for this new chapter in my career",
                    'speaker': "Marcus Johnson",
                    'title': "Traded player"
                }
            ],
            'location': "Chicago",
            'category': "Sports"
        },
        {
            'headline': "City Council Approves Major Infrastructure Investment",
            'facts': [
                "Council approved $50 million infrastructure package",
                "Funds will repair 200 miles of roads and bridges",
                "Project expected to create 500 construction jobs",
                "Work scheduled to begin in spring 2025",
                "Federal grants cover 60% of project costs"
            ],
            'quotes': [
                {
                    'quote': "This investment will improve safety and economic growth",
                    'speaker': "Mayor Patricia Davis",
                    'title': "City Mayor"
                },
                {
                    'quote': "These repairs are long overdue for our community",
                    'speaker': "Councilman Robert Kim",
                    'title': "District 4 Representative"
                }
            ],
            'location': "Metro City",
            'category': "Politics"
        },
        {
            'headline': "Pharmaceutical Company Reports Breakthrough in Cancer Treatment",
            'facts': [
                "New immunotherapy drug shows 80% success rate in trials",
                "Treatment effective against multiple cancer types",
                "Phase 3 trials involved 2,000 patients worldwide",
                "FDA approval expected within 18 months",
                "Drug targets specific protein found in tumor cells"
            ],
            'quotes': [
                {
                    'quote': "This could revolutionize cancer treatment as we know it",
                    'speaker': "Dr. Rachel Martinez",
                    'title': "Oncology researcher"
                },
                {
                    'quote': "We're hopeful this will save countless lives",
                    'speaker': "David Park",
                    'title': "Company spokesperson"
                }
            ],
            'location': "Boston",
            'category': "Health"
        },
        {
            'headline': "Historic Downtown Building Restored to Former Glory",
            'facts': [
                "100-year-old courthouse underwent $8 million renovation",
                "Project preserved original architecture and details",
                "Building will house new community center and museum",
                "Restoration took 18 months to complete",
                "Funded through public-private partnership"
            ],
            'quotes': [
                {
                    'quote': "This building represents our city's rich heritage",
                    'speaker': "Anna Rodriguez",
                    'title': "Historical Society President"
                },
                {
                    'quote': "The craftsmanship in this restoration is exceptional",
                    'speaker': "Bill Murphy",
                    'title': "Project architect"
                }
            ],
            'location': "Heritage City",
            'category': "Community"
        },
        {
            'headline': "International Trade Agreement Reaches Final Negotiations",
            'facts': [
                "Agreement covers trade between six nations",
                "Deal expected to increase GDP by 2% for participating countries",
                "Negotiations lasted 14 months across multiple continents",
                "Agreement includes environmental protection clauses",
                "Final signing ceremony scheduled for next month"
            ],
            'quotes': [
                {
                    'quote': "This agreement benefits workers and businesses in all our nations",
                    'speaker': "Ambassador Susan Wright",
                    'title': "Chief trade negotiator"
                },
                {
                    'quote': "We've created a framework for sustainable economic growth",
                    'speaker': "Minister Carlos Vega",
                    'title': "Foreign affairs representative"
                }
            ],
            'location': "Geneva",
            'category': "International"
        },
        {
            'headline': "Tech Startup Develops Renewable Energy Storage Solution",
            'facts': [
                "Company created battery system with 300% longer life",
                "Technology uses recycled materials for sustainability",
                "System can store solar energy for up to 72 hours",
                "Startup raised $25 million in Series A funding",
                "First commercial installations planned for 2025"
            ],
            'quotes': [
                {
                    'quote': "This technology solves the intermittency problem with renewables",
                    'speaker': "Lisa Chang",
                    'title': "Founder and CEO"
                },
                {
                    'quote': "We're seeing tremendous interest from utility companies",
                    'speaker': "Alex Thompson",
                    'title': "VP of Business Development"
                }
            ],
            'location': "Austin",
            'category': "Business"
        },
        {
            'headline': "Documentary Film Festival Showcases Environmental Activism",
            'facts': [
                "Festival featured 45 films from 20 countries",
                "Event attracted over 10,000 attendees during five-day run",
                "Films focused on climate change and conservation efforts",
                "Festival raised $100,000 for environmental organizations",
                "Next year's festival already planning international expansion"
            ],
            'quotes': [
                {
                    'quote': "Film has the power to inspire real environmental action",
                    'speaker': "Maria Santos",
                    'title': "Festival director"
                },
                {
                    'quote': "These stories need to be told to create awareness",
                    'speaker': "Ahmed Hassan",
                    'title': "Featured filmmaker"
                }
            ],
            'location': "Portland",
            'category': "Entertainment"
        },
        {
            'headline': "Agricultural Innovation Increases Crop Yields by 35%",
            'facts': [
                "New farming technique developed by university researchers",
                "Method combines precision agriculture with AI monitoring",
                "Pilot program tested on 500 farms across three states",
                "Technique reduces water usage by 40% while increasing yields",
                "Technology will be available to farmers nationwide next season"
            ],
            'quotes': [
                {
                    'quote': "This innovation could help feed a growing global population",
                    'speaker': "Dr. Kevin O'Brien",
                    'title': "Agricultural researcher"
                },
                {
                    'quote': "We're seeing remarkable results across different crop types",
                    'speaker': "Sarah Johnson",
                    'title': "Farm technology specialist"
                }
            ],
            'location': "Des Moines",
            'category': "Agriculture"
        },
        {
            'headline': "Virtual Reality Therapy Shows Promise for PTSD Treatment",
            'facts': [
                "Clinical trial involved 150 veterans with PTSD",
                "VR therapy showed 70% improvement in symptoms",
                "Treatment sessions lasted 45 minutes twice weekly",
                "Technology simulates controlled exposure therapy",
                "VA hospitals plan to implement program nationwide"
            ],
            'quotes': [
                {
                    'quote': "VR therapy offers a safe space for healing and recovery",
                    'speaker': "Dr. Amanda Foster",
                    'title': "Clinical psychologist"
                },
                {
                    'quote': "This technology gave me my life back",
                    'speaker': "Veteran John Martinez",
                    'title': "Program participant"
                }
            ],
            'location': "San Diego",
            'category': "Healthcare"
        },
        {
            'headline': "Space Mission Discovers Water Ice on Distant Moon",
            'facts': [
                "Probe detected water ice deposits beneath moon's surface",
                "Discovery made during 18-month exploration mission",
                "Water ice covers approximately 15% of moon's polar regions",
                "Finding supports potential for future human exploration",
                "Data collected from 500 surface measurements"
            ],
            'quotes': [
                {
                    'quote': "This discovery opens new possibilities for space exploration",
                    'speaker': "Dr. Patricia Williams",
                    'title': "Mission director"
                },
                {
                    'quote': "Water is essential for sustainable human presence in space",
                    'speaker': "Commander Robert Taylor",
                    'title': "Astronaut"
                }
            ],
            'location': "Houston",
            'category': "Science"
        },
        {
            'headline': "Community Garden Initiative Transforms Vacant Lots",
            'facts': [
                "Program converted 25 vacant lots into productive gardens",
                "Initiative provides fresh produce to 500 local families",
                "Volunteers contributed over 2,000 hours of work",
                "Gardens produced 10,000 pounds of vegetables last year",
                "Program expanding to neighboring cities"
            ],
            'quotes': [
                {
                    'quote': "These gardens are bringing our community together",
                    'speaker': "Carmen Rodriguez",
                    'title': "Program coordinator"
                },
                {
                    'quote': "My kids are learning where their food really comes from",
                    'speaker': "Parent volunteer Janet Kim",
                    'title': "Community member"
                }
            ],
            'location': "Detroit",
            'category': "Community"
        },
        {
            'headline': "Artificial Intelligence Helps Predict Natural Disasters",
            'facts': [
                "AI system analyzes weather patterns and seismic data",
                "Technology can predict earthquakes 72 hours in advance",
                "System achieved 85% accuracy in recent testing",
                "International disaster agencies plan to adopt technology",
                "Research funded by $10 million government grant"
            ],
            'quotes': [
                {
                    'quote': "Early warning systems save lives and property",
                    'speaker': "Dr. Yuki Tanaka",
                    'title': "Seismology expert"
                },
                {
                    'quote': "AI is revolutionizing how we prepare for natural disasters",
                    'speaker': "Emergency coordinator Mike Davis",
                    'title': "FEMA representative"
                }
            ],
            'location': "Los Angeles",
            'category': "Technology"
        }
    ]

def create_style_guide_templates() -> Dict[str, str]:
    """Create style guide templates for different formats."""
    return {
        'ap_style_guide': """
AP STYLE GUIDE FOR NEWS ARTICLES
================================

1. DATELINES
   - Use city name in ALL CAPS followed by state abbreviation
   - Format: WASHINGTON - Article content begins here...

2. ATTRIBUTION
   - Always attribute information to sources
   - Use "according to" or "said" for attribution
   - Include full names and titles on first reference

3. NUMBERS
   - Spell out numbers one through nine
   - Use figures for 10 and above
   - Always spell out numbers that begin sentences

4. DATES AND TIMES
   - Use month abbreviations (Jan., Feb., March, April, May, June, July, Aug., Sept., Oct., Nov., Dec.)
   - Format: Jan. 15, 2025
   - Use lowercase for a.m. and p.m.

5. QUOTATIONS
   - Use quotation marks for direct quotes
   - Attribution follows the quote
   - Use single quotes for quotes within quotes

6. ABBREVIATIONS
   - Spell out states in headlines
   - Use postal abbreviations only in complete addresses
   - Avoid unnecessary abbreviations

7. CAPITALIZATION
   - Capitalize proper nouns and formal titles before names
   - Lowercase generic titles after names
   - Follow standard capitalization rules
        """,
        
        'blog_style_guide': """
BLOG WRITING STYLE GUIDE
========================

1. HEADLINES
   - Use compelling, descriptive headlines
   - Include keywords for SEO
   - Keep under 60 characters when possible

2. INTRODUCTION
   - Start with a hook to grab attention
   - Clearly state what the post will cover
   - Use bold text for emphasis

3. STRUCTURE
   - Use subheadings (H2, H3) to break up content
   - Keep paragraphs short (2-4 sentences)
   - Use bullet points and numbered lists

4. TONE
   - Conversational and engaging
   - Address readers directly using "you"
   - Show personality while maintaining professionalism

5. SEO CONSIDERATIONS
   - Include relevant keywords naturally
   - Use meta descriptions
   - Add internal and external links

6. VISUAL ELEMENTS
   - Include relevant images
   - Use pull quotes for emphasis
   - Consider infographics for data

7. CALL TO ACTION
   - End with engagement prompts
   - Encourage comments and sharing
   - Include social sharing buttons
        """,
        
        'social_media_guide': """
SOCIAL MEDIA CONTENT GUIDE
==========================

1. TWITTER/X (280 characters)
   - Lead with the most important information
   - Use relevant hashtags (2-3 maximum)
   - Include engaging questions
   - Use threads for longer stories

2. LINKEDIN (Professional)
   - Professional tone and language
   - Include industry insights
   - Use relevant professional hashtags
   - Encourage professional discussion

3. FACEBOOK (Casual)
   - More conversational tone
   - Encourage comments and shares
   - Use emojis appropriately
   - Ask questions to drive engagement

4. INSTAGRAM (Visual-first)
   - Strong visual component required
   - Use story format for breaking news
   - Include relevant hashtags
   - Use caption space for full story

5. GENERAL GUIDELINES
   - Adapt tone for each platform
   - Include clear call-to-action
   - Use platform-specific features
   - Monitor and respond to engagement
        """,
        
        'newsletter_guide': """
NEWSLETTER WRITING GUIDE
========================

1. SUBJECT LINE
   - Clear and compelling
   - Avoid spam trigger words
   - Include urgency when appropriate
   - Keep under 50 characters

2. STRUCTURE
   - Header with newsletter branding
   - Table of contents for longer newsletters
   - Clear sections with subheadings
   - Footer with contact information

3. CONTENT ORGANIZATION
   - Lead with most important story
   - Use bullet points for key information
   - Include "quick read" summaries
   - Add estimated reading times

4. TONE
   - Personal and friendly
   - Direct communication style
   - Use "you" to address readers
   - Include personal insights

5. DESIGN ELEMENTS
   - Use emojis for visual breaks
   - Include relevant images
   - Maintain consistent formatting
   - Ensure mobile responsiveness

6. ENGAGEMENT
   - Include polls or surveys
   - Add sharing buttons
   - Encourage replies
   - Include archive links
        """
    }

def validate_article_data(article_data: Dict) -> tuple:
    """Validate article data completeness and return validation results."""
    required_fields = ['headline', 'lead', 'body', 'conclusion', 'full_article']
    optional_fields = ['metadata', 'fact_check', 'quality_evaluation']
    
    missing_fields = []
    warnings = []
    
    # Check required fields
    for field in required_fields:
        if field not in article_data or not article_data[field]:
            missing_fields.append(field)
    
    # Check optional fields and warn if missing
    for field in optional_fields:
        if field not in article_data:
            warnings.append(f"Optional field '{field}' is missing")
    
    # Validate content quality
    if 'full_article' in article_data:
        word_count = len(article_data['full_article'].split())
        if word_count < 100:
            warnings.append(f"Article is very short ({word_count} words)")
        elif word_count > 2000:
            warnings.append(f"Article is very long ({word_count} words)")
    
    is_valid = len(missing_fields) == 0
    
    return is_valid, missing_fields, warnings

def format_timestamp(timestamp: str = None) -> str:
    """Format timestamp for article metadata."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return timestamp

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    # Remove or replace unsafe characters
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. "
    sanitized = "".join(c if c in safe_chars else '_' for c in filename)
    
    # Remove excessive spaces and underscores
    sanitized = ' '.join(sanitized.split())
    sanitized = sanitized.replace(' ', '_')
    
    # Limit length
    if len(sanitized) > 50:
        sanitized = sanitized[:50]
    
    return sanitized

def get_word_count_category(word_count: int) -> str:
    """Categorize article by word count."""
    if word_count < 200:
        return "Brief"
    elif word_count < 500:
        return "Short"
    elif word_count < 1000:
        return "Medium"
    elif word_count < 1500:
        return "Long"
    else:
        return "Extended"

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text for tagging."""
    import re
    from collections import Counter
    
    # Simple keyword extraction
    # Remove common words
    common_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'against',
        'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself', 'we',
        'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
        'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
        'themselves', 'what', 'which', 'who', 'whom', 'whose', 'this', 'that',
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
        'said', 'says', 'say'
    }
    
    # Extract words (3+ characters, start with letter)
    words = re.findall(r'\b[A-Za-z][A-Za-z]{2,}\b', text.lower())
    
    # Filter out common words
    keywords = [word for word in words if word not in common_words]
    
    # Count frequency and return top keywords
    word_counts = Counter(keywords)
    top_keywords = [word for word, count in word_counts.most_common(max_keywords)]
    
    return top_keywords

def create_article_summary(article_data: Dict) -> Dict:
    """Create a comprehensive summary of article data."""
    summary = {
        'headline': article_data.get('headline', 'No headline'),
        'word_count': len(article_data.get('full_article', '').split()),
        'category': get_word_count_category(len(article_data.get('full_article', '').split())),
        'timestamp': format_timestamp(article_data.get('timestamp')),
        'has_fact_check': 'fact_check' in article_data,
        'has_quality_evaluation': 'quality_evaluation' in article_data,
        'keywords': extract_keywords(article_data.get('full_article', ''), 5)
    }
    
    # Add scores if available
    if 'fact_check' in article_data:
        summary['fact_check_score'] = article_data['fact_check'].get('overall_score', 0)
    
    if 'quality_evaluation' in article_data:
        summary['quality_score'] = article_data['quality_evaluation'].get('overall_score', 0)
    
    return summary
