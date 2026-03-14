# Workflows

## Core Commands

- `autoquant --help`
- `autoquant <command> --help`
- `autoquant health`
- `autoquant create-experiment --name ... --input-ohlc-tickers ... --target-ticker ... --from-date ... --to-date ... --task ... --data-provider ...`
- `autoquant api <path> '<json>'`
- `autoquant validate-model --run-id ... --model-path ...`
- `autoquant run-model --run-id ... --name ... --generation ... --model-path ... --log ...`
- `autoquant get-openapi`

For day-to-day research, prioritize `create-experiment`, `health`, `api`, `validate-model`, and `run-model`.

## Research Loop

Repeat until the stop condition for a given `run_id`:

1. Check environment and backend health with `autoquant health`.
2. Create the run with `autoquant create-experiment --name ... --input-ohlc-tickers ... --target-ticker ... --from-date ... --to-date ... --task ...`.
3. Let `create-experiment` materialize local run data under `AUTOQUANT_WORKSPACE/runs/<run_id>/data/`.
4. Inspect the run with `autoquant api /run/get`.
5. Review past experiments with `autoquant api /experiment/get`.
6. Start from `seed_train.py` or the strongest validated prior model and write the next candidate model file locally.
7. Validate it with `autoquant validate-model --run-id ... --model-path ...`.
8. Treat validation as a sandbox smoke test, not the full training search.
9. Execute the candidate with `autoquant run-model --run-id ... --name ... --generation ... --model-path ... --log ...`.
10. Review the created experiment and compare it with prior attempts.
11. Stop when experiment quality stops improving or the run has enough attempts.
12. Save transferrable findings for future runs.

## Run Lifecycle

### Create

`create-experiment` validates the date range and market config before creating the run. After the run is created, it prepares local run data and writes:

- `AUTOQUANT_WORKSPACE/runs/<run_id>/data/raw_prices.csv`
- `AUTOQUANT_WORKSPACE/runs/<run_id>/data/prices.csv`
- `AUTOQUANT_WORKSPACE/runs/<run_id>/data/run_metadata.json`

Use `--data-provider massive` for the default market data path or `--data-provider ccxt --ccxt-exchange ...` for exchange-backed crypto data.

### Inspect

Use `autoquant api` for inspection. The CLI accepts both `/run/get` and `run/get` style paths.

Inspect one run:

```bash
autoquant api /run/get '{"run_ids":["<run_id>"],"page":1,"limit":1,"sort_by":"created_at","sort_order":"desc"}'
```

Inspect prior experiments for a run:

```bash
autoquant api /experiment/get '{"run_id":"<run_id>","page":1,"limit":20,"sort_by":"created_at","sort_order":"desc"}'
```

### Validate

`validate-model` is a sandbox execution path. It uses local run data, samples a small recent slice, tries one sampled hyperparameter candidate, and returns a validation payload quickly.

Use it to catch contract, feature, prediction, and runtime problems before spending time on a full execution.

### Execute

`run-model` is the full execution path. It ensures local run data exists, runs the full training workflow, performs hyperparameter search, then posts the experiment with source code, selected hyperparameters, evals, and any runtime error details.

## Operating Defaults

- Prefer the CLI over ad hoc scripts.
- Inspect prior experiments before proposing a new model direction.
- Keep each iteration tied to a clear hypothesis.
- Treat `validate-model` as a fast gate before `run-model`.
- Use `autoquant api` for read-only inspection and `autoquant` commands for the main workflow.
- Store transferrable findings after each meaningful learning step.
