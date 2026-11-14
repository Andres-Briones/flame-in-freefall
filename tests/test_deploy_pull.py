import os
import shutil
import subprocess
from pathlib import Path

import pytest

PULL = Path(__file__).resolve().parents[1] / "deploy" / "pull.sh"

pytestmark = pytest.mark.skipif(not (shutil.which("git") and shutil.which("flock")), reason="git or flock missing")


def git(cwd, *args, env=None):
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout


def pull(env):
    return subprocess.run([str(PULL)], env=env, capture_output=True, text=True)


def commit(work, name, env):
    (work / name).write_text(name)
    git(work, "add", name, env=env)
    git(work, "commit", "-qm", name, env=env)
    git(work, "push", "-q", "origin", "main", env=env)


@pytest.fixture
def setup(tmp_path):
    env = {**os.environ, "HOME": str(tmp_path), "GIT_CONFIG_GLOBAL": str(tmp_path / "gitconfig"),
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    github, work, server = tmp_path / "github.git", tmp_path / "work", tmp_path / "server"
    git(tmp_path, "init", "-q", "--bare", "-b", "main", str(github), env=env)
    git(tmp_path, "clone", "-q", str(github), str(work), env=env)
    run_sh = work / "run.sh"
    # Stands in for the real run.sh: logs each start and fails while a file named "broken" exists beside the repo.
    run_sh.write_text('#!/usr/bin/env bash\necho "$1 domain=${FIF_DOMAIN:-none}" >> ../starts.log\n[ ! -e ../broken ]\n')
    run_sh.chmod(0o755)
    git(work, "add", "run.sh", env=env)
    git(work, "commit", "-qm", "init", env=env)
    git(work, "push", "-q", "origin", "main", env=env)
    git(tmp_path, "clone", "-q", str(github), str(server), env=env)
    env.update(FIF_REPO=str(server), FIF_PULL_URL=str(github))
    return tmp_path, work, server, env


def starts(tmp):
    log = tmp / "starts.log"
    return log.read_text().splitlines() if log.exists() else []


def test_a_new_commit_is_merged_and_started_once(setup):
    tmp, work, server, env = setup
    assert pull(env).returncode == 0
    assert len(starts(tmp)) == 1  # the first run cannot know the commit is already running

    commit(work, "new.txt", env)
    r = pull(env)
    assert r.returncode == 0 and "deploying" in r.stdout
    assert (server / "new.txt").exists()
    assert len(starts(tmp)) == 2

    r = pull(env)
    assert r.returncode == 0 and r.stdout == ""
    assert len(starts(tmp)) == 2


def test_a_failed_start_is_tried_again(setup):
    tmp, work, _, env = setup
    pull(env)
    commit(work, "new.txt", env)
    (tmp / "broken").touch()
    assert pull(env).returncode != 0
    (tmp / "broken").unlink()
    assert pull(env).returncode == 0
    assert len(starts(tmp)) == 3


def test_settings_come_from_the_env_file(setup):
    tmp, _, _, env = setup
    (tmp / ".config").mkdir()
    (tmp / ".config" / "fif-deploy.env").write_text("FIF_DOMAIN=example.org\n")
    pull(env)
    assert starts(tmp) == ["start domain=example.org"]


def test_a_server_commit_that_is_not_on_github_stops_the_deploy(setup):
    tmp, work, server, env = setup
    pull(env)
    (server / "local.txt").write_text("local")
    git(server, "add", "local.txt", env=env)
    git(server, "commit", "-qm", "local", env=env)
    commit(work, "new.txt", env)
    assert pull(env).returncode != 0
    assert not (server / "new.txt").exists()
    assert len(starts(tmp)) == 1
