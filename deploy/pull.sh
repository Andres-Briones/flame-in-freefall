#!/usr/bin/env bash
# Deploys main when GitHub has a commit this server has not started yet (demo/README.md, "Automatic deploy").
# Run every minute by deploy/fif-pull.timer; also fine by hand. Quiet when there is nothing to do.
set -euo pipefail

main() {
    # A systemd unit gets no login environment, so FIF_DOMAIN, FIF_PORT etc. come from this file.
    local env_file="${FIF_DEPLOY_ENV:-$HOME/.config/fif-deploy.env}"
    if [ -f "$env_file" ]; then set -a; . "$env_file"; set +a; fi
    local repo="${FIF_REPO:-$HOME/projects/flame-in-freefall}"
    local url="${FIF_PULL_URL:-git@github.com:Andres-Briones/flame-in-freefall.git}"
    local key="${FIF_PULL_KEY:-$HOME/.ssh/fif-pull}"
    cd "$repo"
    [ ! -f "$key" ] || export GIT_SSH_COMMAND="ssh -i $key -o IdentitiesOnly=yes -o BatchMode=yes"

    # A build can outlast the timer's interval: the next tick must not start a second one.
    exec 9>.git/fif-pull.lock
    flock -n 9 || exit 0

    git fetch -q "$url" main
    local want; want="$(git rev-parse FETCH_HEAD)"
    # The marker is written only after a start that came up healthy, so a failed deploy is tried again.
    [ "$(cat .git/fif-deployed 2>/dev/null)" != "$want" ] || exit 0

    echo "fif-pull: deploying $want"
    git merge -q --ff-only "$want"
    ./run.sh start
    echo "$want" > .git/fif-deployed
}

# Bash reads a script as it runs it and the merge may rewrite this file: parse everything before running.
main "$@"; exit
