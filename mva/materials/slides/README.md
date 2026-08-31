# MVA Graphs in Machine Learning - Slides

This directory contains the LaTeX source code and compiled PDFs for the "Graphs in Machine Learning" course at MVA/ENS Paris-Saclay.

## Structure

The slides are organized by lecture number (0-8):

- `0/` - **Overview**: Course logistics and introduction.
- `1/` - **Introduction**: Natural graphs, similarity graphs, graph theory basics.
- `2/` - **PageRank & Natural Graphs**: PageRank algorithm, random graph models, small-world phenomena.
- `3/` - **Graph Laplacian & Spectral Clustering**: Laplacians, random walks, spectral clustering (cuts, relaxation, examples).
- `4/` - **Manifold Learning**: Laplacian Eigenmaps, resistance networks, movie recommendations.
- `5/` - **SSL Foundations**: Semi-supervised learning, harmonic functions, regularization.
- `6/` - **SSL Advanced & Sparsification**: Generalization bounds, LapSVM, spectral/cut sparsifiers.
- `7/` - **Online SSL & Large Scale**: Online learning, quantization, distributed processing (GraphLab).
- `8/` - **Advanced Topics**: Submodularity, graph bandits, influence maximization.

## Lecture 8: Advanced Topics Detail

- **Submodularity: Theory**
  Submodular functions: diminishing returns property. Greedy algorithm with (1-1/e) approximation guarantee.
- **Submodularity: Applications**
  Product placement on social networks: flip coins for "live" edges. Greedy outperforms centrality measures.
- **Graph Bandits**
  Graph bandits: actions are nodes, learners observe neighboring losses. Graph structure enables faster learning.
- **Spectral Bandits**
  Spectral bandits: Laplacian eigenvectors reduce dimension from N to d. SpectralUCB algorithm, regret bounds.
- **Influence Maximization**
  Influence maximization as revealing graph bandit. BARE algorithm achieves better regret bounds.

## Building

Use the Makefile to build slides:

```bash
# Build all slides
make all

# Build a specific folder
make folder-3

# Build a specific slide deck
make 3/mlgraphs-spectral-clustering-examples.pdf

# Clean build artifacts
make clean

# Show help
make help
```

Requires LuaLaTeX (included in TeX Live).

## Common Files

- `common/` - Contains shared resources:
  - `misomva.tex` - Main style file/preamble.
  - `library.bib` - Global bibliography.
  - Logos and colors.

## Images

- `img/` - Contains shared images and TikZ figures used across multiple decks.
