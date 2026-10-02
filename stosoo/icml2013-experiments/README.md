# Historical StoSOO ICML 2013 experiments

Historical MATLAB research code associated with:

**Stochastic Simultaneous Optimistic Optimization**  
Michal Valko, Alexandra Carpentier, Rémi Munos  
International Conference on Machine Learning (ICML), 2013

Paper: https://misovalko.github.io/publications/valko2013stochastic.pdf

This snapshot was recovered from Michal Valko's research archive and preserves the paper-era experiment drivers together with the matching MATLAB implementations:

- `icml2013.m` — experiment and plotting driver used around the ICML 2013 work
- `example_icml.m` — smaller experiment example
- `oo.m` — historical SOO/StoSOO implementation variant
- `stoo.m` — historical stochastic implementation variant

The experiment scripts use MATLAB built-ins and run with low verbosity by default. Higher-verbosity visualization paths in `oo.m` / `stoo.m` refer to historical drawing helpers that are preserved separately in the existing `../oo_v1.zip` archive.

The recovered archive did not contain an explicit software license. This material is published as a historical/reproducibility snapshot; no additional license is asserted here.


## Legacy source history

The `legacy/` subfolder preserves additional paper-era implementation history that was not part of the small runnable snapshot above:

- `oo_old.m` — earlier OO implementation
- `stosoo1d.m` — earlier one-dimensional StoSOO implementation
- `stosoo_test.m` — historical experiment/test driver
- `draw_partition.m` — historical visualization helper

These files are kept for research-history and reproducibility context rather than as a maintained software package.
