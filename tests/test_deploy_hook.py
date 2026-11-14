import os
import shutil
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "deploy" / "ssh-hook.sh"

pytestmark = pytest.mark.skipif(not shutil.which("git"), reason="git not installed")


def git(cwd, *args, env=None):
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout


def hook(command, env, **kw):
    return subprocess.run([str(HOOK)], env={**env, "SSH_ORIGINAL_COMMAND": command}, capture_output=True,
                          text=True, **kw)


@pytest.fixture
def setup(tmp_path):
    env = {**os.environ, "HOME": str(tmp_path), "GIT_CONFIG_GLOBAL": str(tmp_path / "gitconfig"),
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    server = tmp_path / "server"
    server.mkdir()
    git(server, "init", "-q", "-b", "main", env=env)
    git(server, "config", "receive.denyCurrentBranch", "updateInstead", env=env)
    run_sh = server / "run.sh"
    run_sh.write_text('#!/usr/bin/env bash\necho "run.sh $1 domain=${FIF_DOMAIN:-none}"\n')
    run_sh.chmod(0o755)
    git(server, "add", "run.sh", env=env)
    git(server, "commit", "-qm", "init", env=env)
    env["FIF_REPO"] = str(server)
    return tmp_path, server, env


def test_push_through_the_hook_updates_the_checked_out_tree(setup):
    tmp, server, env = setup
    # Stands in for sshd: the remote command arrives as SSH_ORIGINAL_COMMAND, whatever path the client asked for.
    fake_ssh = tmp / "fake-ssh"
    fake_ssh.write_text(f'#!/usr/bin/env bash\nfor a; do last="$a"; done\nSSH_ORIGINAL_COMMAND="$last" exec {HOOK}\n')
    fake_ssh.chmod(0o755)
    clone = tmp / "clone"
    git(tmp, "clone", "-q", str(server), str(clone), env=env)
    (clone / "new.txt").write_text("hello\n")
    git(clone, "add", "new.txt", env=env)
    git(clone, "commit", "-qm", "new", env=env)

    git(clone, "push", "-q", "deploy@host:some/other/path", "HEAD:refs/heads/main",
        env={**env, "GIT_SSH_COMMAND": str(fake_ssh)})

    assert (server / "new.txt").read_text() == "hello\n"


def test_deploy_starts_the_server_with_the_env_file(setup):
    tmp, _, env = setup
    (tmp / ".config").mkdir()
    (tmp / ".config" / "fif-deploy.env").write_text("FIF_DOMAIN=example.org\n")

    out = hook("deploy", env)

    assert out.returncode == 0
    assert out.stdout.strip() == "run.sh start domain=example.org"


@pytest.mark.parametrize("command", ["", "bash", "deploy; rm -rf ~", "git-upload-pack 'repo'", "ls"])
def test_anything_else_is_refused(setup, command):
    _, _, env = setup

    out = hook(command, env)

    assert out.returncode == 1
    assert "refused" in out.stderr
    assert out.stdout == ""
