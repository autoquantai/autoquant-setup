---
name: autoquant-setup
description: Set up and operate AutoQuant as an autonomous research agent through the current CLI for workspace bootstrap, health checks, experiment creation, run inspection, model validation, and full model execution. Use when the user wants an AutoQuant-style agent to run research, improve a model, inspect prior experiments, configure the workspace, or debug CLI and backend workflow issues.
compatibility:
  os: [linux, macos]
  tools: [bash, python3, git]
  network: true
metadata:
  repo: https://github.com/autoquantai/autoquant-cli/tree/main
---

# AutoQuant Setup

Use this skill to bootstrap and operate AutoQuant as an autonomous quantitative research agent through the CLI.

## When To Use

- Use this skill when the user wants to install or reinstall AutoQuant.
- Use this skill when the user wants to configure `AUTOQUANT_WORKSPACE` or required API keys.
- Use this skill when the user wants to run research on an experiment (`run_id`), inspect prior generations and model experiments, validate a model candidate, or execute a full training pass.
- Use this skill when the user wants to debug AutoQuant environment, CLI, or backend connectivity issues.
- Use this skill when the user wants the AutoQuant research style or agent personality applied during model iteration.

## Workflow

1. Decide whether the task is setup, experiment work, model work, or inspection.
2. Read only the reference file needed for that task.
3. Ask the user for any missing secrets, run identifiers, dates, tickers, or task settings instead of inventing them.
4. Prefer the current `autoquant` CLI over ad hoc scripts or manual backend calls.
5. Inspect the experiment graph and prior model experiments before proposing a new model direction.
6. Use `seed_train.py` or a previously validated model as the baseline template.
7. Build each new generation as a set of `N` model candidates, not a single model.
8. Select each candidate's parent set from the model graph with at most two parents per model.
9. Prefer parents from strong prior models; parents can come from the previous generation or any earlier part of the tree.
10. Treat `validate-model` as a sandbox check and `run-model` as the full execution path.
11. Report environment, CLI, validation, or backend issues clearly to the user.
12. Use `autoquant get-api-specs` and endpoint-level specs (`GET <endpoint>/spec.json`) to discover route contracts.

## References

- Setup and installation: [SETUP.md](SETUP.md)
- Research commands and loop: [WORKFLOWS.md](WORKFLOWS.md)
- Model contract, data rules, and metrics: [MODEL_RULES.md](MODEL_RULES.md)
- Baseline starter model: [seed_train.py](seed_train.py)
- Durable knowledge placement: [KNOWLEDGE_FILES.md](KNOWLEDGE_FILES.md)
- Identity and role: [IDENTITY.md](IDENTITY.md)

## Non-Negotiables

- Follow the research loop when iterating on an experiment.
- Use `seed_train.py` or a previously validated model as the baseline template.
- Make generation planning explicit: an experiment contains multiple generations, and each generation contains multiple model experiments.
- Generate multiple models per generation (`N >= 2` unless the user requests otherwise) to explore ideas in parallel.
- Keep parent links explicit for each generated model and enforce a maximum of two parents.
- Never edit installed package source code inside `site-packages`.
- Use `autoquant get-api-specs` to discover endpoint paths and business docs before using unfamiliar routes.
- Use endpoint-level specs (`GET <endpoint>/spec.json`) for payload and response contracts.
- Prefer inspection through `autoquant api` before changing model direction.
- Use CLI commands as the only creation path for runs and model experiments.
- Distinguish sandbox validation from full training and search.
- Report CLI, backend, or virtualenv issues to the user instead of papering over them.
