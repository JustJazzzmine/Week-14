# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Gothic Literature Text Analysis Platform that combines a corpus of classic Gothic/horror novels from Project Gutenberg with comprehensive computational text analysis tools and an interactive web visualization interface. The project demonstrates distant reading techniques through sentiment analysis, topic modeling, lexical diversity metrics, and word cloud visualization.

## Contents

The repository contains five classic Gothic/horror novels:

- **Carmilla** by Joseph Sheridan Le Fanu (177KB)
- **Dracula** by Bram Stoker (870KB)
- **Frankenstein; Or, The Modern Prometheus** by Mary Wollstonecraft Shelley (439KB)
- **The Strange Case of Dr. Jekyll and Mr. Hyde** by Robert Louis Stevenson (160KB)
- **The Turn of the Screw** by Henry James (254KB)

## File Format

All text files are:
- UTF-8 encoded with BOM (Byte Order Mark)
- Using CRLF line terminators (Windows-style)
- Sourced from Project Gutenberg with standard headers and licensing information

## Working with the Texts

When processing these files:

1. **BOM Handling**: Files start with a UTF-8 BOM (﻿). Ensure your text processing tools handle this correctly or strip it when necessary.

2. **Line Endings**: Files use CRLF (`\r\n`). When processing on Unix-like systems, you may need to handle or convert line endings.

3. **Structure**: Each file contains:
   - Project Gutenberg header with licensing and metadata
   - `*** START OF THE PROJECT GUTENBERG EBOOK [TITLE] ***` marker
   - The actual text
   - `*** END OF THE PROJECT GUTENBERG EBOOK [TITLE] ***` marker (at the end)
   - Project Gutenberg footer

4. **Text Extraction**: To extract just the literary content, look for text between the START and END markers.

## Licensing

All texts are in the public domain in the United States and distributed under Project Gutenberg's terms. When using these texts, respect Project Gutenberg's license terms available at www.gutenberg.org.

## Project Setup

### Installing Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Download required NLTK data and check spaCy model
python3 scripts/setup.py

# Optional: Download spaCy model (if not already installed)
python3 -m spacy download en_core_web_sm
```

### Running the Analysis Pipeline

```bash
# 1. Extract clean text from Project Gutenberg files
python3 scripts/extract_texts.py

# 2. Run complete analysis (sentiment, topics, lexical diversity)
python3 scripts/analyze.py

# 3. View results in web interface
# Open web/index.html in a browser
```

## Architecture

### Project Structure

```
Week-14/
├── *.txt                      # Original Project Gutenberg texts
├── data/
│   ├── processed/            # Cleaned text files (extracted content)
│   └── analysis_results.json # Complete analysis output
├── scripts/
│   ├── setup.py             # Environment setup script
│   ├── extract_texts.py     # Text extraction from Gutenberg format
│   ├── preprocess.py        # Text preprocessing module
│   └── analyze.py           # Main analysis pipeline
└── web/
    ├── index.html           # Web interface structure
    ├── styles.css           # Gothic-themed styling
    ├── app.js              # Interactive visualization logic
    └── data/
        └── analysis.json    # Analysis data for web display
```

### Analysis Pipeline

The analysis pipeline follows a three-stage process:

1. **Text Extraction** (`extract_texts.py`)
   - Reads raw Project Gutenberg files
   - Strips BOM and normalizes line endings
   - Extracts content between START/END markers
   - Outputs cleaned texts to `data/processed/`

2. **Preprocessing** (`preprocess.py`)
   - Tokenization using NLTK (falls back from spaCy if unavailable)
   - Stopword removal using NLTK's English stopword list
   - Bag-of-words generation
   - Vocabulary statistics calculation

3. **Analysis** (`analyze.py`)
   - **Sentiment Analysis**: VADER-based scoring (positive, negative, neutral, compound)
   - **Lexical Diversity**: Type-token ratio, content TTR, root TTR, lexical density
   - **Topic Modeling**: LDA-based topic extraction with Gensim
   - **Word Frequencies**: Top 100 words per text for visualization

### Web Interface

The web interface (`web/`) provides:

- **Single Text View**: Navigate texts via sidebar, view all analysis for one text
- **Comparison Mode**: Select two texts to compare side-by-side
- **Visualizations**:
  - D3-based word clouds (rendered client-side from word frequencies)
  - Sentiment bars showing polarity scores
  - Lexical diversity metrics in card layout
  - Topic modeling results with top words per topic

### Key Technologies

- **Python**: spaCy, VADER, NLTK, Gensim for NLP/analysis
- **JavaScript**: D3.js and d3-cloud for word cloud visualization
- **Frontend**: Vanilla HTML/CSS/JS (no framework required)
- **Data Format**: JSON for analysis interchange between Python and web

### Development Workflow

When adding new texts:
1. Add `.txt` file to root directory (must be Project Gutenberg format)
2. Run `python3 scripts/extract_texts.py`
3. Run `python3 scripts/analyze.py`
4. Copy `data/analysis_results.json` to `web/data/analysis.json`
5. Refresh web interface

When modifying analysis:
- Edit `scripts/analyze.py` for new metrics
- Re-run analysis pipeline
- Update `web/app.js` to display new metrics
- Update JSON structure as needed
