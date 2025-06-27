#!/usr/bin/env python3
"""
Setup and installation script for the Hugging Face News Article Generator.
Handles dependency installation, model downloads, and environment setup.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def print_header():
    """Print setup header."""
    print("🚀 HUGGING FACE NEWS ARTICLE GENERATOR SETUP")
    print("=" * 60)
    print("Setting up your news article generation environment...")
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")

def install_requirements():
    """Install required packages."""
    print("\n📦 Installing required packages...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        if os.path.exists("requirements.txt"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ All packages installed successfully")
        else:
            print("❌ requirements.txt not found")
            install_packages_manually()
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        print("Trying alternative installation...")
        install_packages_manually()

def install_packages_manually():
    """Install packages manually if requirements.txt fails."""
    packages = [
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "tokenizers>=0.13.0",
        "datasets>=2.10.0",
        "accelerate>=0.20.0",
        "huggingface-hub>=0.15.0",
        "gradio>=4.0.0",
        "streamlit>=1.25.0",
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "spacy>=3.4.0",
        "textstat>=0.7.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {package} - you may need to install manually")

def download_spacy_model():
    """Download spaCy language model."""
    print("\n🔤 Setting up spaCy language model...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy English model downloaded successfully")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to download spaCy model - some features may not work")
        print("   You can manually install it later with: python -m spacy download en_core_web_sm")

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating project directories...")
    
    directories = [
        "sample_articles",
        "sample_articles/news",
        "sample_articles/blog", 
        "sample_articles/social",
        "sample_articles/newsletter",
        "style_guides",
        "data",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def test_installation():
    """Test if installation was successful."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test core imports
        import torch
        import transformers
        import gradio
        import streamlit
        import spacy
        import textstat
        import pandas
        import numpy
        
        print("✅ All core packages imported successfully")
        
        # Test spaCy model
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model loaded successfully")
        except OSError:
            print("⚠️ spaCy model not found - some features may not work")
        
        # Test PyTorch
        if torch.cuda.is_available():
            print(f"✅ CUDA available - GPU acceleration enabled")
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("ℹ️ CUDA not available - using CPU (slower but functional)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def create_sample_config():
    """Create sample configuration file."""
    print("\n⚙️ Creating sample configuration...")
    
    config_content = """# News Article Generator Configuration
# Copy this to config_local.py and modify as needed

# Model settings
MODEL_CACHE_DIR = "./models"
DEFAULT_STYLE = "news"
DEFAULT_LENGTH = 500

# Output settings
OUTPUT_DIR = "./sample_articles"
SAVE_ANALYSIS = True
INCLUDE_METADATA = True

# Performance settings
USE_GPU = True  # Set to False if you don't have CUDA
BATCH_SIZE = 1
MAX_MEMORY = 0.8  # 80% of GPU memory

# Quality thresholds
MIN_QUALITY_SCORE = 70
MIN_FACT_CHECK_SCORE = 75
"""
    
    with open("config_sample.py", "w") as f:
        f.write(config_content)
    
    print("✅ Sample configuration created: config_sample.py")

def show_next_steps():
    """Show next steps after installation."""
    print("\n🎉 SETUP COMPLETE!")
    print("=" * 40)
    print()
    print("Next steps:")
    print("1. Test the CLI interface:")
    print("   python main.py --sample --count 1")
    print()
    print("2. Launch the web interface:")
    print("   streamlit run web_interface.py")
    print()
    print("3. Or try the Gradio interface:")
    print("   python gradio_interface.py")
    print()
    print("4. Run the full demo:")
    print("   python demo.py")
    print()
    print("📚 Check README.md for detailed usage instructions")
    print("🆘 If you encounter issues, check the troubleshooting section")

def troubleshooting_info():
    """Display troubleshooting information."""
    print("\n🔧 TROUBLESHOOTING TIPS")
    print("=" * 30)
    print()
    print("Common issues and solutions:")
    print()
    print("1. CUDA/GPU issues:")
    print("   - Install PyTorch with CUDA support from pytorch.org")
    print("   - Or set USE_GPU = False in config")
    print()
    print("2. Memory errors:")
    print("   - Reduce batch size or use smaller models")
    print("   - Close other applications to free up memory")
    print()
    print("3. Model download failures:")
    print("   - Check internet connection")
    print("   - Try downloading models manually")
    print()
    print("4. Package conflicts:")
    print("   - Use a virtual environment")
    print("   - Update all packages to latest versions")

def main():
    """Main setup function."""
    try:
        print_header()
        check_python_version()
        install_requirements()
        download_spacy_model()
        create_directories()
        create_sample_config()
        
        if test_installation():
            show_next_steps()
        else:
            print("\n❌ Installation test failed")
            troubleshooting_info()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        troubleshooting_info()
        sys.exit(1)

if __name__ == "__main__":
    main()
