#!/bin/bash
# Script location: scripts/build/optimize_pdfs.sh
# =============================================================================
# PDF Optimization Script for MVA ML Graphs Lecture Slides
# =============================================================================
# Uses Ghostscript to compress PDF files
#
# Usage: ./optimize_pdfs.sh [--dry-run]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

DRY_RUN=false
if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
fi

TOTAL_BEFORE=0
TOTAL_AFTER=0

echo -e "${BLUE}=== PDF Optimization ===${NC}\n"

# Function to get file size in bytes
get_size() {
    stat -f%z "$1" 2>/dev/null || stat -c%s "$1" 2>/dev/null || echo 0
}

# Function to format bytes
format_size() {
    local size=$1
    if [ $size -ge 1048576 ]; then
        echo "$(echo "scale=1; $size/1048576" | bc)MB"
    else
        echo "$(echo "scale=1; $size/1024" | bc)KB"
    fi
}

# Function to optimize a single PDF
optimize_pdf() {
    local file=$1
    local temp_file="${file%.pdf}_temp.pdf"

    local size_before=$(get_size "$file")
    TOTAL_BEFORE=$((TOTAL_BEFORE + size_before))

    if [ "$DRY_RUN" = true ]; then
        echo "  Would optimize: $file ($(format_size $size_before))"
        return
    fi

    # Use Ghostscript to compress PDF
    gs -sDEVICE=pdfwrite \
       -dCompatibilityLevel=1.5 \
       -dPDFSETTINGS=/screen \
       -dNOPAUSE -dQUIET -dBATCH \
       -dEmbedAllFonts=true \
       -dSubsetFonts=true \
       -dColorImageDownsampleType=/Bicubic \
       -dColorImageResolution=150 \
       -dGrayImageDownsampleType=/Bicubic \
       -dGrayImageResolution=150 \
       -dMonoImageDownsampleType=/Bicubic \
       -dMonoImageResolution=150 \
       -sOutputFile="$temp_file" \
       "$file" 2>/dev/null

    if [ -f "$temp_file" ]; then
        local size_after=$(get_size "$temp_file")
        TOTAL_AFTER=$((TOTAL_AFTER + size_after))

        # Only replace if the compressed version is smaller
        if [ $size_after -lt $size_before ]; then
            mv "$temp_file" "$file"
            local saved=$((size_before - size_after))
            local percent=$((100 * saved / size_before))
            echo -e "  ${GREEN}✓${NC} $(basename "$file"): $(format_size $size_before) → $(format_size $size_after) (-${percent}%)"
        else
            rm "$temp_file"
            TOTAL_AFTER=$((TOTAL_AFTER - size_after + size_before))
            echo "  ⊘ $(basename "$file"): Already optimized"
        fi
    else
        echo "  ✗ $(basename "$file"): Failed to optimize"
        TOTAL_AFTER=$((TOTAL_AFTER + size_before))
    fi
}

# Find and optimize all PDFs
for dir in 0 1 2 3 4 5 6 7 8; do
    if [ ! -d "$dir" ]; then
        continue
    fi

    pdf_files=("$dir"/*.pdf)
    if [ -e "${pdf_files[0]}" ]; then
        echo -e "${YELLOW}Directory $dir:${NC}"
        for pdf in "${pdf_files[@]}"; do
            optimize_pdf "$pdf"
        done
        echo ""
    fi
done

# Summary
if [ "$DRY_RUN" = false ]; then
    echo -e "${BLUE}=== Optimization Summary ===${NC}"
    echo -e "Total before: $(format_size $TOTAL_BEFORE)"
    echo -e "Total after:  $(format_size $TOTAL_AFTER)"

    if [ $TOTAL_BEFORE -gt 0 ]; then
        local saved=$((TOTAL_BEFORE - TOTAL_AFTER))
        local percent=$((100 * saved / TOTAL_BEFORE))
        echo -e "${GREEN}Saved: $(format_size $saved) (-${percent}%)${NC}"
    fi
fi
