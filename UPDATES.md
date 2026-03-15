# Updates

When asked to update this skill:

1. Clone `https://github.com/autoquantai/autoquant-setup` in the workspace only if if's not already there.
2. If already there, do a git diff of the local repo against latest version to check what has changed in the Autoquant framework and prompts, and what knowledge needs to be updated locally
4. Apply the required updates in your system prompts and memory. autoquant-setup repo is the latest source of truth of how Autoquant operates. It's important we keep the latest source of truth only in your own prompts and MEMORY.md as well.
5. Execute ```pip install --upgrade --force-reinstall "git+https://github.com/autoquantai/autoquant-cli.git``` from the correct virtual environment to update the cli
