#!/bin/bash
# Script location: scripts/build/build_all.sh
# =============================================================================
# Build Script for MVA ML Graphs Lecture Slides
# =============================================================================
# Compiles all LaTeX presentation files and cleans up auxiliary files
#
# Usage: cd /path/to/slides && ./scripts/build/build_all.sh [--clean-only]
#    Or: cd /path/to/slides/scripts/build && ./build_all.sh [--clean-only]

set -e  # Exit on error

# Ensure we're in the slides directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# SCRIPT_DIR is projects/mva/scripts/build
# SLIDES_DIR should be projects/mva/materials/slides
# ../.. goes to projects/mva
# then materials/slides
SLIDES_DIR="$(cd "$SCRIPT_DIR/../../materials/slides" && pwd)"
cd "$SLIDES_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
SUCCESS_COUNT=0
FAIL_COUNT=0
FAILED_FILES=()

# Function to clean auxiliary files
clean_aux_files() {
    echo -e "${BLUE}Cleaning auxiliary files...${NC}"
    find . -type f \( \
        -name "*.aux" -o \
        -name "*.log" -o \
        -name "*.nav" -o \
        -name "*.out" -o \
        -name "*.snm" -o \
        -name "*.toc" -o \
        -name "*.bcf" -o \
        -name "*.run.xml" -o \
        -name "*.blg" -o \
        -name "*.bbl" -o \
        -name "*.synctex.gz" -o \
        -name "*.fls" -o \
        -name "*.fdb_latexmk" -o \
        -name "*.xdv" \
    \) -delete
    echo -e "${GREEN}✓ Auxiliary files cleaned${NC}"
}

# Function to compile a single file
compile_file() {
    local file=$1
    local dir=$(dirname "$file")
    local base=$(basename "$file")

    echo -n "  Compiling $base... "

    if (cd "$dir" && lualatex -interaction=nonstopmode "$base" > /dev/null 2>&1); then
        echo -e "${GREEN}✓${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}✗${NC}"
        ((FAIL_COUNT++))
        FAILED_FILES+=("$file")
    fi
}

# Main build function
build_all() {
    echo -e "${BLUE}=== Building MVA ML Graphs Lecture Slides ===${NC}\n"

    # Build main combined lecture files
    echo -e "${YELLOW}Building main combined lectures...${NC}"
    for i in 0 1 2 3 4 5 6; do
        if [ -f "$i/mlgraphs$i.tex" ]; then
            compile_file "$i/mlgraphs$i.tex"
        fi
    done

    # Build individual topic files by directory
    for dir in 1 2 3 4 5 6 7 8; do
        if [ ! -d "$dir" ]; then
            continue
        fi

        topic_files=("$dir"/mlgraphs-*.tex)
        if [ -e "${topic_files[0]}" ]; then
            echo -e "\n${YELLOW}Building topic files in directory $dir...${NC}"
            for file in "${topic_files[@]}"; do
                compile_file "$file"
            done
        fi
    done

    # Summary
    echo -e "\n${BLUE}=== Build Summary ===${NC}"
    echo -e "${GREEN}Successful: $SUCCESS_COUNT${NC}"
    echo -e "${RED}Failed: $FAIL_COUNT${NC}"

    if [ $FAIL_COUNT -gt 0 ]; then
        echo -e "\n${RED}Failed files:${NC}"
        for file in "${FAILED_FILES[@]}"; do
            echo "  - $file"
        done
    fi
}

# Parse arguments
if [ "$1" == "--clean-only" ]; then
    clean_aux_files
    exit 0
fi

# Run build
build_all

# Clean up auxiliary files after build
echo ""
clean_aux_files

echo -e "\n${GREEN}✓ Build complete!${NC}"
