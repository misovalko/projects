#!/usr/bin/env python3
# Script location: scripts/web/add_accessibility.py
"""
Add accessibility improvements to HTML:
- aria-labels for PDF links
- Better semantic structure
"""

import re
from pathlib import Path

def add_accessibility():
    """Add aria-labels and improve accessibility."""
    # Assuming relative path from script location (projects/mva/scripts/web)
    # index.html is at projects/mva/index.html
    html_path = Path(__file__).parent.parent.parent / "index.html"

    if not html_path.exists():
        # Fallback to absolute if relative fails (for local dev)
        html_path = Path('/Users/michalvalko/Documents/GitHub/misovalko.github.io/mva/index.html')

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Pattern: <a href="materials/slides/X/file.pdf">Title</a> <span class="pdf-size">(Size)</span>
    # Add aria-label with description
    pattern = r'<a href="materials/slides/([^"]+\.pdf)">([^<]+)</a> <span class="pdf-size">\(([^)]+)\)</span></strong>\s+<span class="subdeck-description">([^<]+)</span>'

    def add_aria_label(match):
        pdf_path = match.group(1)
        title = match.group(2)
        size = match.group(3)
        description = match.group(4)

        aria_label = f"{title}, {size} PDF. {description}"
        return f'<a href="materials/slides/{pdf_path}" aria-label="{aria_label}">{title}</a> <span class="pdf-size">({size})</span></strong>\n                                <span class="subdeck-description">{description}</span>'

    html_updated = re.sub(pattern, add_aria_label, html)

    # Add download attribute for better UX
    html_updated = re.sub(
        r'<a href="materials/slides/([^"]+\.pdf)"',
        r'<a href="materials/slides/\1" download',
        html_updated
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_updated)

    print("✓ Added accessibility improvements (aria-labels and download attributes)")

if __name__ == '__main__':
    add_accessibility()
