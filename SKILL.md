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
- Use this skill when the user wants to run research on a `run_id`, inspect prior runs or experiments, validate a model candidate, or execute a full training pass.
- Use this skill when the user wants to debug AutoQuant environment, CLI, or backend connectivity issues.
- Use this skill when the user wants the AutoQuant research style or agent personality applied during model iteration.

## Workflow

1. Decide whether the task is setup, experiment work, model work, or inspection.
2. Read only the reference file needed for that task.
3. Ask the user for any missing secrets, run identifiers, dates, tickers, or task settings instead of inventing them.
4. Prefer the current `autoquant` CLI over ad hoc scripts or manual backend calls.
5. Inspect the run and prior experiments before proposing a new model direction.
6. Use `seed_train.py` or a previously validated model as the baseline template for the next candidate.
7. Treat `validate-model` as a sandbox check and `run-model` as the full execution path.
8. Report environment, CLI, validation, or backend issues clearly to the user.

## References

- Setup and installation: [SETUP.md](SETUP.md)
- Research commands and loop: [WORKFLOWS.md](WORKFLOWS.md)
- Model contract, data rules, and metrics: [MODEL_RULES.md](MODEL_RULES.md)
- Baseline starter model: [seed_train.py](seed_train.py)
- Durable knowledge placement: [KNOWLEDGE_FILES.md](KNOWLEDGE_FILES.md)
- Identity and role: [IDENTITY.md](IDENTITY.md)

## Non-Negotiables

- Follow the research loop when iterating on a run.
- Use `seed_train.py` or a previously validated model as the baseline template.
- Never edit installed package source code inside `site-packages`.
- Prefer inspection through `autoquant api` before changing model direction.
- Distinguish sandbox validation from full training and search.
- Report CLI, backend, or virtualenv issues to the user instead of papering over them.
