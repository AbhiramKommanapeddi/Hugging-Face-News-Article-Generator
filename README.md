# Hugging Face News Article Generator

An automated news article writer using Hugging Face models that generates professional articles from headlines and key facts.

## Features

### Core Features

- **Article Generation**: Headline expansion, fact integration, quote incorporation, conclusion writing
- **Journalism Features**: Inverted pyramid structure, source attribution, objectivity checks
- **Formatting Options**: News wire format, blog style, social media versions, newsletter format

### Bonus Features

- Multi-source synthesis
- Image caption generation
- Related article links
- Trend analysis

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download spaCy model:

```bash
python -m spacy download en_core_web_sm
```

## Usage

### Command Line Interface

```bash
python main.py --headline "Your headline here" --facts "fact1,fact2,fact3" --style "news"
```

### Web Interface

```bash
streamlit run web_interface.py
```

### Gradio Interface

```bash
python gradio_interface.py
```

## Project Structure

```
├── main.py                 # Main CLI application
├── web_interface.py        # Streamlit web interface
├── gradio_interface.py     # Gradio interface
├── src/
│   ├── news_generator.py   # Core news generation logic
│   ├── style_manager.py    # Style and format management
│   ├── fact_checker.py     # Fact verification
│   ├── quality_metrics.py  # Article quality assessment
│   └── utils.py           # Utility functions
├── templates/
│   ├── news_wire.py       # News wire format template
│   ├── blog_style.py      # Blog format template
│   ├── social_media.py    # Social media format template
│   └── newsletter.py      # Newsletter format template
├── sample_articles/       # Generated sample articles
├── style_guides/         # Style guide templates
└── data/                 # Sample data and configurations
```

## Sample Articles

The system generates 15+ sample articles covering various topics and formats:

- Breaking news
- Sports coverage
- Technology updates
- Political analysis
- Business reports
- Health and science
- Entertainment news

## Quality Metrics

- Writing Quality (40%): Professional tone, clarity, engagement
- Accuracy (25%): Fact handling and verification
- Structure (20%): Proper journalistic format
- Variety (15%): Coverage of different topics and styles

## License

MIT License
