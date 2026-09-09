# Michal Valko — Research Projects and Archives

Public project, course, thesis, code, and archival materials by **Michal Valko**, a French-Slovak AI researcher and computer scientist working on reinforcement learning, LLM alignment, self-supervised learning, and bandit algorithms.

[Personal website](https://misovalko.github.io/) · [Google Scholar](https://scholar.google.com/citations?user=jrazNCQAAAAJ&sortby=pubdate) · [ORCID](https://orcid.org/0009-0009-2673-0144) · [GitHub](https://github.com/misovalko)

This repository is the canonical home for files served under:

`https://misovalko.github.io/projects/`

The main website source and the curated projects overview live in `misovalko/misovalko.github.io`. This repository owns the underlying project and archival files.

## Contents

The repository includes research project material, course archives, thesis material, older software and code, historical university work, and other public archival assets that are too large or too independent to belong in the main website repository.

## Publishing

GitHub Pages publishes this repository directly as static files. `.nojekyll` is intentional so historical directories and files are served without Jekyll processing.

Because `.nojekyll` is intentional, HTML in this repository must not depend on Jekyll/Liquid rendering. In particular, the MVA course pages are static Pages content. Their structured archive metadata remains canonical in the main website repository and is exposed publicly by the main site at `/mva-archive-data.json` for the static year pages to consume.

The `Static Pages template guard` workflow rejects Liquid/Jekyll expressions in MVA HTML so template source cannot accidentally be published literally again.

Existing paths should be treated as stable public URLs. Avoid renaming or reorganizing archival directories unless the corresponding links in the main website are updated at the same time.

## Relationship to the website

The public URL prefix remains `/projects/` even though the files are maintained in this independent repository. The main website intentionally does not contain a `projects/` tree or a Git submodule for this repository.

Publication PDFs, BibTeX, talks, and posters belong in `misovalko/publications`, not here.
