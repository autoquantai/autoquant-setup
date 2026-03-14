# AutoQuant Install

## Environment variables

Persist environment variables in ~/.autoquant/.env (add or create)

MASSIVE_API_KEY=<your_massive_api_key>
AUTOQUANT_API_KEY=<your_autoquant_api_key>
AUTOQUANT_API_URL=<your_autoquant_api_url>

## Virtual env

```bash
mkdir -p "$HOME/.autoquant/venv"
python3 -m venv "$HOME/.autoquant/venv/autoquant"
```

## AutoQuant CLI

```bash
"$HOME/.autoquant/venv/autoquant/bin/pip" install "git+https://github.com/autoquantai/autoquant-cli.git@main"
```

## Shell launcher 

Create a persistent shell launcher (one-time) so `autoquant` works in every new bash session without venv activation.
   ```bash
   mkdir -p "$HOME/.local/bin"
   cat > "$HOME/.local/bin/autoquant" << 'EOF'
   #!/usr/bin/env bash
   exec "$HOME/.autoquant/venv/autoquant/bin/autoquant" "$@"
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