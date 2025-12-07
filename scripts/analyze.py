#!/usr/bin/env python3
"""
Comprehensive text analysis pipeline
Includes sentiment analysis, topic modeling, and style metrics
"""
import json
from pathlib import Path
from collections import Counter
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gensim import corpora
from gensim.models import LdaModel
from nltk.tokenize import sent_tokenize
import nltk

from preprocess import TextPreprocessor

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)


class TextAnalyzer:
    """Comprehensive text analyzer for literary works"""

    def __init__(self):
        self.preprocessor = TextPreprocessor(use_stopwords=True)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text, sample_size=1000):
        """
        Analyze sentiment using VADER

        Args:
            text: Input text
            sample_size: Number of sentences to sample for analysis

        Returns:
            Dictionary with sentiment scores
        """
        # Split into sentences
        sentences = sent_tokenize(text)

        # Sample sentences if text is very long
        if len(sentences) > sample_size:
            step = len(sentences) // sample_size
            sentences = sentences[::step][:sample_size]

        # Analyze each sentence
        scores = {
            'positive': [],
            'negative': [],
            'neutral': [],
            'compound': []
        }

        for sentence in sentences:
            sentiment = self.sentiment_analyzer.polarity_scores(sentence)
            scores['positive'].append(sentiment['pos'])
            scores['negative'].append(sentiment['neg'])
            scores['neutral'].append(sentiment['neu'])
            scores['compound'].append(sentiment['compound'])

        # Calculate averages
        avg_scores = {
            'positive': round(float(np.mean(scores['positive'])), 4),
            'negative': round(float(np.mean(scores['negative'])), 4),
            'neutral': round(float(np.mean(scores['neutral'])), 4),
            'compound': round(float(np.mean(scores['compound'])), 4)
        }

        # Overall sentiment classification
        if avg_scores['compound'] >= 0.05:
            overall = 'positive'
        elif avg_scores['compound'] <= -0.05:
            overall = 'negative'
        else:
            overall = 'neutral'

        return {
            'scores': avg_scores,
            'overall': overall,
            'sentences_analyzed': len(sentences)
        }

    def calculate_lexical_diversity(self, text):
        """
        Calculate various lexical diversity metrics

        Args:
            text: Input text

        Returns:
            Dictionary with diversity metrics
        """
        # Get tokens
        tokens = self.preprocessor.tokenize(text)
        content_tokens = self.preprocessor.remove_stopwords(tokens)

        # Basic metrics
        total_words = len(tokens)
        unique_words = len(set(tokens))
        content_words = len(content_tokens)
        unique_content = len(set(content_tokens))

        # Type-Token Ratio
        ttr = unique_words / total_words if total_words > 0 else 0

        # Content TTR
        content_ttr = unique_content / content_words if content_words > 0 else 0

        # Root TTR (TTR / sqrt(total words))
        rttr = unique_words / np.sqrt(total_words) if total_words > 0 else 0

        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'content_words': content_words,
            'unique_content_words': unique_content,
            'type_token_ratio': round(float(ttr), 4),
            'content_ttr': round(float(content_ttr), 4),
            'root_ttr': round(float(rttr), 4),
            'lexical_density': round(float(content_words / total_words), 4) if total_words > 0 else 0
        }

    def extract_topics(self, text, num_topics=5, words_per_topic=10):
        """
        Extract topics using LDA

        Args:
            text: Input text
            num_topics: Number of topics to extract
            words_per_topic: Number of top words per topic

        Returns:
            List of topics with their top words
        """
        # Get tokens without stopwords
        tokens = self.preprocessor.tokenize(text)
        tokens = self.preprocessor.remove_stopwords(tokens)

        # Split into chunks for topic modeling (by paragraphs or chunks)
        chunk_size = 500
        chunks = []
        for i in range(0, len(tokens), chunk_size):
            chunk = tokens[i:i + chunk_size]
            if len(chunk) >= 10:  # Minimum chunk size
                chunks.append(chunk)

        if len(chunks) < num_topics:
            num_topics = max(1, len(chunks))

        # Create dictionary and corpus
        dictionary = corpora.Dictionary(chunks)

        # Filter extremes
        dictionary.filter_extremes(no_below=2, no_above=0.5)

        # Create corpus
        corpus = [dictionary.doc2bow(chunk) for chunk in chunks]

        # Train LDA model
        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=num_topics,
            random_state=42,
            passes=10,
            alpha='auto'
        )

        # Extract topics
        topics = []
        for idx in range(num_topics):
            topic_words = lda_model.show_topic(idx, topn=words_per_topic)
            topics.append({
                'topic_id': idx,
                'words': [{'word': word, 'weight': round(float(weight), 4)} for word, weight in topic_words]
            })

        return topics

    def get_word_frequencies(self, text, top_n=100):
        """
        Get top word frequencies for word cloud

        Args:
            text: Input text
            top_n: Number of top words to return

        Returns:
            Dictionary with word frequencies
        """
        # Get bag of words
        bow = self.preprocessor.create_bag_of_words(text)

        # Sort by frequency and get top N
        sorted_words = sorted(bow.items(), key=lambda x: x[1], reverse=True)[:top_n]

        return dict(sorted_words)

    def analyze_text(self, text, title="Unknown"):
        """
        Perform complete analysis on text

        Args:
            text: Input text
            title: Title of the work

        Returns:
            Dictionary with all analysis results
        """
        print(f"\nAnalyzing: {title}")
        print("-" * 60)

        # Sentiment analysis
        print("  • Running sentiment analysis...")
        sentiment = self.analyze_sentiment(text)

        # Lexical diversity
        print("  • Calculating lexical diversity...")
        lexical = self.calculate_lexical_diversity(text)

        # Topic modeling
        print("  • Extracting topics...")
        topics = self.extract_topics(text)

        # Word frequencies
        print("  • Generating word frequencies...")
        word_freq = self.get_word_frequencies(text)

        print("  ✓ Analysis complete")

        return {
            'title': title,
            'sentiment': sentiment,
            'lexical_diversity': lexical,
            'topics': topics,
            'word_frequencies': word_freq
        }


def analyze_all_texts(input_dir='data/processed', output_file='data/analysis_results.json'):
    """
    Analyze all processed texts

    Args:
        input_dir: Directory containing processed texts
        output_file: Path to save results

    Returns:
        Dictionary with all analysis results
    """
    analyzer = TextAnalyzer()

    # Get all processed text files (skip requirements.txt)
    text_files = list(Path(input_dir).glob('*_clean.txt'))
    text_files = [f for f in text_files if 'requirements' not in f.stem.lower()]

    print("=" * 60)
    print("Gothic Literature Analysis Pipeline")
    print("=" * 60)
    print(f"\nFound {len(text_files)} texts to analyze")

    results = {}

    for text_file in text_files:
        # Read text
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Extract title from filename
        title = text_file.stem.replace('_clean', '')

        # Analyze
        analysis = analyzer.analyze_text(text, title)
        results[title] = analysis

    # Save results
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Analysis Complete! Results saved to: {output_file}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    results = analyze_all_texts()

    # Print summary
    print("\nSummary:")
    print("-" * 60)
    for title, analysis in results.items():
        sentiment = analysis['sentiment']['overall']
        compound = analysis['sentiment']['scores']['compound']
        words = analysis['lexical_diversity']['total_words']
        unique = analysis['lexical_diversity']['unique_words']
        ttr = analysis['lexical_diversity']['type_token_ratio']

        print(f"\n{title}:")
        print(f"  Words: {words:,} | Unique: {unique:,} | TTR: {ttr}")
        print(f"  Sentiment: {sentiment} (compound: {compound})")
