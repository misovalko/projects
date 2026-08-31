#!/usr/bin/env python3
# Script location: scripts/web/add_pdf_sizes.py
"""
Add PDF file sizes to HTML links for better user experience.
"""

import re
from pathlib import Path

def format_size(bytes):
    """Format bytes to human-readable size."""
    if bytes >= 1048576:  # 1MB
        return f"{bytes/1048576:.1f}MB"
    else:
        return f"{bytes/1024:.0f}KB"

def add_pdf_sizes_to_html():
    """Add PDF file sizes to all PDF links in HTML."""
    html_path = Path(__file__).parent.parent.parent / "index.html"
    slides_base = Path(__file__).parent.parent.parent / "materials" / "slides"

    if not html_path.exists():
        # Fallback to absolute if relative fails
        html_path = Path('/Users/michalvalko/Documents/GitHub/misovalko.github.io/mva/index.html')
        slides_base = Path('/Users/michalvalko/Documents/GitHub/misovalko.github.io/mva/materials/slides')

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Pattern: <strong><a href="materials/slides/X/file.pdf">Title</a></strong>
    pattern = r'(<strong><a href="materials/slides/([^"]+\.pdf)">([^<]+)</a></strong>)'

    def replace_with_size(match):
        full_match = match.group(1)
        pdf_path = match.group(2)
        title = match.group(3)

        # Get file size
        pdf_full_path = slides_base / pdf_path
        if pdf_full_path.exists():
            size_bytes = pdf_full_path.stat().st_size
            size_str = format_size(size_bytes)
            # Add size in a subtle way
            return f'<strong><a href="materials/slides/{pdf_path}">{title}</a> <span class="pdf-size">({size_str})</span></strong>'
        else:
            print(f"Warning: {pdf_path} not found")
            return full_match

    html_updated = re.sub(pattern, replace_with_size, html)

    # Add CSS for pdf-size class if not already present
    if '.pdf-size' not in html_updated:
        css_addition = """        .pdf-size {
            color: #94a3b8;
            font-size: 0.85em;
            font-weight: normal;
        }
"""
        # Insert before closing </style> tag if present, else ignore (assuming external CSS)
        if '    </style>' in html_updated:
            html_updated = html_updated.replace('    </style>', css_addition + '    </style>')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_updated)

    print("✓ Added PDF file sizes to HTML links")

if __name__ == '__main__':
    add_pdf_sizes_to_html()
