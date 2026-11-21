# Data source and reproduction

Download **ks-projects-201801.csv** from [Kickstarter Projects by Mickaël Mouillé](https://www.kaggle.com/datasets/kemical/kickstarter-projects). Place it in `data/raw/` (create that directory if needed). The source file contains 378,661 campaigns and 15 columns; the analysis retains 331,675 campaigns labeled `successful` or `failed`.

The source data card lists **CC BY-NC-SA 4.0**. This repository does not redistribute the source CSV or campaign-level predictions. The data license is separate from any rights in this project's code or writing; consult the original source for its terms. Aggregate result tables are provided for inspection.

`usd_goal_real` is a USD conversion of the goal using Fixer.io, credited by the data author to a conversion script by `tonyplaysguitar`. The data card does not establish a launch-time exchange rate. Similarly, this historical snapshot does not verify that titles and categories are unchanged since launch. Therefore, results describe retrospective prediction with launch-related attributes, not a fully audited point-in-time backtest.

The notebook prints the CSV's SHA-256 and records it in `results/run_summary.json`. Use that checksum to identify the exact input used for the published run.

## Sample and exclusions

- Successful campaigns are the positive class; failed campaigns are the negative class.
- Canceled, suspended, live, and undefined campaigns are excluded from the primary model.
- Canceled campaigns are scored separately in a sensitivity exercise, temporarily treating cancellation as failure without retraining.
- Pledged amounts, USD pledged amounts, backer counts, and final state are never predictors.
- IDs identify the common split; they are not model inputs.
- Missing titles are represented by empty strings; the malformed country label `N,0"` is retained as `Unknown`.

Source documentation checked on 21 November 2026. No claim is made that this historical dataset represents today's Kickstarter campaigns.
