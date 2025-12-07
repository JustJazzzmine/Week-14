#!/usr/bin/env python3
"""
Text preprocessing module
Handles tokenization, stopword removal, and bag-of-words creation
"""
import re
from collections import Counter
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure NLTK data is available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

# Try to use spaCy if available, fall back to NLTK
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        USE_SPACY = True
        print("Using spaCy for NLP processing")
    except OSError:
        USE_SPACY = False
        print("spaCy model not found, using NLTK for processing")
except ImportError:
    USE_SPACY = False
    print("spaCy not installed, using NLTK for processing")


class TextPreprocessor:
    """Preprocessor for literary texts"""

    def __init__(self, use_stopwords=True):
        """
        Initialize the preprocessor

        Args:
            use_stopwords: Whether to remove stopwords
        """
        self.use_stopwords = use_stopwords
        self.stop_words = set(stopwords.words('english')) if use_stopwords else set()

    def tokenize(self, text):
        """
        Tokenize text into words

        Args:
            text: Input text

        Returns:
            List of tokens
        """
        if USE_SPACY:
            doc = nlp(text)
            tokens = [token.text.lower() for token in doc if token.is_alpha]
        else:
            # Use NLTK tokenization
            tokens = word_tokenize(text.lower())
            # Keep only alphabetic tokens
            tokens = [t for t in tokens if t.isalpha()]

        return tokens

    def remove_stopwords(self, tokens):
        """
        Remove stopwords from token list

        Args:
            tokens: List of tokens

        Returns:
            List of tokens without stopwords
        """
        return [t for t in tokens if t not in self.stop_words]

    def lemmatize(self, tokens):
        """
        Lemmatize tokens

        Args:
            tokens: List of tokens

        Returns:
            List of lemmatized tokens
        """
        if USE_SPACY:
            # Process as text for lemmatization
            doc = nlp(" ".join(tokens))
            return [token.lemma_.lower() for token in doc if token.is_alpha]
        else:
            # NLTK doesn't have a simple lemmatizer, so we'll skip this step
            return tokens

    def create_bag_of_words(self, text):
        """
        Create bag-of-words representation

        Args:
            text: Input text

        Returns:
            Dictionary with tokens as keys and frequencies as values
        """
        # Tokenize
        tokens = self.tokenize(text)

        # Remove stopwords
        if self.use_stopwords:
            tokens = self.remove_stopwords(tokens)

        # Create frequency distribution
        bow = Counter(tokens)

        return dict(bow)

    def get_vocabulary(self, text):
        """
        Get vocabulary statistics

        Args:
            text: Input text

        Returns:
            Dictionary with vocabulary statistics
        """
        # Get all tokens (with stopwords)
        all_tokens = self.tokenize(text)

        # Get content tokens (without stopwords)
        content_tokens = self.remove_stopwords(all_tokens) if self.use_stopwords else all_tokens

        # Calculate statistics
        total_words = len(all_tokens)
        unique_words = len(set(all_tokens))
        content_words = len(content_tokens)
        unique_content_words = len(set(content_tokens))

        # Type-token ratio (lexical diversity)
        ttr = unique_words / total_words if total_words > 0 else 0
        content_ttr = unique_content_words / content_words if content_words > 0 else 0

        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'content_words': content_words,
            'unique_content_words': unique_content_words,
            'type_token_ratio': round(ttr, 4),
            'content_type_token_ratio': round(content_ttr, 4)
        }


def process_text_file(file_path, preprocessor=None):
    """
    Process a single text file

    Args:
        file_path: Path to the text file
        preprocessor: TextPreprocessor instance (creates new one if None)

    Returns:
        Dictionary with processed data
    """
    if preprocessor is None:
        preprocessor = TextPreprocessor()

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Get vocabulary statistics
    vocab_stats = preprocessor.get_vocabulary(text)

    # Create bag of words
    bow = preprocessor.create_bag_of_words(text)

    return {
        'vocabulary': vocab_stats,
        'bag_of_words': bow,
        'text_length': len(text)
    }


if __name__ == "__main__":
    # Test the preprocessor
    test_text = "The quick brown fox jumps over the lazy dog. The dog was really lazy!"

    preprocessor = TextPreprocessor()
    print("Testing preprocessor...\n")

    tokens = preprocessor.tokenize(test_text)
    print(f"Tokens: {tokens}\n")

    no_stop = preprocessor.remove_stopwords(tokens)
    print(f"Without stopwords: {no_stop}\n")

    bow = preprocessor.create_bag_of_words(test_text)
    print(f"Bag of words: {bow}\n")

    vocab = preprocessor.get_vocabulary(test_text)
    print(f"Vocabulary stats: {vocab}")
