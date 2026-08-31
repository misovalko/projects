#!/usr/bin/env python3
# Script location: scripts/maintenance/clean_comments.py
"""
Clean Commented Code from LaTeX Files
Removes large blocks of commented-out code while preserving:
- Single-line comments that appear to be documentation
- TeX directives (lines starting with % !)
- Section separators (lines with only %%%%%%)
"""

import re
import sys
from pathlib import Path

def should_keep_comment(line):
    """Determine if a comment line should be kept."""
    stripped = line.strip()

    # Keep TeX directives
    if stripped.startswith('% !'):
        return True

    # Keep section separators (only % and nothing else meaningful)
    if re.match(r'^%+\s*$', stripped):
        return True

    # Keep short documentation comments at file level
    if stripped in ['% Topic-specific title slide', '% Main content']:
        return True

    return False

def is_block_comment_start(line):
    """Check if line starts a block of commented code."""
    stripped = line.strip()
    # Lines starting with %\begin or similar LaTeX commands
    return stripped.startswith(r'%\begin') or stripped.startswith(r'%\end')

def clean_tex_file(filepath, dry_run=False):
    """Clean commented code from a tex file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    in_block_comment = False
    removed_count = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if we're entering a block comment
        if is_block_comment_start(line):
            in_block_comment = True

        # If we're in a block comment
        if in_block_comment:
            # Check if block ends (non-comment line or end of certain patterns)
            if not stripped.startswith('%'):
                in_block_comment = False
                cleaned_lines.append(line)
            else:
                removed_count += 1
                continue

        # Handle individual comment lines
        elif stripped.startswith('%'):
            if should_keep_comment(line):
                cleaned_lines.append(line)
            else:
                # Check if this starts a multi-line commented block
                # Look ahead to see if next lines are also comments
                is_multi_line = False
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('%'):
                    is_multi_line = True

                if is_multi_line:
                    removed_count += 1
                    continue
                else:
                    # Keep isolated single comments as they might be important
                    cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    if removed_count > 0:
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(cleaned_lines)
        print(f"{'[DRY RUN] ' if dry_run else ''}Cleaned {filepath.name}: removed {removed_count} comment lines")
        return removed_count

    return 0

def main():
    dry_run = '--dry-run' in sys.argv
    base_dir = Path(__file__).parent.parent.parent / "materials" / "slides"

    total_removed = 0
    files_cleaned = 0

    for tex_file in base_dir.glob('*/mlgraphs-*.tex'):
        removed = clean_tex_file(tex_file, dry_run)
        if removed > 0:
            files_cleaned += 1
            total_removed += removed

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Files cleaned: {files_cleaned}")
    print(f"  Total lines removed: {total_removed}")

if __name__ == '__main__':
    main()
