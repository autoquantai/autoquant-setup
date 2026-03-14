# Workflows

## Core Commands

- `autoquant --help`
- `autoquant <command> --help`
- `autoquant health`
- `autoquant create-experiment --name ... --input-ohlc-tickers ... --target-ticker ... --from-date ... --to-date ... --task ... --data-provider ... --ccxt-exchange ... --max-experiments ... --train-time-limit-minutes ... --refresh-data`
- `autoquant api <path> '<json>'`
- `autoquant validate-model --run-id ... --model-path ...`
- `autoquant run-model --run-id ... --name ... --generation ... --model-path ... --log ... --parent-ids ... --reasoning ... --task ...`
- `autoquant get-openapi`

For day-to-day research, prioritize `create-experiment`, `health`, `api`, `validate-model`, and `run-model`.

## API Action Space

- Treat `autoquant api` as a first-class action space for exploration and inspection.
- Fetch the API schema with `autoquant get-openapi` at the start of a session or when endpoint support is unclear.
- Use the OpenAPI output to discover valid endpoints and payload shapes before calling unknown routes.

## Research Loop

Assume the experiment (`run_id`) already exists. 
Ensure the backend contract is current with `autoquant get-openapi`.

Repeat until the stop condition is reached:

- Check environment and backend health with `autoquant health`.
- Inspect experiment metadata with `autoquant api /run/get`.
- Review prior model experiments with `autoquant api /experiment/get`.
- Fetch the run graph for lineage context with `autoquant api /run/graph/get '{"run_id":"<run_id>"}'`.
- Use your learning context to decide the next generation as `N` candidate models that target different hypotheses.
- For each candidate model, choose up to 2 parents from strong prior models in the graph.
- For root nodes, set `parent_ids` to `null` (or `[]`) in the run payload.
- Parent models can come from the previous generation or any earlier part of the tree.
- Start from `seed_train.py` for classification or strong validated prior models and write all candidate model files locally.
- Validate each candidate with `autoquant validate-model --run-id ... --model-path ...`.
- Treat validation as a sandbox smoke test, not the full training search.
- Execute each candidate with `autoquant run-model --run-id ... --name ... --generation ... --model-path ... --log ... --parent-ids ... --reasoning ...`.
- Review all model experiments from the generation together and compare against prior generations and results vs expected results.
- Write the generation report through the API with `autoquant api /report/create '{"run_id":"<run_id>","generation":<generation>,"content_md":"..."}'`.
- Stop when objective quality plateaus or the run has enough generations.
- Save transferrable findings for future runs.

## Canonical Terms

- Experiment: the top-level optimization process identified by `run_id`.
- Generation: a batch inside an experiment.
- Model experiment: one model candidate evaluated inside a generation.

## Experiment Graph Semantics

- A run consists of multiple generations.
- A generation consists of multiple model experiments evaluated together.
- A model experiment may have zero, one, or two parents.
- A model's parents can be selected from the immediate prior generation or any earlier generation.
- The agent should choose generation size `N` based on search needs and available budget, while preferring `N >= 2` for exploration breadth.

## Experiment Lifecycle

### Create

`create-experiment` validates the date range and market config before creating the experiment. After the experiment is created, it prepares local experiment data and writes:

- `AUTOQUANT_WORKSPACE/runs/<run_id>/data/ohlcv.csv`
- `AUTOQUANT_WORKSPACE/runs/<run_id>/data/run_dataset.csv`

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
