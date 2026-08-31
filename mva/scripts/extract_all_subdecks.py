#!/usr/bin/env python3
"""
Extract subdecks from lecture files based on frame title patterns.
"""
import re
import os
from pathlib import Path

def extract_content_between_patterns(content, start_pattern, end_pattern=None):
    """Extract content between two patterns."""
    # Escape special regex chars but keep LaTeX commands
    start_escaped = start_pattern.replace('\\', '\\\\')
    end_escaped = end_pattern.replace('\\', '\\\\') if end_pattern else None
    
    start_match = re.search(start_escaped, content)
    if not start_match:
        return None
    
    start_pos = start_match.start()
    
    if end_pattern:
        end_match = re.search(end_escaped, content[start_pos:])
        if end_match:
            end_pos = start_pos + end_match.start()
        else:
            end_pos = len(content)
    else:
        end_pos = len(content)
    
    return content[start_pos:end_pos]

def get_header(lecture_file):
    """Extract header from lecture file."""
    with open(lecture_file, 'r') as f:
        content = f.read()
    
    # Find header up to \begin{document}
    header_match = re.search(r'% !TEX TS-program.*?\\begin\{document\}', content, re.DOTALL)
    if header_match:
        return header_match.group(0)
    return None

def create_subdeck(lecture_dir, lecture_num, topic_name, topic_title, topic_subtitle,
                   start_pattern, end_pattern, credits, tikz_setup=None):
    """Create a subdeck file."""
    lecture_file = f"{lecture_dir}/mlgraphs{lecture_num}.tex"
    
    if not os.path.exists(lecture_file):
        print(f"Warning: {lecture_file} not found")
        return False
    
    with open(lecture_file, 'r') as f:
        content = f.read()
    
    # Extract frames
    frames_content = extract_content_between_patterns(content, start_pattern, end_pattern)
    if not frames_content:
        print(f"Warning: Could not find content for {topic_name} in {lecture_file}")
        return False
    
    # Get header
    header = get_header(lecture_file)
    if not header:
        header = f"""% !TEX TS-program = lualatex
\\documentclass{{beamer}}
\\input{{../common/misomva}}
\\begin{{document}}"""
    
    # Create subdeck content
    subdeck_content = header.rstrip() + "\n"
    subdeck_content += f"""% Topic-specific title slide
\\newcommand{{\\topictitle}}{{{topic_title}}}
\\newcommand{{\\topicsubtitle}}{{{topic_subtitle}}}
\\newcommand{{\\misoclasstinytitleslide}}{{{credits}}}
"""
    
    if tikz_setup:
        subdeck_content += f"{tikz_setup}\n"
    
    subdeck_content += f"""
\\input{{../common/mvamlgraphstopic1slide}}

{frames_content}

\\input{{../common/mvamlgraphslastslide}}
\\end{{document}}
"""
    
    # Write subdeck file
    subdeck_file = f"{lecture_dir}/mlgraphs-{topic_name}.tex"
    with open(subdeck_file, 'w') as f:
        f.write(subdeck_content)
    
    print(f"Created: {subdeck_file}")
    return True

# Define all subdecks configuration
LECTURE2_CREDITS = "Partially based on material by:  Ulrike von Luxburg, \\\\[-1em] Gary Miller, Doyle \\& Schnell, Daniel Spielman"
LECTURE2_TIKZ = """\\usetikzlibrary{graphs}

\\tikzset{{
  vertex/.style={{circle,fill=black!25,minimum size=20pt,inner sep=0pt}},
  selected vertex/.style={{vertex, fill=red!24}},
  edge/.style={{draw,thick,->}},
  weight/.style={{font=\\small}},
  selected edge/.style={{draw,line width=5pt,-,red!50}},
  ignored edge/.style={{draw,line width=5pt,-,black!20}}
}}"""

LECTURE1_CREDITS = "Partially based on material by:  Andreas Krause, \\\\[-1em] Branislav Kveton, Michael Kearns"

ALL_SUBDECKS = [
    # Lecture 1
    {
        "lecture_dir": "1",
        "lecture_num": "1",
        "topic_name": "introduction",
        "topic_title": "Introduction to Graphs in ML",
        "topic_subtitle": "Course Overview and Motivation",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Administrivia\}",
        "end_pattern": r"\\begin\{frame\}\s*\\frametitle\{.*Natural graphs",
        "credits": LECTURE1_CREDITS,
        "tikz_setup": None
    },
    {
        "lecture_dir": "1",
        "lecture_num": "1",
        "topic_name": "natural-graphs",
        "topic_title": "Natural Graphs",
        "topic_subtitle": "Social, Information, and Biological Networks",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Natural graphs from",
        "end_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Submodularity",
        "credits": LECTURE1_CREDITS,
        "tikz_setup": None
    },
    {
        "lecture_dir": "1",
        "lecture_num": "1",
        "topic_name": "submodularity",
        "topic_title": "Submodularity",
        "topic_subtitle": "Theory and Product Placement Application",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Submodularity",
        "end_pattern": r"\\begin\{frame\}\s*\\frametitle\{.*Google",
        "credits": LECTURE1_CREDITS,
        "tikz_setup": None
    },
    {
        "lecture_dir": "1",
        "lecture_num": "1",
        "topic_name": "pagerank",
        "topic_title": "Google PageRank",
        "topic_subtitle": "Random Surfer and Steady State",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Success story.*Google",
        "end_pattern": r"\\begin\{frame\}\s*\\frametitle\{.*Similarity",
        "credits": LECTURE1_CREDITS,
        "tikz_setup": None
    },
    {
        "lecture_dir": "1",
        "lecture_num": "1",
        "topic_name": "similarity-graphs",
        "topic_title": "Similarity Graphs",
        "topic_subtitle": "Graph Theory Refresher and Construction",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf.*Similarity",
        "end_pattern": None,
        "credits": LECTURE1_CREDITS,
        "tikz_setup": None
    },
    
    # Lecture 2 - already created similarity-graphs-construction, continue with others
    {
        "lecture_dir": "2",
        "lecture_num": "2",
        "topic_name": "graph-laplacian",
        "topic_title": "Graph Laplacian",
        "topic_subtitle": "Properties and Spectral Theory",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Graph Laplacian\}",
        "end_pattern": r"\\setbeamertemplate\{background canvas\}.*spectral clustering",
        "credits": LECTURE2_CREDITS,
        "tikz_setup": LECTURE2_TIKZ
    },
    {
        "lecture_dir": "2",
        "lecture_num": "2",
        "topic_name": "spectral-clustering",
        "topic_title": "Spectral Clustering",
        "topic_subtitle": "Theory and Applications",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Spectral Clustering: Cuts",
        "end_pattern": r"\\setbeamertemplate\{background canvas\}.*manifold learning",
        "credits": LECTURE2_CREDITS,
        "tikz_setup": LECTURE2_TIKZ
    },
    {
        "lecture_dir": "2",
        "lecture_num": "2",
        "topic_name": "manifold-learning",
        "topic_title": "Manifold Learning",
        "topic_subtitle": "Laplacian Eigenmaps",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Background: Manifold Learning\}",
        "end_pattern": r"\\setbeamertemplate\{background canvas\}.*recommendation",
        "credits": LECTURE2_CREDITS,
        "tikz_setup": LECTURE2_TIKZ
    },
    {
        "lecture_dir": "2",
        "lecture_num": "2",
        "topic_name": "recommendations-resistance",
        "topic_title": "Recommendations and Resistance Networks",
        "topic_subtitle": "Graph Distances and Effective Resistance",
        "start_pattern": r"\\begin\{frame\}\s*\\frametitle\{\\bf Use of Laplacians: Movie recommendation\}",
        "end_pattern": None,
        "credits": LECTURE2_CREDITS,
        "tikz_setup": LECTURE2_TIKZ
    },
]

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    created = 0
    failed = 0
    
    for subdeck in ALL_SUBDECKS:
        if create_subdeck(**subdeck):
            created += 1
        else:
            failed += 1
    
    print(f"\nSummary: Created {created} subdecks, {failed} failed")
