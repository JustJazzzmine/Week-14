# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Gothic literature text corpus containing classic works from Project Gutenberg. The repository serves as a data source for text analysis, natural language processing, or literary studies.

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
