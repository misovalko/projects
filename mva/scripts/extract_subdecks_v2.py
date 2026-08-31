#!/usr/bin/env python3
"""
Extract subdecks from lecture files using line-based extraction.
"""
import os
from pathlib import Path

def find_line_with_pattern(lines, pattern, start_line=0):
    """Find line number containing pattern."""
    for i in range(start_line, len(lines)):
        if pattern in lines[i]:
            return i
    return None

def find_frame_end(lines, start_idx):
    """Find the end of a frame starting at start_idx."""
    # Look for \end{frame} after start_idx
    for i in range(start_idx + 1, len(lines)):
        if '\\end{frame}' in lines[i]:
            return i + 1
    return len(lines)

def extract_lines_between_patterns(lines, start_pattern, end_pattern=None, start_offset=0):
    """Extract lines between two patterns, ensuring complete frames."""
    start_idx = find_line_with_pattern(lines, start_pattern, start_offset)
    if start_idx is None:
        return None, None
    
    # Find the frame that contains start_pattern
    # Go backwards to find \begin{frame}
    frame_start = start_idx
    for i in range(start_idx, max(0, start_idx - 20), -1):
        if '\\begin{frame}' in lines[i]:
            frame_start = i
            break
    
    if end_pattern:
        end_frame_start = find_line_with_pattern(lines, end_pattern, start_idx + 1)
        if end_frame_start is None:
            # Go to end of document, but before \input{lastslide}
            for i in range(len(lines) - 1, max(0, len(lines) - 50), -1):
                if '\\input{../common/mvamlgraphslastslide}' in lines[i]:
                    end_idx = i
                    break
            else:
                end_idx = len(lines)
        else:
            # Find the frame start for the end pattern (this is the NEXT topic's frame)
            end_frame_begin = end_frame_start
            for i in range(end_frame_start, max(0, end_frame_start - 20), -1):
                if '\\begin{frame}' in lines[i]:
                    end_frame_begin = i
                    break
            # Now find the LAST \end{frame} BEFORE end_frame_begin (this is the end of current topic)
            # Need to be careful: there might be a special title slide (with beamer template changes)
            # between the last content frame and the next topic's frame. We should stop before that.
            end_idx = end_frame_begin
            # First, find the last \end{frame} before end_frame_begin
            last_end_frame = None
            for i in range(end_frame_begin - 1, max(0, end_frame_begin - 200), -1):
                if '\\end{frame}' in lines[i]:
                    last_end_frame = i
                    break
            if last_end_frame is not None:
                # Check if the frame ending at last_end_frame is part of a special title slide.
                # Title slides typically have \setbeamertemplate{background canvas} before them.
                # Find the \begin{frame} for the frame ending at last_end_frame
                frame_start_for_last_end = None
                for i in range(last_end_frame, max(0, last_end_frame - 50), -1):
                    if '\\begin{frame}' in lines[i]:
                        frame_start_for_last_end = i
                        break
                # Check if there's a \setbeamertemplate{background canvas} before this frame
                # (within reasonable distance, say 20 lines)
                is_title_slide = False
                if frame_start_for_last_end is not None:
                    for i in range(frame_start_for_last_end - 1, max(0, frame_start_for_last_end - 20), -1):
                        if '\\setbeamertemplate{background canvas}' in lines[i]:
                            is_title_slide = True
                            break
                # If this is a title slide, find the \end{frame} before it
                if is_title_slide and frame_start_for_last_end is not None:
                    for i in range(frame_start_for_last_end - 1, max(0, frame_start_for_last_end - 200), -1):
                        if '\\end{frame}' in lines[i]:
                            last_end_frame = i  # Update to the frame before the title slide
                            break
                # Include everything up to and including the \end{frame} line
                end_idx = last_end_frame + 1
            else:
                # Fallback: just use end_frame_begin
                end_idx = end_frame_begin
    else:
        # Go to end, but before \input{lastslide}
        for i in range(len(lines) - 1, max(0, len(lines) - 50), -1):
            if '\\input{../common/mvamlgraphslastslide}' in lines[i]:
                end_idx = i
                break
        else:
            end_idx = len(lines)
    
    return frame_start, end_idx

def get_header_lines(lecture_file):
    """Get header lines up to \begin{document}."""
    with open(lecture_file, 'r') as f:
        lines = f.readlines()
    
    header_lines = []
    for i, line in enumerate(lines):
        if '\\begin{document}' in line:
            header_lines.append(line)
            break
        header_lines.append(line)
    
    return header_lines if header_lines else None

def create_subdeck_from_lines(lecture_dir, lecture_num, topic_name, topic_title, topic_subtitle,
                              start_pattern, end_pattern, credits, tikz_setup=None):
    """Create a subdeck file by extracting specific lines."""
    lecture_file = f"{lecture_dir}/mlgraphs{lecture_num}.tex"
    
    if not os.path.exists(lecture_file):
        print(f"Warning: {lecture_file} not found")
        return False
    
    with open(lecture_file, 'r') as f:
        lines = f.readlines()
    
    # Find frame boundaries
    start_idx, end_idx = extract_lines_between_patterns(lines, start_pattern, end_pattern)
    if start_idx is None:
        print(f"Warning: Could not find start pattern '{start_pattern}' in {lecture_file}")
        return False
    
    # Extract content
    content_lines = lines[start_idx:end_idx] if end_idx else lines[start_idx:]
    content = ''.join(content_lines)
    
    # Get header
    header_lines = get_header_lines(lecture_file)
    if not header_lines:
        header = f"""% !TEX TS-program = lualatex
\\documentclass{{beamer}}
\\input{{../common/misomva}}
\\begin{{document}}
"""
    else:
        header = ''.join(header_lines)
    
    # Create subdeck - check if header already has misoclasstinytitleslide
    header_text = header.rstrip()
    if '\\newcommand{\\misoclasstinytitleslide}' in header_text:
        # Use renewcommand
        credits_cmd = f"\\renewcommand{{\\misoclasstinytitleslide}}{{{credits}}}"
    else:
        # Use newcommand
        credits_cmd = f"\\newcommand{{\\misoclasstinytitleslide}}{{{credits}}}"
    
    subdeck_content = header_text + "\n"
    subdeck_content += f"""% Topic-specific title slide
\\newcommand{{\\topictitle}}{{{topic_title}}}
\\newcommand{{\\topicsubtitle}}{{{topic_subtitle}}}
{credits_cmd}
"""
    
    if tikz_setup:
        subdeck_content += f"{tikz_setup}\n"
    
    subdeck_content += f"""
\\input{{../common/mvamlgraphstopic1slide}}

{content}

\\input{{../common/mvamlgraphslastslide}}
\\end{{document}}
"""
    
    # Write file
    subdeck_file = f"{lecture_dir}/mlgraphs-{topic_name}.tex"
    with open(subdeck_file, 'w') as f:
        f.write(subdeck_content)
    
    print(f"Created: {subdeck_file} ({end_idx - start_idx if end_idx else 'rest'} lines)")
    return True

# Configuration
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
LECTURE3_CREDITS = "Partially based on material by:  Mikhail Belkin, Partha Niyogi, \\\\[-1em] Olivier Chapelle, Bernhard Sch\\\"olkopf"
LECTURE4_CREDITS = "Partially based on material by:  Mikhail Belkin, Partha Niyogi, \\\\[-1em] Olivier Chapelle, Bernhard Sch\\\"olkopf"
LECTURE5_CREDITS = "Partially based on material by:  Branislav Kveton, \\\\[-1em] Mikhail Belkin, Jerry Zhu"
LECTURE6_CREDITS = "Partially based on material by:  Rob Fergus, Nikhil Srivastava,\\\\[-1em] Yiannis Koutis, Joshua Batson, Daniel Spielman"
LECTURE7_CREDITS = "Partially based on material by:  Branislav Kveton, \\\\[-1em] Andreas Krause"

# Add remaining lecture subdecks
ALL_SUBDECKS = [
    # Lecture 1
    {
        "lecture_dir": "1", "lecture_num": "1",
        "topic_name": "introduction",
        "topic_title": "Introduction to Graphs in ML",
        "topic_subtitle": "Course Overview and Motivation",
        "start_pattern": "\\frametitle{\\bf Administrivia}",
        "end_pattern": "\\frametitle{\\bf Natural graphs from",
        "credits": LECTURE1_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "1", "lecture_num": "1",
        "topic_name": "natural-graphs",
        "topic_title": "Natural Graphs",
        "topic_subtitle": "Social, Information, and Biological Networks",
        "start_pattern": "\\frametitle{\\bf Natural graphs from",
        "end_pattern": "\\frametitle{\\bf Submodularity:",
        "credits": LECTURE1_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "1", "lecture_num": "1",
        "topic_name": "submodularity",
        "topic_title": "Submodularity",
        "topic_subtitle": "Theory and Product Placement Application",
        "start_pattern": "\\frametitle{\\bf Submodularity:",
        "end_pattern": "\\frametitle{\\bf Success story #2",
        "credits": LECTURE1_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "1", "lecture_num": "1",
        "topic_name": "pagerank",
        "topic_title": "Google PageRank",
        "topic_subtitle": "Random Surfer and Steady State",
        "start_pattern": "\\frametitle{\\bf Success story \\#2",
        "end_pattern": "\\frametitle{\\bf.*Similarity",
        "credits": LECTURE1_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "1", "lecture_num": "1",
        "topic_name": "similarity-graphs",
        "topic_title": "Similarity Graphs",
        "topic_subtitle": "Graph Theory Refresher and Construction",
        "start_pattern": "\\frametitle{\\bf Graph theory refresher}",
        "end_pattern": None,
        "credits": LECTURE1_CREDITS, "tikz_setup": None
    },
    
    # Lecture 2 - skip similarity-graphs-construction (already created)
    {
        "lecture_dir": "2", "lecture_num": "2",
        "topic_name": "graph-laplacian",
        "topic_title": "Graph Laplacian",
        "topic_subtitle": "Properties and Spectral Theory",
        "start_pattern": "\\frametitle{\\bf Graph Laplacian}",
        "end_pattern": "spectral clustering",
        "credits": LECTURE2_CREDITS, "tikz_setup": LECTURE2_TIKZ
    },
    {
        "lecture_dir": "2", "lecture_num": "2",
        "topic_name": "spectral-clustering",
        "topic_title": "Spectral Clustering",
        "topic_subtitle": "Theory and Applications",
        "start_pattern": "\\frametitle{\\bf Spectral Clustering: Cuts",
        "end_pattern": "\\frametitle{\\bf Background: Manifold Learning",
        "credits": LECTURE2_CREDITS, "tikz_setup": LECTURE2_TIKZ
    },
    {
        "lecture_dir": "2", "lecture_num": "2",
        "topic_name": "manifold-learning",
        "topic_title": "Manifold Learning",
        "topic_subtitle": "Laplacian Eigenmaps",
        "start_pattern": "\\frametitle{\\bf Background: Manifold Learning",
        "end_pattern": "\\frametitle{\\bf Use of Laplacians: Movie recommendation",
        "credits": LECTURE2_CREDITS, "tikz_setup": LECTURE2_TIKZ
    },
    {
        "lecture_dir": "2", "lecture_num": "2",
        "topic_name": "recommendations-resistance",
        "topic_title": "Recommendations and Resistance Networks",
        "topic_subtitle": "Graph Distances and Effective Resistance",
        "start_pattern": "\\frametitle{\\bf Use of Laplacians: Movie recommendation",
        "end_pattern": None,
        "credits": LECTURE2_CREDITS, "tikz_setup": LECTURE2_TIKZ
    },
    
    # Lecture 3
    {
        "lecture_dir": "3", "lecture_num": "3",
        "topic_name": "manifold-learning-continued",
        "topic_title": "Manifold Learning",
        "topic_subtitle": "Laplacian Eigenmaps (Continued)",
        "start_pattern": "\\frametitle{\\bf Background: Manifold Learning",
        "end_pattern": "\\frametitle{\\bf Semi-supervised learning",
        "credits": LECTURE3_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "3", "lecture_num": "3",
        "topic_name": "ssl-introduction",
        "topic_title": "Semi-Supervised Learning Introduction",
        "topic_subtitle": "Why and When SSL Helps",
        "start_pattern": "\\frametitle{\\bf Semi-supervised learning",
        "end_pattern": "\\frametitle{\\bf SSL with Graphs: Harmonic",
        "credits": LECTURE3_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "3", "lecture_num": "3",
        "topic_name": "ssl-harmonic-functions",
        "topic_title": "SSL with Graphs: Harmonic Functions",
        "topic_subtitle": "Gaussian Random Fields Solution",
        "start_pattern": "\\frametitle{\\bf SSL with Graphs: Harmonic",
        "end_pattern": "\\frametitle{\\bf SSL with Graphs: Regularized",
        "credits": LECTURE3_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "3", "lecture_num": "3",
        "topic_name": "ssl-regularization",
        "topic_title": "SSL Regularization and Stability",
        "topic_subtitle": "Regularized, Soft Harmonic, and Stability Bounds",
        "start_pattern": "\\frametitle{\\bf SSL with Graphs: Regularized",
        "end_pattern": "\\frametitle{\\bf SSL with Graphs: Manifold Regularization",
        "credits": LECTURE3_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "3", "lecture_num": "3",
        "topic_name": "ssl-manifold-regularization",
        "topic_title": "SSL Manifold Regularization",
        "topic_subtitle": "Manifold Regularization and Laplacian SVMs",
        "start_pattern": "\\frametitle{\\bf SSL with Graphs: Manifold Regularization",
        "end_pattern": None,
        "credits": LECTURE3_CREDITS, "tikz_setup": None
    },
    
    # Lecture 4
    {
        "lecture_dir": "4", "lecture_num": "4",
        "topic_name": "ssl-transductive-bounds",
        "topic_title": "Transductive Generalization Bounds",
        "topic_subtitle": "Stability-Based Bounds for SSL",
        "start_pattern": "\\frametitle{\\bf Transductive Generalization Bounds",
        "end_pattern": "\\frametitle{\\bf SSL with Graphs: Laplacian SVMs",
        "credits": LECTURE4_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "4", "lecture_num": "4",
        "topic_name": "ssl-lapsvms-maxmargin",
        "topic_title": "Laplacian SVMs and Max-Margin Graph Cuts",
        "topic_subtitle": "Inductive SSL Methods",
        "start_pattern": "\\frametitle{\\bf SSL with Graphs: Laplacian SVMs",
        "end_pattern": "\\frametitle{\\bf Inductive Generalization Bounds",
        "credits": LECTURE4_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "4", "lecture_num": "4",
        "topic_name": "ssl-inductive-bounds",
        "topic_title": "Inductive Generalization Bounds",
        "topic_subtitle": "Theoretical Guarantees for Inductive SSL",
        "start_pattern": "\\frametitle{\\bf Inductive Generalization Bounds",
        "end_pattern": None,
        "credits": LECTURE4_CREDITS, "tikz_setup": None
    },
    
    # Lecture 5
    {
        "lecture_dir": "5", "lecture_num": "5",
        "topic_name": "online-ssl",
        "topic_title": "Online SSL with Graphs",
        "topic_subtitle": "Graph Quantization and Online Learning",
        "start_pattern": "\\frametitle{\\bf \\emphcol{Online} SSL with Graphs",
        "end_pattern": "\\frametitle{\\bf Online SSL with Graphs: Analysis",
        "credits": LECTURE5_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "5", "lecture_num": "5",
        "topic_name": "online-ssl-analysis",
        "topic_title": "Analysis of Online SSL",
        "topic_subtitle": "Quantization Error and Performance Analysis",
        "start_pattern": "\\frametitle{\\bf Online SSL with Graphs: Analysis",
        "end_pattern": "\\frametitle{\\bf SSL with Graphs: What is behind it",
        "credits": LECTURE5_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "5", "lecture_num": "5",
        "topic_name": "ssl-learnability",
        "topic_title": "SSL Learnability",
        "topic_subtitle": "When Does Graph-Based SSL Provably Help?",
        "start_pattern": "\\frametitle{\\bf SSL with Graphs: What is behind it",
        "end_pattern": None,
        "credits": LECTURE5_CREDITS, "tikz_setup": None
    },
    
    # Lecture 6
    {
        "lecture_dir": "6", "lecture_num": "6",
        "topic_name": "large-scale-introduction",
        "topic_title": "Large-Scale Machine Learning on Graphs",
        "topic_subtitle": "Computational Bottlenecks and Challenges",
        "start_pattern": "\\frametitle{\\bf Large scale Machine Learning on Graphs",
        "end_pattern": "\\frametitle{\\bf Graph Sparsification",
        "credits": LECTURE6_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "6", "lecture_num": "6",
        "topic_name": "graph-sparsification",
        "topic_title": "Graph Sparsification",
        "topic_subtitle": "Cut and Spectral Sparsifiers",
        "start_pattern": "\\frametitle{\\bf Graph Sparsification",
        "end_pattern": "\\frametitle{\\bf Distributed graph processing",
        "credits": LECTURE6_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "6", "lecture_num": "6",
        "topic_name": "distributed-processing",
        "topic_title": "Distributed Graph Processing",
        "topic_subtitle": "GraphLab Abstraction and Large-Scale Tools",
        "start_pattern": "\\frametitle{\\bf Distributed graph processing",
        "end_pattern": None,
        "credits": LECTURE6_CREDITS, "tikz_setup": None
    },
    
    # Lecture 7
    {
        "lecture_dir": "7", "lecture_num": "7",
        "topic_name": "multi-armed-bandits",
        "topic_title": "Multi-Armed Bandits",
        "topic_subtitle": "UCB Algorithm and Regret Bounds",
        "start_pattern": "\\frametitle{\\bf Multi-Armed Bandits",
        "end_pattern": "\\frametitle{\\bf Spectral Bandits",
        "credits": LECTURE7_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "7", "lecture_num": "7",
        "topic_name": "spectral-bandits",
        "topic_title": "Spectral Bandits",
        "topic_subtitle": "SpectralUCB Algorithm",
        "start_pattern": "\\frametitle{\\bf Spectral Bandits",
        "end_pattern": "\\frametitle{\\bf Influence Maximization",
        "credits": LECTURE7_CREDITS, "tikz_setup": None
    },
    {
        "lecture_dir": "7", "lecture_num": "7",
        "topic_name": "influence-maximization",
        "topic_title": "Influence Maximization on Graphs",
        "topic_subtitle": "BARE Algorithm and Detectable Dimension",
        "start_pattern": "\\frametitle{\\bf Influence Maximization",
        "end_pattern": None,
        "credits": LECTURE7_CREDITS, "tikz_setup": None
    },
]

if __name__ == "__main__":
    # Script is in mva/scripts/, need to go to mva/materials/slides/
    base_dir = Path(__file__).parent.parent / "materials" / "slides"
    os.chdir(base_dir)
    
    created = 0
    failed = 0
    
    for subdeck in ALL_SUBDECKS:
        if create_subdeck_from_lines(**subdeck):
            created += 1
        else:
            failed += 1
    
    print(f"\nSummary: Created {created} subdecks, {failed} failed")
