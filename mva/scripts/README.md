# MVA Slides Automation Scripts

This directory contains all automation scripts for building, maintaining, and enhancing the MVA Graphs in Machine Learning course slides.

## Directory Structure

```
scripts/
├── build/              # Compilation and content generation
│   ├── build_all.sh              - Compile all LaTeX slides
│   ├── generate_thumbnails.py    - Create PDF preview images
│   ├── generate_thumbnails.sh    - Shell version (deprecated)
│   └── optimize_pdfs.sh          - Compress PDF files
├── web/                # HTML and web enhancements
│   ├── add_accessibility.py      - Add ARIA labels (one-time)
│   ├── add_pdf_sizes.py          - Add file sizes to links (one-time)
├── maintenance/        # Code cleanup and quality
│   └── clean_comments.py         - Remove dead commented code
├── analyze_subdecks.py    - Subdeck analysis
├── clean_subdecks.py      - Content cleanup
├── extract_subdecks_v2.py - Subdeck extraction
└── README.md              # This file
```

## Quick Start

### Build All Slides
From the project root (`projects/mva`):
```bash
./scripts/build/build_all.sh
```

### Generate Thumbnails
```bash
python3 scripts/build/generate_thumbnails.py
```

## Build Scripts

### `build/build_all.sh`
Compiles all LaTeX presentations and cleans auxiliary files.

**Features:**
- Compiles main combined lectures (mlgraphs0-6.tex)
- Compiles individual topic files in all directories
- Colored output (✓ success, ✗ failure)
- Automatic cleanup of .aux, .log, etc.
- Error reporting with file list

**Usage:**
```bash
./scripts/build/build_all.sh              # Full build
./scripts/build/build_all.sh --clean-only # Just clean
```

**Output:**
- Success count and failure count
- List of failed files (if any)
- Cleaned auxiliary files message

---

### `build/generate_thumbnails.py`
Generates JPEG preview images of first page of each PDF.

**Features:**
- Uses Ghostscript for high-quality rendering
- 450x600px at 150 DPI
- 85% JPEG quality
- Generates ~30 thumbnails

**Requirements:**
- Ghostscript (`gs` command)

**Output:** Thumbnails in `materials/slides/thumbnails/` directory (relative to slides)

**Example:**
```bash
python3 scripts/build/generate_thumbnails.py
# Creates: mlgraphs0-thumb.jpg, mlgraphs-introduction-thumb.jpg, etc.
```

---

### `build/optimize_pdfs.sh`
Compresses PDF files using Ghostscript to reduce file sizes.

**Features:**
- Screen-quality settings (suitable for presentations)
- Only replaces if compressed version is smaller
- Reports savings percentage
- Dry-run mode available

**Usage:**
```bash
./scripts/build/optimize_pdfs.sh --dry-run    # Preview
./scripts/build/optimize_pdfs.sh              # Execute
```

**Settings:**
- Resolution: 150 DPI (color, gray, mono)
- Downsampling: Bicubic
- Embeds and subsets all fonts

**Warning:** Test on a few files first as quality may be reduced for complex graphics.

## Web Enhancement Scripts

### `web/add_accessibility.py`
One-time script to add accessibility features to HTML.

**Features:**
- Adds descriptive aria-labels to all PDF links
- Adds `download` attribute to links
- Format: `aria-label="Title, Size PDF. Description"`

**Usage:**
```bash
python3 scripts/web/add_accessibility.py
```

**Note:** Already run. Only needed if HTML structure changes.

---

### `web/add_pdf_sizes.py`
One-time script to add file sizes to HTML links.

**Features:**
- Scans all PDFs and gets file sizes
- Adds formatted sizes (e.g., "1.3MB", "450KB")
- Injects CSS for styling
- Right-aligned with consistent width

**Usage:**
```bash
python3 scripts/web/add_pdf_sizes.py
```

**Note:** Already run. Only needed for new PDFs or structure changes.

## Maintenance Scripts

### `maintenance/clean_comments.py`
Removes large blocks of commented-out code from LaTeX files.

**Features:**
- Preserves TeX directives (`% !TEX`)
- Preserves section separators
- Preserves documentation comments
- Removes commented `\begin{frame}` blocks
- Statistics reporting

**Usage:**
```bash
python3 scripts/maintenance/clean_comments.py --dry-run  # Preview
python3 scripts/maintenance/clean_comments.py            # Execute
```

**Example Output:**
```
Cleaned mlgraphs-graphlab-abstraction.tex: removed 552 comment lines
Cleaned mlgraphs-ssl-transductive-bounds.tex: removed 92 comment lines
...
Summary:
  Files cleaned: 33
  Total lines removed: 1219
```

## Common Workflows

### Complete Build
From `projects/mva`:

```bash
# 1. Compile all slides
./scripts/build/build_all.sh

# 2. Generate thumbnails
python3 scripts/build/generate_thumbnails.py

# 3. (Optional) Optimize PDFs
./scripts/build/optimize_pdfs.sh --dry-run
./scripts/build/optimize_pdfs.sh
```

### After Adding New Slides

```bash
# Compile the new slide (example for Lecture 3)
cd materials/slides/3/
lualatex -interaction=nonstopmode new-slide.tex

# Or rebuild everything from root
cd ../../../..
./scripts/build/build_all.sh

# Update thumbnails
python3 scripts/build/generate_thumbnails.py
```

### Code Cleanup
```bash
# Preview cleanup
python3 scripts/maintenance/clean_comments.py --dry-run

# Execute cleanup
python3 scripts/maintenance/clean_comments.py

# Rebuild after cleanup
./scripts/build/build_all.sh
```

## Requirements

### System Dependencies
- **LuaLaTeX** - For compiling .tex files
- **Ghostscript (gs)** - For PDF operations and thumbnails
- **Python 3** - For Python scripts
- **Bash** - For shell scripts

### Checking Dependencies
```bash
which lualatex  # Should return path
which gs        # Should return path
which python3   # Should return path
```

### LaTeX Packages
All required packages are specified in `common/misomva.tex`:
- beamer
- tikz
- biblatex
- graphicx
- textpos
- And others...

## Troubleshooting

### Build Script Fails
**Issue:** `lualatex: command not found`
**Solution:** Install TeX Live or MacTeX

**Issue:** Some files fail to compile
**Solution:** Check error logs in corresponding .log files

### Thumbnail Generation Fails
**Issue:** `gs: command not found`
**Solution:** Install Ghostscript
```bash
# macOS
brew install ghostscript

# Linux
sudo apt-get install ghostscript
```

### Python Script Fails
**Issue:** Import errors
**Solution:** Scripts use only standard library, check Python version (3.6+)

## File Permissions

All scripts should be executable:
```bash
chmod +x scripts/build/*.sh
chmod +x scripts/maintenance/*.py
chmod +x scripts/web/*.py
```

## Best Practices

1. **Scripts work from project root**
   - Scripts are designed to be run from `projects/mva/`
   - They handle paths relative to their location

2. **Test with dry-run first**
   - Many scripts support `--dry-run` flag
   - Preview changes before executing

3. **Keep backups**
   - Scripts modify files in place
   - Git tracks changes, but be cautious

4. **Check build output**
   - Review success/failure counts
   - Investigate failed compilations

5. **Regular maintenance**
   - Run `clean_comments.py` after major edits
   - Update thumbnails for new slides

## Contributing

When adding new scripts:
1. Place in appropriate subdirectory (build/web/maintenance)
2. Add usage comment at top
3. Include in this README
4. Make executable (`chmod +x`)
5. Test thoroughly

## Support

For issues or questions:
- Check script comments and usage instructions
- Review error messages carefully

## License

These scripts are part of the MVA Graphs in Machine Learning course materials.
