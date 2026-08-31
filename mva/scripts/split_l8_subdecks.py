#!/usr/bin/env python3
"""Split L8 PDF into subdecks based on identified topics."""

import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)

# Based on PDF analysis, L8 covers:
# 1. Graph Bandits (pages 9-20): Introduction, side observations, setup
# 2. Spectral Bandits (pages 21-35): SpectralUCB, effective dimension, regret
# 3. Influence Maximization (pages 36-51): Revealing bandits, BARE algorithm

SUBDECKS = [
    {
        'name': 'graph-bandits',
        'title': 'Graph Bandits',
        'subtitle': 'Multi-Armed Bandits on Graphs with Side Observations',
        'start_page': 9,  # 0-indexed, so page 9 = index 8
        'end_page': 20,   # inclusive
        'description': 'Introduction to graph bandits, where actions are nodes on a graph and learners can observe losses of neighboring nodes. Covers the general setup, side observations, and how graph structure enables faster learning compared to standard multi-armed bandits.'
    },
    {
        'name': 'spectral-bandits',
        'title': 'Spectral Bandits',
        'subtitle': 'SpectralUCB and Effective Dimension',
        'start_page': 21,
        'end_page': 35,
        'description': 'Spectral bandits leverage graph Laplacian eigenvectors to reduce the effective dimension from N (number of nodes) to d (effective dimension). Covers SpectralUCB algorithm, effective dimension analysis, regret bounds, and experimental results on synthetic and real-world graphs (Barabási–Albert, Flixster, MovieLens).'
    },
    {
        'name': 'influence-maximization',
        'title': 'Influence Maximization',
        'subtitle': 'Revealing Graph Bandits and BARE Algorithm',
        'start_page': 36,
        'end_page': 51,
        'description': 'Influence maximization as a revealing graph bandit problem, where selecting a node reveals which neighbors it influences. Introduces the BARE (BAndit REvelator) algorithm, detectable dimension D*, and how it achieves better regret bounds by exploiting graph structure. Includes applications to social networks and empirical results.'
    }
]

def split_pdf(pdf_path, output_dir):
    """Split PDF into subdecks."""
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    print(f"Total pages in PDF: {total_pages}")
    print(f"Creating {len(SUBDECKS)} subdecks...\n")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    created_files = []
    
    for subdeck in SUBDECKS:
        name = subdeck['name']
        start = subdeck['start_page'] - 1  # Convert to 0-indexed
        end = subdeck['end_page']  # Already 1-indexed, but end is exclusive in slicing
        
        # Adjust if pages exceed PDF
        if start >= total_pages:
            print(f"Warning: {name} starts at page {start+1} but PDF only has {total_pages} pages. Skipping.")
            continue
        if end > total_pages:
            print(f"Warning: {name} ends at page {end} but PDF only has {total_pages} pages. Adjusting to {total_pages}.")
            end = total_pages
        
        # Create PDF writer
        writer = PdfWriter()
        
        # Add pages (end is exclusive in slicing)
        for page_num in range(start, end):
            writer.add_page(reader.pages[page_num])
        
        # Write output PDF
        output_path = output_dir / f"mlgraphs-{name}.pdf"
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        print(f"Created: {output_path} (pages {start+1}-{end})")
        created_files.append({
            'path': output_path,
            'subdeck': subdeck
        })
    
    return created_files

if __name__ == "__main__":
    pdf_path = Path(__file__).parent.parent / "materials" / "year-archives" / "2017-2018" / "mlgraphs8.pdf"
    output_dir = Path(__file__).parent.parent / "materials" / "slides" / "8"
    
    if not pdf_path.exists():
        print(f"Error: PDF not found at {pdf_path}")
        sys.exit(1)
    
    print(f"Splitting PDF: {pdf_path}\n")
    created_files = split_pdf(pdf_path, output_dir)
    
    print(f"\n{'='*80}")
    print("SUBDECK DESCRIPTIONS:")
    print("="*80)
    for item in created_files:
        subdeck = item['subdeck']
        print(f"\n{subdeck['name']}:")
        print(f"  Title: {subdeck['title']}")
        print(f"  Subtitle: {subdeck['subtitle']}")
        print(f"  Description: {subdeck['description']}")
        print(f"  File: {item['path'].name}")


