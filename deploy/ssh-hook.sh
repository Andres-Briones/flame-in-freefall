#!/usr/bin/env bash
# Forced command for the GitHub deploy key (demo/README.md, "Automatic deploy from GitHub").
# Copy it OUTSIDE the repo (e.g. ~/bin/fif-deploy-hook): a push must not be able to change what the key may run.
# The key may only push into the repo and start the server; anything else, including a shell, is refused.
set -euo pipefail
repo="${FIF_REPO:-$HOME/projects/flame-in-freefall}"
# A forced command gets no login environment, so FIF_DOMAIN, FIF_PORT etc. come from this file.
env_file="${FIF_DEPLOY_ENV:-$HOME/.config/fif-deploy.env}"

case "${SSH_ORIGINAL_COMMAND:-}" in
    "git-receive-pack "*)
        # The path the client asks for is ignored: the key can only ever reach $repo.
        exec git-receive-pack "$repo" ;;
    deploy)
        if [ -f "$env_file" ]; then set -a; . "$env_file"; set +a; fi
        cd "$repo"
        exec ./run.sh start ;;
    *)
        echo "fif-deploy-hook: refused: ${SSH_ORIGINAL_COMMAND:-<interactive shell>}" >&2
        exit 1 ;;
esac
