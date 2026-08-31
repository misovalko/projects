import re
import sys

def extract_frames(filename, start_pattern, end_pattern):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find start
    start_match = re.search(start_pattern, content)
    if not start_match:
        return None
    
    start_pos = start_match.start()
    
    # Find end
    if end_pattern:
        end_match = re.search(end_pattern, content[start_pos:])
        if end_match:
            end_pos = start_pos + end_match.start()
        else:
            end_pos = len(content)
    else:
        end_pos = len(content)
    
    return content[start_pos:end_pos]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: extract_frames.py <file> <start_pattern> [end_pattern]")
        sys.exit(1)
    
    filename = sys.argv[1]
    start_pattern = sys.argv[2]
    end_pattern = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = extract_frames(filename, start_pattern, end_pattern)
    if result:
        print(result)
    else:
        print("Pattern not found", file=sys.stderr)
        sys.exit(1)
