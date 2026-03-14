# Model Rules

## Model Contract

Model files must contain exactly one concrete subclass of `AutoQuantModel`.

- Implement `create_features(frame)` and return `(prepared_frame, feature_names)`.
- Optionally implement `get_hyperparameter_candidates()`.
- Implement `fit(x_train, y_train, hyperparams)`.
- Implement `predict(x_test)`.
- Keep the file class-only.
- Do not add `argparse`, `main()`, `if __name__ == "__main__"`, or `TRAIN_OUTPUT`.
- The runtime must discover exactly one concrete subclass from that file.
- Model execution output must be exactly `{train, validation}` and both values must be dicts.

Validation or execution fails if:

- the file contains zero concrete subclasses
- the file contains more than one concrete subclass
- `fit(...)` or `predict(...)` is missing
- the output shape is not exactly `{train, validation}`
- `get_hyperparameter_candidates()` does not return a dict
- `predict(...)` returns a different length than the provided feature frame

Use `seed_train.py` as the baseline template for the canonical model signature.

## Hyperparameters

- `training_size_days` is reserved and injected automatically by the framework.
- Do not define `training_size_days` inside `get_hyperparameter_candidates()`.
- Sandbox validation samples one hyperparameter candidate.
- Full execution performs hyperparameter search across the model search space plus the automatic `training_size_days` search.

## Data Rules

- Training data is per-run OHLCV market data.
- Data source is `massive` or `ccxt`.
- Granularity is 1 hour candles.
- Local run data lives under `AUTOQUANT_WORKSPACE/runs/<run_id>/data/`.
- The local run directory contains `raw_prices.csv`, `prices.csv`, and `run_metadata.json`.
- `raw_prices.csv` stores long-form OHLCV rows with `timestamp`, `ticker`, `open`, `high`, `low`, `close`, `volume`.
- `prices.csv` stores the merged model dataset.
- The target ticker becomes canonical `open`, `high`, `low`, `close`, `volume` columns.
- Input ticker features are added as prefixed columns such as `msft_open` or `qqq_close`.
- Input ticker data is merged into the target timeline and the merged dataset must not lose more than 10% of target rows.
- Full training requires at least 220 merged rows.

## Validation And Execution

- `validate-model` is a sandbox check, not the full training workflow.
- Sandbox validation uses a small recent sample and sets `selected_hyperparams.training_size_days` to `3`.
- `run-model` is the full execution path and performs the full training and search workflow.

## Generation And Parent Rules

- Treat search as a generation graph, not a single linear sequence.
- Each generation is a group of multiple model experiments within one experiment (`run_id`).
- Generate `N` new models in each generation to test multiple ideas in parallel.
- Each model can have at most two parents.
- Parent models can be chosen from the previous generation or any earlier node in the graph.
- Choose parents that maximize expected objective improvement based on historical experiment results.

## Metrics And Results

- Failed experiments store `error` and may include `runtime_error`, `stdout`, and `stderr`.
- Completed experiments store `evals.train` and `evals.validation`.
- Classification selection metric is weighted-average F1.
- Regression selection metric is `r2`.
