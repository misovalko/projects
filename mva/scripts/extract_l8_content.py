#!/usr/bin/env python3
"""Extract content from L8 PDF to identify topics for subdeck creation."""

import sys
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)

def extract_pdf_content(pdf_path, output_file=None):
    """Extract text from PDF and identify slide titles/topics."""
    import warnings
    warnings.filterwarnings('ignore')
    
    reader = PdfReader(pdf_path)
    
    output_lines = []
    output_lines.append(f"Total pages: {len(reader.pages)}\n")
    output_lines.append("=" * 80)
    output_lines.append("")
    
    # Keywords that indicate major topics
    topic_keywords = [
        'graph neural network', 'gnn', 'graphnet', 'graph nets',
        'random graph', 'erdos', 'renyi', 'barabasi', 'albert',
        'link prediction', 'link classification',
        'anomaly detection', 'outlier',
        'community detection', 'community mining',
        'graph embedding', 'node embedding', 'graph representation',
        'social network', 'recommender system', 'recommendation'
    ]
    
    all_text = []
    page_titles = []
    
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        if not text:
            continue
            
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            continue
        
        all_text.append((i, text, lines))
        
        # First line often contains title
        first_line = lines[0] if lines else ""
        second_line = lines[1] if len(lines) > 1 else ""
        
        # Check if this looks like a title slide
        is_likely_title = False
        title_candidate = first_line
        
        # Check for common title patterns
        if len(first_line) < 80:
            # Check if it contains topic keywords
            first_lower = first_line.lower()
            if any(kw in first_lower for kw in topic_keywords):
                is_likely_title = True
            # Check if it's all caps or has title case
            elif first_line.isupper() or (first_line and first_line[0].isupper() and len(first_line.split()) <= 8):
                is_likely_title = True
        
        if is_likely_title or i <= 3:  # First few pages are usually title/intro
            page_titles.append((i, title_candidate, text[:500]))
        
        # Print page info
        output_lines.append(f"\n--- Page {i} ---")
        output_lines.append(f"Title candidate: {title_candidate[:80]}")
        if len(lines) > 1:
            output_lines.append(f"Second line: {lines[1][:80]}")
        output_lines.append(f"Text preview: {text[:400]}...")
        output_lines.append("")
    
    # Identify major sections
    output_lines.append("\n" + "=" * 80)
    output_lines.append("IDENTIFIED TOPIC CANDIDATES:")
    output_lines.append("=" * 80)
    
    topics = []
    for page_num, title, preview in page_titles:
        output_lines.append(f"\nPage {page_num}: {title}")
        output_lines.append(f"  Preview: {preview[:200]}...")
        
        # Try to categorize
        title_lower = title.lower()
        if any(kw in title_lower for kw in ['neural', 'gnn', 'graphnet']):
            topics.append(('Graph Neural Networks', page_num))
        elif any(kw in title_lower for kw in ['random', 'erdos', 'renyi', 'barabasi']):
            topics.append(('Random Graph Models', page_num))
        elif any(kw in title_lower for kw in ['link prediction', 'link classification']):
            topics.append(('Link Prediction', page_num))
        elif any(kw in title_lower for kw in ['anomaly', 'outlier']):
            topics.append(('Anomaly Detection', page_num))
        elif any(kw in title_lower for kw in ['community']):
            topics.append(('Community Detection', page_num))
        elif any(kw in title_lower for kw in ['embedding', 'representation']):
            topics.append(('Graph Embeddings', page_num))
        elif any(kw in title_lower for kw in ['social', 'recommender', 'recommendation']):
            topics.append(('Applications: Social Networks & Recommender Systems', page_num))
    
    output_lines.append("\n" + "=" * 80)
    output_lines.append("SUGGESTED SUBDECK TOPICS:")
    output_lines.append("=" * 80)
    
    # Deduplicate and organize topics
    seen = set()
    unique_topics = []
    for topic, page in topics:
        if topic not in seen:
            seen.add(topic)
            unique_topics.append((topic, page))
            output_lines.append(f"\n- {topic} (starts around page {page})")
    
    output_text = '\n'.join(output_lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"Output saved to: {output_file}")
    else:
        print(output_text)
    
    return unique_topics, all_text

if __name__ == "__main__":
    pdf_path = Path(__file__).parent.parent / "materials" / "year-archives" / "2017-2018" / "mlgraphs8.pdf"
    output_path = Path(__file__).parent / "l8_extraction.txt"
    
    if not pdf_path.exists():
        print(f"Error: PDF not found at {pdf_path}")
        sys.exit(1)
    
    print(f"Extracting content from: {pdf_path}\n")
    topics, all_text = extract_pdf_content(pdf_path, output_path)
    
    print(f"\nFound {len(topics)} potential topics for subdecks.")


