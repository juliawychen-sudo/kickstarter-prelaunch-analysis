# Analysis notebook

Open [campaign_success.ipynb](campaign_success.ipynb) for the canonical executed analysis. It includes sample construction, descriptive checks, candidate models, cross-validation, historical test results, calibration, risk ranking and robustness checks.

For reproduction, follow the root README, put the source CSV in `data/raw/`, select the project Python kernel, and restart/run all cells. The final cell exports aggregate tables and run metadata into `results/`. The notebook can be launched from either the repository root or this folder.

The historical specification is retained for continuity with the original analysis. Read the feature-availability and validation caveats before interpreting the scores as prospective performance.
