# Gothic Literature Text Analysis Platform

A comprehensive computational text analysis platform for exploring classic Gothic literature through distant reading techniques.

## Overview

This project combines five classic Gothic/horror novels from Project Gutenberg with advanced NLP analysis tools and an interactive web visualization interface. Using sentiment analysis, topic modeling, and lexical diversity metrics, the platform enables comparative literary analysis at scale.

## Features

- **Sentiment Analysis**: VADER-based sentiment scoring across texts
- **Topic Modeling**: LDA-based topic extraction revealing thematic patterns
- **Lexical Diversity**: Multiple metrics including TTR, Root TTR, and lexical density
- **Word Cloud Visualization**: D3-based interactive word frequency displays
- **Comparative Analysis**: Side-by-side comparison of any two texts
- **Gothic-Themed UI**: Dark, immersive interface matching the literary genre

## Texts Included

1. **Carmilla** by Joseph Sheridan Le Fanu
2. **Dracula** by Bram Stoker
3. **Frankenstein** by Mary Wollstonecraft Shelley
4. **The Strange Case of Dr. Jekyll and Mr. Hyde** by Robert Louis Stevenson
5. **The Turn of the Screw** by Henry James

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python3 scripts/setup.py
```

### 2. Run Analysis Pipeline

```bash
# Extract clean text
python3 scripts/extract_texts.py

# Run complete analysis
python3 scripts/analyze.py
```

### 3. View Results

Open `web/index.html` in your browser to explore the interactive visualization.

## Project Structure

```
├── *.txt                   # Original Project Gutenberg texts
├── data/
│   ├── processed/         # Cleaned text files
│   └── analysis_results.json
├── scripts/
│   ├── extract_texts.py   # Text extraction
│   ├── preprocess.py      # NLP preprocessing
│   └── analyze.py         # Analysis pipeline
└── web/
    ├── index.html         # Web interface
    ├── styles.css         # Gothic styling
    ├── app.js            # Visualization logic
    └── data/
        └── analysis.json  # Analysis data
```

## Technologies

- **Python**: VADER, NLTK, Gensim, spaCy
- **JavaScript**: D3.js, d3-cloud
- **Analysis**: Sentiment analysis, topic modeling, lexical statistics

## License

All texts are in the public domain (via Project Gutenberg). Analysis code is provided as-is for educational purposes.

## Documentation

See [CLAUDE.md](CLAUDE.md) for detailed architecture documentation and development guidance.
