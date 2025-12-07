#!/usr/bin/env python3
"""
Extract literary content from Project Gutenberg texts
Removes BOM, headers, and footers, keeping only the actual book content
"""
import os
import re
from pathlib import Path

def extract_text(file_path):
    """
    Extract the main text content from a Project Gutenberg file

    Args:
        file_path: Path to the .txt file

    Returns:
        Extracted text content
    """
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Find START and END markers
    start_pattern = r'\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK .+ \*\*\*'
    end_pattern = r'\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK .+ \*\*\*'

    start_match = re.search(start_pattern, content, re.IGNORECASE)
    end_match = re.search(end_pattern, content, re.IGNORECASE)

    if start_match and end_match:
        # Extract text between markers
        text = content[start_match.end():end_match.start()]
    else:
        print(f"Warning: Could not find START/END markers in {file_path}")
        text = content

    # Clean up the text
    text = text.strip()

    # Normalize line endings to \n
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    return text

def extract_all_texts(input_dir='.', output_dir='data/processed'):
    """
    Extract text from all .txt files in the input directory

    Args:
        input_dir: Directory containing source .txt files
        output_dir: Directory to save processed texts
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Get all .txt files
    txt_files = list(Path(input_dir).glob('*.txt'))

    # Filter out files in subdirectories
    txt_files = [f for f in txt_files if f.parent == Path(input_dir)]

    print(f"Found {len(txt_files)} text files to process\n")

    results = {}

    for txt_file in txt_files:
        print(f"Processing: {txt_file.name}")

        # Extract text
        text = extract_text(txt_file)

        # Create output filename
        output_file = Path(output_dir) / f"{txt_file.stem}_clean.txt"

        # Save extracted text
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)

        word_count = len(text.split())
        print(f"  Extracted {word_count:,} words -> {output_file.name}\n")

        results[txt_file.stem] = {
            'original': str(txt_file),
            'processed': str(output_file),
            'word_count': word_count
        }

    return results

if __name__ == "__main__":
    print("=" * 60)
    print("Gothic Literature Text Extraction")
    print("=" * 60 + "\n")

    results = extract_all_texts()

    print("\n" + "=" * 60)
    print("Extraction Complete!")
    print("=" * 60)
    print(f"\nProcessed {len(results)} texts:")
    for title, info in results.items():
        print(f"  • {title}: {info['word_count']:,} words")
