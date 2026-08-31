#!/usr/bin/env python3
# Script location: scripts/build/generate_thumbnails.py
"""
Generate thumbnail images for PDF slides using Ghostscript.
"""

import subprocess
from pathlib import Path
import sys

THUMB_DIR = Path('/Users/michalvalko/Documents/GitHub/misovalko.github.io/mva/materials/lectures/thumbnails')
THUMB_DIR.mkdir(exist_ok=True, parents=True)

def generate_thumbnail(pdf_path, output_path):
    """Generate thumbnail using Ghostscript."""
    try:
        # Use Ghostscript to render first page as JPEG
        subprocess.run([
            'gs',
            '-dSAFER',
            '-dBATCH',
            '-dNOPAUSE',
            '-sDEVICE=jpeg',
            '-dFirstPage=1',
            '-dLastPage=1',
            '-r150',  # 150 DPI
            '-dJPEGQ=85',
            '-g450x600',  # Width x Height (approx 300px width at standard aspect)
            f'-sOutputFile={output_path}',
            str(pdf_path)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    base_dir = Path(__file__).parent.parent.parent / "materials" / "slides"
    count = 0

    print("=== Generating Slide Thumbnails ===\n")

    # Generate thumbnails for main lecture files
    for i in range(9):
        lecture_pdf = base_dir / str(i) / f'mlgraphs{i}.pdf'
        if lecture_pdf.exists():
            thumb_path = THUMB_DIR / f'mlgraphs{i}-thumb.jpg'
            if not thumb_path.exists():
                if generate_thumbnail(lecture_pdf, thumb_path):
                    print(f"✓ Created thumbnail for mlgraphs{i}.pdf")
                    count += 1
                else:
                    print(f"✗ Failed: mlgraphs{i}.pdf")

    # Generate thumbnails for selected topic files
    for i in range(9):
        topic_dir = base_dir / str(i)
        if not topic_dir.is_dir():
            continue

        topic_pdfs = sorted(topic_dir.glob('mlgraphs-*.pdf'))
        for pdf in topic_pdfs[:3]:  # First 3 topics per lecture
            thumb_path = THUMB_DIR / f'{pdf.stem}-thumb.jpg'
            if not thumb_path.exists():
                if generate_thumbnail(pdf, thumb_path):
                    print(f"✓ Created thumbnail for {pdf.name}")
                    count += 1
                else:
                    print(f"✗ Failed: {pdf.name}")

    print(f"\n=== Summary ===")
    print(f"Generated {count} thumbnails")
    print(f"Location: {THUMB_DIR}")

if __name__ == '__main__':
    main()
