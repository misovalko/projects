#!/usr/bin/env python3
"""
Remove all course-specific and navigation frames from subdecks.
"""
import re
from pathlib import Path

def remove_frame_by_pattern(content, pattern):
    """Remove frames matching a pattern."""
    # Find all frame starts
    frame_starts = []
    for match in re.finditer(r'\\begin\{frame\}', content):
        frame_starts.append(match.start())
    
    # Process from end to start
    for frame_start in reversed(frame_starts):
        # Find frame end
        remaining = content[frame_start:]
        end_match = re.search(r'\\end\{frame\}', remaining)
        if not end_match:
            continue
        
        frame_end = frame_start + end_match.end()
        frame_content = content[frame_start:frame_end]
        
        # Check if frame matches pattern
        if re.search(pattern, frame_content, re.IGNORECASE):
            # Remove frame
            before = content[:frame_start].rstrip()
            after = content[frame_end:].lstrip()
            
            # Preserve spacing
            if before and not before.endswith('\n'):
                before += '\n'
            if after and not after.startswith('\n'):
                after = '\n' + after
            
            content = before + after
    
    return content

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    
    patterns_to_remove = [
        r'\\frametitle\{[^}]*administrivia',
        r'\\frametitle\{[^}]*this lecture',
        r'\\frametitle\{[^}]*previous lecture',
        r'\\frametitle\{[^}]*next lecture',
        r'\\frametitle\{[^}]*this topic',
        r'\\frametitle\{[^}]*next class',
        r'\\frametitle\{[^}]*previous lab',
        r'\\frametitle\{[^}]*next.*lab',
        r'\\frametitle\{[^}]*links to.*courses',
        r'deadline',
        r'reminder',
        r'validation:',
        r'8 lectures',
        r'recitations',
    ]
    
    cleaned = 0
    for lecture_dir in ['1', '2', '3', '4', '5', '6', '7']:
        lecture_path = base_dir / lecture_dir
        if not lecture_path.exists():
            continue
        
        for tex_file in lecture_path.glob('mlgraphs-*.tex'):
            with open(tex_file, 'r') as f:
                content = f.read()
            
            original = content
            for pattern in patterns_to_remove:
                content = remove_frame_by_pattern(content, pattern)
            
            if content != original:
                with open(tex_file, 'w') as f:
                    f.write(content)
                print(f"Cleaned: {tex_file}")
                cleaned += 1
    
    print(f"\nCleaned {cleaned} subdeck files")
