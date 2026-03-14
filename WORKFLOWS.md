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

Repeat until the stop condition for a given experiment (`run_id`):

1. Check environment and backend health with `autoquant health`.
2. Create the experiment with `autoquant create-experiment --name ... --input-ohlc-tickers ... --target-ticker ... --from-date ... --to-date ... --task ...`.
3. Let `create-experiment` materialize local experiment data under `AUTOQUANT_WORKSPACE/runs/<run_id>/data/`.
4. Inspect experiment metadata with `autoquant api /run/get`.
5. Review prior model experiments with `autoquant api /experiment/get`.
6. Plan the next generation as `N` candidate models that target different hypotheses.
7. For each candidate model, choose 0-2 parents from strong prior models in the graph.
8. Parent models can come from the previous generation or any earlier part of the tree.
9. Start from `seed_train.py` or strong validated prior models and write all candidate model files locally.
10. Validate each candidate with `autoquant validate-model --run-id ... --model-path ...`.
11. Treat validation as a sandbox smoke test, not the full training search.
12. Execute each candidate with `autoquant run-model --run-id ... --name ... --generation ... --model-path ... --log ...`.
13. Review all model experiments from the generation together and compare against prior generations.
14. Stop when objective quality plateaus or the run has enough generations.
15. Save transferrable findings for future runs.

## Canonical Terms

- Experiment: the top-level optimization process identified by `run_id`.
- Generation: a batch inside an experiment.
- Model experiment: one model candidate evaluated inside a generation.

## Experiment Graph Semantics

- An experiment consists of multiple generations.
- A generation consists of multiple model experiments evaluated together.
- A model experiment may have zero, one, or two parents.
- A model's parents can be selected from the immediate prior generation or any earlier generation.
- The agent should choose generation size `N` based on search needs and available budget, while preferring `N >= 2` for exploration breadth.

## Experiment Lifecycle

### Create

`create-experiment` validates the date range and market config before creating the experiment. After the experiment is created, it prepares local experiment data and writes:

- `AUTOQUANT_WORKSPACE/runs/<run_id>/data/raw_prices.csv`
- `AUTOQUANT_WORKSPACE/runs/<run_id>/data/prices.csv`
- `AUTOQUANT_WORKSPACE/runs/<run_id>/data/run_metadata.json`

Use `--data-provider massive` for the default market data path or `--data-provider ccxt --ccxt-exchange ...` for exchange-backed crypto data.

### Inspect

Use `autoquant api` for inspection. The CLI accepts both `/run/get` and `run/get` style paths.

Inspect one experiment:

```bash
autoquant api /run/get '{"run_ids":["<run_id>"],"page":1,"limit":1,"sort_by":"created_at","sort_order":"desc"}'
```

Inspect prior model experiments for an experiment:

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
