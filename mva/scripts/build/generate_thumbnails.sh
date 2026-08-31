#!/bin/bash
# Script location: scripts/build/generate_thumbnails.sh
# =============================================================================
# Generate Thumbnails for PDF Slides
# =============================================================================
# Creates thumbnail images (first page) for each PDF

set -e

THUMB_DIR="/Users/michalvalko/Documents/GitHub/misovalko.github.io/mva/materials/lectures/thumbnails"
mkdir -p "$THUMB_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Generating Slide Thumbnails ===${NC}\n"

count=0

# Generate thumbnails for main lecture files and key topic files
for dir in 0 1 2 3 4 5 6 7 8; do
    if [ ! -d "$dir" ]; then
        continue
    fi

    # Main lecture file
    if [ -f "$dir/mlgraphs$dir.pdf" ]; then
        output="$THUMB_DIR/mlgraphs$dir-thumb.jpg"
        if [ ! -f "$output" ]; then
            convert -density 150 "$dir/mlgraphs$dir.pdf[0]" \
                    -quality 85 \
                    -resize 300x \
                    "$output" 2>/dev/null && \
            echo -e "${GREEN}✓${NC} Created thumbnail for mlgraphs$dir.pdf" && \
            ((count++)) || \
            echo "✗ Failed: mlgraphs$dir.pdf"
        fi
    fi

    # Key topic files (first few in each directory)
    topic_count=0
    for pdf in "$dir"/mlgraphs-*.pdf; do
        if [ -f "$pdf" ] && [ $topic_count -lt 3 ]; then
            filename=$(basename "$pdf" .pdf)
            output="$THUMB_DIR/${filename}-thumb.jpg"
            if [ ! -f "$output" ]; then
                convert -density 150 "$pdf[0]" \
                        -quality 85 \
                        -resize 300x \
                        "$output" 2>/dev/null && \
                echo -e "${GREEN}✓${NC} Created thumbnail for $filename.pdf" && \
                ((count++)) || \
                echo "✗ Failed: $filename.pdf"
            fi
            ((topic_count++))
        fi
    done
done

echo -e "\n${BLUE}=== Summary ===${NC}"
echo -e "${GREEN}Generated $count thumbnails${NC}"
echo "Location: $THUMB_DIR"
