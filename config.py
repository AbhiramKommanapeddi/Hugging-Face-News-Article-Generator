# Configuration file for the News Article Generator

# Model Configuration
MODEL_CONFIG = {
    'gpt2_model': 'gpt2-medium',  # or 'gpt2', 'gpt2-large', 'gpt2-xl'
    't5_model': 't5-base',        # or 't5-small', 't5-large'
    'sentiment_model': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
    'device': 'auto',  # 'auto', 'cpu', 'cuda'
    'max_memory_usage': 0.8  # 80% of available GPU memory
}

# Generation Parameters
GENERATION_CONFIG = {
    'max_length': 150,
    'temperature': 0.7,
    'do_sample': True,
    'repetition_penalty': 1.2,
    'no_repeat_ngram_size': 3,
    'pad_token_id': 50256  # GPT-2 EOS token
}

# Quality Thresholds
QUALITY_THRESHOLDS = {
    'excellent': 90,
    'good': 80,
    'fair': 70,
    'poor': 60
}

# Fact Check Configuration
FACT_CHECK_CONFIG = {
    'objectivity_weight': 0.30,
    'attribution_weight': 0.25,
    'consistency_weight': 0.25,
    'credibility_weight': 0.20,
    'min_attribution_ratio': 0.02,  # 2% of words should be attribution
    'max_bias_tolerance': 5  # Maximum bias indicators allowed
}

# Style Guide Settings
STYLE_SETTINGS = {
    'news': {
        'target_grade_level': 8,
        'max_sentence_length': 25,
        'paragraph_length': (50, 150),
        'required_elements': ['who', 'what', 'when', 'where', 'why']
    },
    'blog': {
        'target_grade_level': 10,
        'max_sentence_length': 30,
        'paragraph_length': (30, 100),
        'engagement_elements': ['questions', 'subheadings', 'lists']
    },
    'social': {
        'character_limits': {
            'twitter': 280,
            'instagram': 2200,
            'facebook': 63206,
            'linkedin': 3000
        },
        'hashtag_limits': {
            'twitter': 2,
            'instagram': 10,
            'facebook': 3,
            'linkedin': 5
        }
    },
    'newsletter': {
        'target_grade_level': 9,
        'max_sentence_length': 20,
        'personal_tone': True,
        'sections': ['header', 'summary', 'content', 'cta', 'footer']
    }
}

# File Output Settings
OUTPUT_CONFIG = {
    'default_output_dir': 'sample_articles',
    'file_formats': ['json', 'txt', 'md'],
    'include_metadata': True,
    'include_analysis': True,
    'filename_template': '{category}_{timestamp}_{style}'
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_logging': True,
    'log_file': 'news_generator.log',
    'max_log_size': '10MB',
    'backup_count': 5
}

# API Configuration (for potential future integrations)
API_CONFIG = {
    'rate_limit': 100,  # requests per hour
    'timeout': 30,      # seconds
    'retry_attempts': 3,
    'retry_delay': 1    # seconds
}

# Performance Settings
PERFORMANCE_CONFIG = {
    'batch_size': 1,
    'parallel_processing': False,
    'cache_models': True,
    'cache_size': 100,  # number of cached results
    'memory_optimization': True
}
