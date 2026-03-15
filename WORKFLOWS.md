# Workflows

## Core Commands

 `autoquant --help` to get the list of commands and `autoquant <command> --help` to get the command contract/signature

## Folder structure

Each run has its own folder under "$AUTOQUANT_WORKSPACE/runs/<run-id>". It contains:
- data: the raw and dataset we're working with
- models: all your candidate models.

## API endpoints

- Use `autoquant api get-api-specs` at the start of a session to discover available endpoint paths and business docs.
- Use `autoquant api` for inspection and allowed backend actions.
- Create runs only with `autoquant create-experiment`.
- Create model experiments only with `autoquant run-model`.

## Research Loop

Check app health with `autoquant health`. Check API spec with `autoquant api get-api-specs`
and inspect endpoint contracts with `autoquant api <endpoint>/spec.json`.

Repeat until the stop condition is reached:

while True:
    
    - Inspect run status with `autoquant api /run/get_status`.

    if completed experiments < max_experiments:
        continue
    else:
        stop


    if this is the root/seed experiment:
        For root nodes, set `parent_ids` to `null` (or `[]`) in the run payload.
        - Start from `seed_train.py` for classification or use linear regression for regression. 
    else:
        - Fetch the run graph for lineage context with `autoquant api /run/get_graph`.
        - Use your learning context to decide the next generation as `N` candidate models that target different hypotheses. 
        Each candidate model from the next generation must inherited parent_id from up to 2 experiments from any part of the learning graph
        Candidate models must be saved under models/ in your run folder

        - Validate each candidate with `autoquant validate-model`.
        - Treat validation as a sandbox smoke test, not the full training search.
        - Execute each candidate with `autoquant run-model`.
        - Write a report on this new generation using `autoquant api /report/create
        


## Canonical Terms

- Experiment: the top-level optimization process identified by `run_id`.
- Generation: a batch inside an experiment.
- Model experiment: one model candidate evaluated inside a generation.

## Experiment Graph Semantics

- A run consists of multiple generations.
- A generation consists of multiple model experiments 
- A model experiment may have zero (seed/root), one, or two parents.
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
- Use `autoquant api` for inspection and supported backend actions.
- Use CLI commands as the only creation path for runs and model experiments.
- Store transferrable findings after each meaningful learning step.
