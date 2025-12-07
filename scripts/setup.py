#!/usr/bin/env python3
"""
Setup script to download required NLTK data and check spaCy model
"""
import nltk
import sys

def download_nltk_data():
    """Download required NLTK data"""
    print("Downloading NLTK data...")
    try:
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        print("✓ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"✗ Error downloading NLTK data: {e}")
        return False

def check_spacy_model():
    """Check if spaCy model is available"""
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✓ spaCy model 'en_core_web_sm' is available")
            return True
        except OSError:
            print("✗ spaCy model 'en_core_web_sm' not found")
            print("  Run: python -m spacy download en_core_web_sm")
            return False
    except ImportError:
        print("✗ spaCy not installed")
        return False

if __name__ == "__main__":
    print("Setting up Gothic Literature Analysis environment...\n")

    nltk_ok = download_nltk_data()
    spacy_ok = check_spacy_model()

    if nltk_ok and spacy_ok:
        print("\n✓ Setup complete!")
        sys.exit(0)
    else:
        print("\n⚠ Setup incomplete. Some features may not work.")
        sys.exit(1)
