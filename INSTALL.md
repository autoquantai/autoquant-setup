# AutoQuant Install

## Environment variables

Use `AUTOQUANT_WORKSPACE` as the single workspace root. If you do not set it, the CLI defaults to `~/.nanobot/workspace/autoquant`.

```bash
export AUTOQUANT_WORKSPACE="${AUTOQUANT_WORKSPACE:-$HOME/.nanobot/workspace/autoquant}"
mkdir -p "$AUTOQUANT_WORKSPACE"
```

Persist environment variables in `$AUTOQUANT_WORKSPACE/.env` (add or create)

MASSIVE_API_KEY=<your_massive_api_key>
AUTOQUANT_API_KEY=<your_autoquant_api_key>
AUTOQUANT_API_URL=<your_autoquant_api_url>

## Virtual env

```bash
mkdir -p "$AUTOQUANT_WORKSPACE/venv"
python3 -m venv "$AUTOQUANT_WORKSPACE/venv/autoquant"
```

## AutoQuant CLI

```bash
"$AUTOQUANT_WORKSPACE/venv/autoquant/bin/pip" install "git+https://github.com/autoquantai/autoquant-cli.git@main"
```

## Shell launcher 

Create a persistent shell launcher (one-time) so `autoquant` works in every new bash session without venv activation.
   ```bash
   mkdir -p "$HOME/.local/bin"
   cat > "$HOME/.local/bin/autoquant" << 'EOF'
   #!/usr/bin/env bash
   export AUTOQUANT_WORKSPACE="${AUTOQUANT_WORKSPACE:-$HOME/.nanobot/workspace/autoquant}"
   exec "$AUTOQUANT_WORKSPACE/venv/autoquant/bin/autoquant" "$@"
   EOF
   chmod +x "$HOME/.local/bin/autoquant"
   grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
   source "$HOME/.bashrc"
   ```

## Verify 

Verify env and backend connectivity.

```bash
autoquant health
```

## Update your identity

Read the README.md and bootstrap yourself as AutoQuant.