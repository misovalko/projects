# Makefile for MVA Graphs in Machine Learning Slides
# Usage:
#   make all      - Compile all slide decks
#   make clean    - Remove build artifacts
#   make folder-N - Compile all slides in folder N (e.g., make folder-3)
#   make FILE     - Compile a specific file (e.g., make 3/mlgraphs-spectral-clustering-examples)

LATEX = lualatex
LATEXFLAGS = -interaction=nonstopmode

# Find all tex files (excluding common/ and local files)
TEXFILES := $(shell find . -maxdepth 2 -name "mlgraphs*.tex" -type f)
PDFFILES := $(TEXFILES:.tex=.pdf)

# Build artifacts to clean
CLEANEXT = aux log nav out snm toc bbl bcf blg run.xml fdb_latexmk fls synctex.gz

.PHONY: all clean folder-0 folder-1 folder-2 folder-3 folder-4 folder-5 folder-6 folder-7 folder-8 help

all: $(PDFFILES)
	@echo ""
	@echo "=== All slides compiled successfully! ==="
	@echo "Total PDFs: $$(find . -maxdepth 2 -name 'mlgraphs*.pdf' | wc -l | tr -d ' ')"

# Pattern rule for compiling tex to pdf.
# Always runs two passes: tikzpicture[remember picture, overlay] needs the
# first pass to record absolute positions in .aux, the second to use them.
# Without two passes the title-slide Isara logo silently disappears.
%.pdf: %.tex
	@echo "Compiling: $<"
	@cd $(dir $<) && $(LATEX) $(LATEXFLAGS) $(notdir $<) > /dev/null 2>&1 || \
		echo "  ERROR in $<"
	@cd $(dir $<) && $(LATEX) $(LATEXFLAGS) $(notdir $<) > /dev/null 2>&1 || true

# Folder-specific targets
folder-0:
	@$(MAKE) $(shell find 0 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

folder-1:
	@$(MAKE) $(shell find 1 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

folder-2:
	@$(MAKE) $(shell find 2 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

folder-3:
	@$(MAKE) $(shell find 3 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

folder-4:
	@$(MAKE) $(shell find 4 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

folder-5:
	@$(MAKE) $(shell find 5 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

folder-6:
	@$(MAKE) $(shell find 6 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

folder-7:
	@$(MAKE) $(shell find 7 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

folder-8:
	@$(MAKE) $(shell find 8 -name "mlgraphs*.tex" | sed 's/.tex/.pdf/')

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@find . -maxdepth 2 -type f \( $(foreach ext,$(CLEANEXT),-name "*.$(ext)" -o) -false \) -delete
	@echo "Done! Removed all build artifacts."

# Show help
help:
	@echo "MVA Slides Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make all        - Compile all slide decks"
	@echo "  make clean      - Remove build artifacts (aux, log, etc.)"
	@echo "  make folder-N   - Compile all slides in folder N (0-8)"
	@echo "  make FILE.pdf   - Compile a specific file"
	@echo ""
	@echo "Examples:"
	@echo "  make folder-3"
	@echo "  make 3/mlgraphs-spectral-clustering-examples.pdf"
	@echo ""
	@echo "Slide folders:"
	@echo "  0: Course intro"
	@echo "  1: Graph theory basics, similarity graphs"
	@echo "  2: Natural graphs, PageRank, random models"
	@echo "  3: Laplacians, spectral clustering"
	@echo "  4: Resistance, manifold learning"
	@echo "  5: Semi-supervised learning"
	@echo "  6: Sparsifiers, SSL bounds"
	@echo "  7: Large-scale, online SSL"
	@echo "  8: Bandits, submodularity"
