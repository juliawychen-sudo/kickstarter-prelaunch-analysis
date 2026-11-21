# Kickstarter pre-launch analysis

**Can launch-related campaign information predict crowdfunding success?**

A Python analysis of **331,675 completed Kickstarter campaigns**, comparing richer input information with model flexibility, then examining calibration, risk concentration, and robustness.

**[Read the project brief](reports/project_brief.pdf)** · **[Explore the executed notebook](notebooks/campaign_success.ipynb)** · **[Inspect the result tables](results/)**

## Results

All models use the same historical random test sample of 66,335 campaigns. The selected XGBoost specification uses sub-category and title-length features in addition to the baseline inputs.

| Model / input set | Accuracy | ROC-AUC |
|---|---:|---:|
| Majority-class baseline | 59.6% | 0.500 |
| Logistic regression / baseline | 65.4% | 0.690 |
| Tuned Random Forest / baseline | 66.9% | 0.718 |
| Logistic regression / expanded | 67.7% | 0.730 |
| Selected XGBoost / expanded | 69.8% | 0.761 |


- **Information matters alongside algorithms.** Common-fold comparisons separate the contribution of richer inputs from the choice of learner; expanded-input logistic regression is competitive with baseline-input boosted trees.
- **Risk ranking is more useful than a binary verdict.** Among the riskiest 20% of historical test campaigns, 90.2% failed. This is risk concentration, not evidence that coaching would improve their outcomes.
- **Validation goes beyond accuracy.** The notebook includes calibration (Brier score 0.1932), input-group ablation, paired bootstrap intervals, category-level results, and cancellation sensitivity. A 2017 temporal robustness check gives AUC 0.770; its specification was developed with observations including 2017, so it is not an untouched forecast.

## Data and methods

[Kickstarter Projects by Mickaël Mouillé](https://www.kaggle.com/datasets/kemical/kickstarter-projects): 378,661 raw campaigns; retain successful and failed outcomes for the primary binary target. Data source, exclusions, licensing and checksum details are in [data/README.md](data/README.md). Raw data are not redistributed.

The pipeline uses a fixed stratified 80/20 split, a majority baseline, logistic regression, Decision Tree, Random Forest and XGBoost. Forest settings and candidate specifications are compared using training-sample cross-validation. Pledged amounts, backer counts and other outcome variables are excluded as predictors.

Baseline inputs: main category, log USD goal, planned duration, country/currency and launch calendar. Expanded inputs add sub-category and title character/word counts. The [controlled comparison](results/input_algorithm_comparison.csv) holds either the learner or inputs fixed.

## Interpretation and limits

This is **retrospective prediction, not causal inference or a production-ready score**. The snapshot does not establish launch-time FX conversion or unchanged campaign attributes. Early development examined the same random test split, and training-fold tuning is non-nested. The notebook's final presentation does not remove that history. Results also omit creator history, campaign media and marketing reach, and may not generalize to current campaigns.

Risk can help motivate a review workflow; it does not identify who benefits most from support. Prospective evaluation and a randomized support pilot would be needed before making intervention claims. See [methodology and validation limits](reports/methodology.md).

## Reproduce

Tested with **Python 3.13.1**. The full run took approximately **12 minutes** on the machine used for this edition; runtime varies with hardware.

1. Download `ks-projects-201801.csv` from the linked dataset and put it in `data/raw/` (create the folder if needed).
2. From the repository root:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   python -m ipykernel install --user --name kickstarter --display-name "Python (Kickstarter)"
   jupyter lab notebooks/campaign_success.ipynb
   ```

   On Windows, activate with `.venv\Scripts\activate` instead.
3. Select **Python (Kickstarter)**, then restart the kernel and run all cells. The notebook writes aggregate evidence to `results/`; it does not export raw campaigns or fitted models.
4. Optional: rebuild the short PDF after the notebook finishes:

   ```bash
   python -m pip install -r reports/requirements.txt
   python reports/build_report.py
   ```

The [run summary](results/run_summary.json) records exact input SHA-256, package versions, sample sizes and headline metrics. The executed notebook includes outputs for inspection without rerunning.

## Repository guide

| Path | Purpose |
|---|---|
| `notebooks/campaign_success.ipynb` | One canonical analysis, including robustness checks |
| `results/` | Aggregate tables and run metadata |
| `reports/project_brief.pdf` | Three-page findings and limitations |
| `reports/methodology.md` | Design choices and validation caveats |
| `reports/build_report.py` | Rebuild the brief from exported results |
| `data/README.md` | Source, sample definition and data instructions |

## Author

**Wanyu (Julia) Chen** — independently completed the data preparation, modelling, validation, interpretation and original deliverables. Developed as part of *Business Analytics Using Python* at HEC Paris; curated here as a personal portfolio project.
