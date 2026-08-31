#!/usr/bin/env python3
"""
Script to extract subdecks from lecture files based on frame title patterns.
"""
import re
import os
from pathlib import Path

def find_frame_ranges(content, start_pattern, end_pattern=None):
    """Find content between two frame patterns."""
    start_match = re.search(start_pattern, content, re.MULTILINE)
    if not start_match:
        return None
    
    start_pos = start_match.start()
    
    if end_pattern:
        end_match = re.search(end_pattern, content[start_pos:], re.MULTILINE)
        if end_match:
            end_pos = start_pos + end_match.start()
        else:
            end_pos = len(content)
    else:
        end_pos = len(content)
    
    return content[start_pos:end_pos]

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
    frames_content = find_frame_ranges(content, start_pattern, end_pattern)
    if not frames_content:
        print(f"Warning: Could not find content for {topic_name}")
        return False
    
    # Get header from original file
    header_match = re.search(r'% !TEX TS-program.*?\\begin\{document\}', content, re.DOTALL)
    if header_match:
        header = header_match.group(0)
    else:
        header = f"""% !TEX TS-program = lualatex
\\documentclass{{beamer}}
\\input{{../common/misomva}}
\\begin{{document}}"""
    
    # Create subdeck content
    subdeck_content = f"""{header}
% Topic-specific title slide
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

# Lecture 2 subdecks
lecture2_dir = "2"
lecture2_credits = "Partially based on material by:  Ulrike von Luxburg, \\\\[-1em] Gary Miller, Doyle \\& Schnell, Daniel Spielman"
lecture2_tikz = """\\usetikzlibrary{graphs}

\\tikzset{{
  vertex/.style={{circle,fill=black!25,minimum size=20pt,inner sep=0pt}},
  selected vertex/.style={{vertex, fill=red!24}},
  edge/.style={{draw,thick,->}},
  weight/.style={{font=\\small}},
  selected edge/.style={{draw,line width=5pt,-,red!50}},
  ignored edge/.style={{draw,line width=5pt,-,black!20}}
}}"""

# Define all subdecks
subdecks = [
    # Lecture 2
    {
        "lecture_dir": "2",
        "lecture_num": "2",
        "topic_name": "similarity-graphs-construction",
        "topic_title": "Similarity Graphs Construction",
        "topic_subtitle": "Building Graphs from Data",
        "start_pattern": r"\\\\begin\{frame\}\s*\\\\frametitle\{\\\\bf Similarity Graphs\}",
        "end_pattern": r"\\\\setbeamertemplate\{background canvas\}.*?\\\\frametitle\{\\\\bf Graph Laplacian\}",
        "credits": lecture2_credits,
        "tikz_setup": lecture2_tikz
    },
    {
        "lecture_dir": "2",
        "lecture_num": "2",
        "topic_name": "graph-laplacian",
        "topic_title": "Graph Laplacian",
        "topic_subtitle": "Properties and Spectral Theory",
        "start_pattern": r"\\\\begin\{frame\}\s*\\\\frametitle\{\\\\bf Graph Laplacian\}",
        "end_pattern": r"\\\\setbeamertemplate\{background canvas\}.*?spectral clustering",
        "credits": lecture2_credits,
        "tikz_setup": lecture2_tikz
    },
]

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    for subdeck in subdecks:
        create_subdeck(**subdeck)
