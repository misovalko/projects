#!/usr/bin/env python3
"""
Remove Administrivia, lecture navigation, and deadline reminders from all subdecks.
"""
import re
import os
from pathlib import Path

def remove_unwanted_frames(content):
    """Remove frames with unwanted content."""
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a frame start
        if '\\begin{frame}' in line:
            # Collect the entire frame
            frame_lines = [line]
            i += 1
            frame_start_idx = i - 1
            
            # Find frametitle
            frametitle_found = False
            frametitle_line = None
            
            # Collect until we find \end{frame}
            while i < len(lines) and '\\end{frame}' not in lines[i]:
                frame_lines.append(lines[i])
                if '\\frametitle' in lines[i]:
                    frametitle_found = True
                    frametitle_line = lines[i].lower()
                i += 1
            
            # Add the \end{frame} line
            if i < len(lines):
                frame_lines.append(lines[i])
                i += 1
            
            # Check if this frame should be removed
            should_remove = False
            if frametitle_found and frametitle_line:
                patterns = [
                    'administrivia',
                    'this lecture',
                    'previous lecture',
                    'next lecture',
                    'this topic',
                    'next class',
                    'previous lab',
                    'next.*lab',
                ]
                for pattern in patterns:
                    if re.search(pattern, frametitle_line):
                        should_remove = True
                        break
            
            # Also check frame content for deadline/reminder
            frame_content = '\n'.join(frame_lines).lower()
            if not should_remove:
                content_patterns = [
                    r'\bdeadline\b',
                    r'\breminder\b',
                    r'validation:',
                    r'8 lectures',
                    r'recitations',
                    r'course website',
                ]
                for pattern in content_patterns:
                    if re.search(pattern, frame_content):
                        should_remove = True
                        break
            
            if not should_remove:
                result_lines.extend(frame_lines)
        else:
            result_lines.append(line)
            i += 1
    
    return '\n'.join(result_lines)

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    
    cleaned = 0
    for lecture_dir in ['1', '2', '3', '4', '5', '6', '7']:
        lecture_path = base_dir / lecture_dir
        if not lecture_path.exists():
            continue
        
        for tex_file in lecture_path.glob('mlgraphs-*.tex'):
            with open(tex_file, 'r') as f:
                original = f.read()
            
            cleaned_content = remove_unwanted_frames(original)
            
            if cleaned_content != original:
                with open(tex_file, 'w') as f:
                    f.write(cleaned_content)
                print(f"Cleaned: {tex_file}")
                cleaned += 1
    
    print(f"\nCleaned {cleaned} subdeck files")
