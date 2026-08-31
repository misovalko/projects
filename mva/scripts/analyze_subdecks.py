#!/usr/bin/env python3
"""Analyze all subdeck LaTeX files for duplicates, inconsistencies, and improvements."""

import re
from pathlib import Path
from collections import defaultdict

def extract_frames(content):
    """Extract frame titles and content from LaTeX."""
    frames = []
    # Match \begin{frame} ... \end{frame} blocks
    frame_pattern = r'\\begin\{frame\}.*?\\frametitle\{([^}]+)\}.*?\\end\{frame\}'
    matches = re.finditer(frame_pattern, content, re.DOTALL)
    for match in matches:
        title = match.group(1).strip()
        frame_content = match.group(0)
        frames.append((title, frame_content))
    return frames

def extract_definitions(content):
    """Extract common definitions and theorems."""
    definitions = {}
    
    # Graph Laplacian definition
    if '\\bL = \\bD - \\bW' in content or 'L = D - W' in content:
        definitions['laplacian_def'] = True
    
    # Eigenvalue/eigenvector review
    if re.search(r'Review.*[Ee]igen', content):
        definitions['eigen_review'] = True
    
    # Properties of Laplacian
    if re.search(r'Properties.*[Ll]aplacian', content):
        definitions['laplacian_props'] = True
    
    # Normalized Laplacians
    if '\\bL_{sym}' in content or 'L_{sym}' in content:
        definitions['normalized_laplacian'] = True
    
    # Administrivia frames
    if 'Administrivia' in content or '\\frametitle.*Administrivia' in content:
        definitions['administrivia'] = True
    
    return definitions

def analyze_file(filepath):
    """Analyze a single subdeck file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    frames = extract_frames(content)
    definitions = extract_definitions(content)
    
    # Check for TikZ settings
    has_tikz_settings = '\\tikzset{' in content
    
    # Check for custom commands
    custom_commands = re.findall(r'\\newcommand\{([^}]+)\}', content)
    
    # Check credits/attribution
    credits = re.findall(r'\\newcommand\{\\misoclasstinytitleslide\}\{([^}]+)\}', content)
    
    return {
        'file': filepath.name,
        'path': str(filepath),
        'frames': frames,
        'definitions': definitions,
        'has_tikz_settings': has_tikz_settings,
        'custom_commands': custom_commands,
        'credits': credits,
        'num_frames': len(frames),
        'content_length': len(content)
    }

def main():
    base_dir = Path(__file__).parent.parent / "materials" / "slides"
    
    # Find all subdeck files
    subdeck_files = []
    for lecture_dir in sorted(base_dir.glob("[0-9]")):
        for tex_file in lecture_dir.glob("mlgraphs-*.tex"):
            subdeck_files.append(tex_file)
    
    print(f"Found {len(subdeck_files)} subdeck files\n")
    print("=" * 80)
    
    # Analyze all files
    analyses = []
    all_definitions = defaultdict(list)
    all_frame_titles = defaultdict(list)
    
    for filepath in sorted(subdeck_files):
        analysis = analyze_file(filepath)
        analyses.append(analysis)
        
        # Collect definitions
        for def_type, present in analysis['definitions'].items():
            if present:
                all_definitions[def_type].append(analysis['file'])
        
        # Collect frame titles
        for title, _ in analysis['frames']:
            # Normalize title (remove formatting)
            clean_title = re.sub(r'\\[a-zA-Z]+\{', '', title)
            clean_title = re.sub(r'\{|\}', '', clean_title)
            clean_title = clean_title.strip()
            all_frame_titles[clean_title].append(analysis['file'])
    
    # Report duplicates
    print("\nDUPLICATE CONTENT ANALYSIS")
    print("=" * 80)
    
    print("\n1. DEFINITIONS FOUND IN MULTIPLE FILES:")
    for def_type, files in all_definitions.items():
        if len(files) > 1:
            print(f"\n   {def_type.upper().replace('_', ' ')}:")
            for f in files:
                print(f"     - {f}")
    
    print("\n2. DUPLICATE FRAME TITLES:")
    for title, files in sorted(all_frame_titles.items()):
        if len(files) > 1 and len(title) > 10:  # Only significant titles
            print(f"\n   '{title[:60]}...':")
            for f in files:
                print(f"     - {f}")
    
    print("\n3. FILES WITH TIKZ SETTINGS (could be moved to common):")
    tikz_files = [a for a in analyses if a['has_tikz_settings']]
    for a in tikz_files:
        print(f"   - {a['file']}")
    
    print("\n4. FILES WITH ADMINISTRIVIA (should be removed):")
    admin_files = [a for a in analyses if a['definitions'].get('administrivia')]
    for a in admin_files:
        print(f"   - {a['file']}")
    
    print("\n5. INCONSISTENT CREDITS/ATTRIBUTION:")
    credits_by_file = {a['file']: a['credits'] for a in analyses if a['credits']}
    # Group by similar credits
    credit_groups = defaultdict(list)
    for file, credits in credits_by_file.items():
        # Normalize credits
        credit_str = ' '.join(credits).lower()
        credit_groups[credit_str].append(file)
    
    for credit_str, files in credit_groups.items():
        if len(files) > 1:
            print(f"\n   Similar credits in {len(files)} files:")
            for f in files[:3]:  # Show first 3
                print(f"     - {f}")
            if len(files) > 3:
                print(f"     ... and {len(files) - 3} more")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total subdecks: {len(analyses)}")
    print(f"Total frames: {sum(a['num_frames'] for a in analyses)}")
    print(f"Average frames per subdeck: {sum(a['num_frames'] for a in analyses) / len(analyses):.1f}")
    print(f"Files with Laplacian definition: {len(all_definitions.get('laplacian_def', []))}")
    print(f"Files with eigen review: {len(all_definitions.get('eigen_review', []))}")
    print(f"Files with normalized Laplacian: {len(all_definitions.get('normalized_laplacian', []))}")
    print(f"Files with Administrivia: {len(all_definitions.get('administrivia', []))}")

if __name__ == "__main__":
    main()

