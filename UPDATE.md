# Autoquant update

The goal is to update your internal prompts with the latest knowledge on the autoquant framework by reviewing the docs diffs.

README.md serves as the single source of truth of how autoquant works. The goal is to find any diff

Running an autoquant update works by detecting deltas in your prompts vs latest autoquant setup/readme docs, updating your prompts to fix the deltas. Any local markdown prompt is fair game to edit to make you up to date.

1) Run:
   autoquant get-readme-diff
   autoquant get-update-diffs
   Check what changes where made to docs
2) make a list of diffs with impact analysis on your current prompts.
3) make a concrete list of changes to make to your own prompts and knowledge base. 
update user on progress so far and wait for approval before making changes.

4) when ready to make an update, run:
   ```bash
   autoquant run-update
   autoquant --help
   autoquant get-openapi
   ```
   
5) Update your prompts with the latest knowledge and CLI commands and API endpoints as planned in step 3