# Setup

## Workspace

Use `AUTOQUANT_WORKSPACE` as the single workspace root.

```bash
export AUTOQUANT_WORKSPACE="${AUTOQUANT_WORKSPACE:-$HOME/.nanobot/workspace/autoquant}"
mkdir -p "$AUTOQUANT_WORKSPACE"
```

AutoQuant loads environment variables from `AUTOQUANT_WORKSPACE/.env`.

## Required Env Vars

Persist required secrets in `$AUTOQUANT_WORKSPACE/.env` and ask the user for any missing values.

```bash
MASSIVE_API_KEY=<your_massive_api_key>
AUTOQUANT_API_KEY=<your_autoquant_api_key>
AUTOQUANT_API_URL=<your_autoquant_api_url>
```

## Install

```bash
mkdir -p "$AUTOQUANT_WORKSPACE/venv"
python3 -m venv "$AUTOQUANT_WORKSPACE/venv/autoquant"
"$AUTOQUANT_WORKSPACE/venv/autoquant/bin/pip" install "git+https://github.com/autoquantai/autoquant-cli.git@main"
```

Use the installed CLI as the primary interface. Do not edit package source inside the virtualenv.

## Launcher

Create a stable launcher so `autoquant` works in fresh bash sessions.

```bash
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/autoquant" <<'EOF'
#!/usr/bin/env bash
export AUTOQUANT_WORKSPACE="${AUTOQUANT_WORKSPACE:-$HOME/.nanobot/workspace/autoquant}"
exec "$AUTOQUANT_WORKSPACE/venv/autoquant/bin/autoquant" "$@"
EOF
chmod +x "$HOME/.local/bin/autoquant"
grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
source "$HOME/.bashrc"
```

## Verify

```bash
autoquant health
```

Healthy output should confirm:

- `status`
- `env_vars_ok`
- `env_file`
- `env_file_exists`
- `backend`

If health fails, stop and surface the exact environment, authentication, or backend issue to the user.

