#!/usr/bin/env python3
"""
Remove Administrivia, lecture navigation, and deadline reminders from all subdecks.
"""
import re
import os
from pathlib import Path

def should_remove_frame(content, frame_start, frame_end):
    """Check if a frame should be removed."""
    frame_content = content[frame_start:frame_end].lower()
    
    # Patterns to remove
    patterns = [
        r'\\frametitle\{.*administrivia',
        r'\\frametitle\{.*this lecture',
        r'\\frametitle\{.*previous lecture',
        r'\\frametitle\{.*next lecture',
        r'\\frametitle\{.*this topic',
        r'\\frametitle\{.*next class',
        r'\\frametitle\{.*previous lab',
        r'\\frametitle\{.*next.*lab',
        r'deadline',
        r'reminder',
        r'validation:',
        r'prerequisites:',
        r'course website',
        r'8 lectures',
        r'recitations',
    ]
    
    for pattern in patterns:
        if re.search(pattern, frame_content):
            return True
    return False

def remove_frames_from_file(filepath):
    """Remove unwanted frames from a subdeck file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    modified = False
    
    # Find all frames
    frame_pattern = r'\\begin\{frame\}'
    frames = list(re.finditer(frame_pattern, content))
    
    # Process frames from end to start to preserve indices
    for frame_match in reversed(frames):
        frame_start = frame_match.start()
        
        # Find the end of this frame
        remaining = content[frame_start:]
        end_match = re.search(r'\\end\{frame\}', remaining)
        if not end_match:
            continue
        
        frame_end = frame_start + end_match.end()
        
        # Check if this frame should be removed
        if should_remove_frame(content, frame_start, frame_end):
            # Remove the frame (including any preceding whitespace/comments)
            # Find where the frame actually starts (may have comments before)
            before_frame = content[:frame_start]
            # Remove trailing newlines and comments before the frame
            before_clean = before_frame.rstrip()
            # Keep one newline if there was content before
            if before_clean and not before_clean.endswith('\n'):
                before_clean += '\n'
            
            # Get content after frame
            after_frame = content[frame_end:]
            # Remove leading newlines after the frame
            after_clean = after_frame.lstrip()
            # Keep one newline if there's content after
            if after_clean and not after_clean.startswith('\n'):
                after_clean = '\n' + after_clean
            
            content = before_clean + after_clean
            modified = True
    
    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    
    cleaned = 0
    for lecture_dir in ['1', '2', '3', '4', '5', '6', '7']:
        lecture_path = base_dir / lecture_dir
        if not lecture_path.exists():
            continue
        
        for tex_file in lecture_path.glob('mlgraphs-*.tex'):
            if remove_frames_from_file(tex_file):
                print(f"Cleaned: {tex_file}")
                cleaned += 1
            else:
                print(f"No changes: {tex_file}")
    
    print(f"\nCleaned {cleaned} subdeck files")
