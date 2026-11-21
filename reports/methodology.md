# Design and interpretation

## Question

How much historical predictive information is contained in campaign attributes associated with the launch decision, and how much comes from richer inputs versus a more flexible classifier?

This is a retrospective classification study, not an estimate of the effect of changing a goal or offering campaign support.

## Comparison design

The primary sample contains campaigns marked successful or failed. A fixed stratified 80/20 split of campaign IDs (`random_state=42`) keeps the train/test observations identical across classifiers. Failure is the majority-class baseline. Accuracy, precision, recall, F1 and ROC-AUC are reported; ROC-AUC is the selection metric.

The baseline input set contains main category, log USD funding goal, duration, country, currency, launch year and month. The expanded set adds sub-category and title character/word counts. The notebook compares logistic regression, Random Forest and XGBoost across both input sets on common five-fold training splits. The forest settings are selected with a small grid; XGBoost candidates vary depth and boosting rounds.

The notebook preserves the original historical analysis specification, including dummy encoding of the full feature table. Labels are not used to define that vocabulary. A deployment implementation would instead fit preprocessing inside training folds and explicitly handle unknown categories.

## What the validation does and does not establish

- **Random holdout:** gives a common historical comparison. Earlier notebook versions examined scores on this split; presenting the final score after CV does not restore a completely untouched test set.
- **Cross-validation:** supports candidate selection. Forest tuning and subsequent comparison reuse training folds, so these are non-nested selection scores, not unbiased estimates of the full search procedure.
- **Calibration:** compares observed outcomes with predicted probabilities in the historical test set. It does not demonstrate calibration in a future population.
- **Ablation:** removes input families and repeats CV with the selected XGBoost settings. It measures conditional predictive contribution, not causation. Substitutable features can mask one another's value.
- **Paired bootstrap:** resamples test campaigns with predictions fixed. The intervals describe test-sample uncertainty conditional on fitted models; they omit retraining and selection uncertainty. The forest comparator uses baseline inputs, while the logistic comparator uses expanded inputs.
- **Temporal robustness:** trains through 2016 and evaluates 2017 without year indicators. Since the chosen specification was developed using observations including 2017, this is not a pristine prospective test. The random-split comparison also removes year indicators.
- **Cancellation sensitivity:** applies the already fitted model to canceled campaigns. It does not establish that cancellation and funding failure have identical causes.

## Decision interpretation

A high observed failure rate among low-scoring campaigns shows risk concentration. It does not show that those campaigns benefit most from coaching or that coaching improves funding outcomes. Review-capacity tables describe hypothetical selections in historical data; no campaign in this analysis received an experimental intervention. A prospective test and randomized pilot within risk bands would be needed to evaluate support allocation.

## Provenance

Wanyu (Julia) Chen independently completed the data preparation, modelling, validation, interpretation and original deliverables. The project originated in Business Analytics Using Python at HEC Paris. This public edition focuses the original analysis, consolidates reproduction instructions, exports aggregate evidence and makes the validation limitations explicit. It is a personal portfolio project, not a publication or deployed product.
