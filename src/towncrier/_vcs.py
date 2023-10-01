# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import annotations

import os

from subprocess import DEVNULL, STDOUT, call, check_output


GIT = "git"
HG = "mercurial"


REPO_TYPE = HG if not call(["hg", "status"], stdout=DEVNULL, stderr=DEVNULL) else GIT


def git_remove(fragment_filenames: list[str]) -> None:
    if fragment_filenames:
        call(["git", "rm", "--quiet"] + fragment_filenames)


def git_add(directory: str, filename: str) -> None:
    call(["git", "add", os.path.join(directory, filename)])


def git_remote_branches(base_directory: str) -> list[str]:
    output = check_output(
        ["git", "branch", "-r"], cwd=base_directory, encoding="utf-8", stderr=STDOUT
    )

    return [branch.strip() for branch in output.strip().splitlines()]


def git_list_changed_files_compared_to_branch(
    base_directory: str, compare_with: str
) -> list[str]:
    output = check_output(
        ["git", "diff", "--name-only", compare_with + "..."],
        cwd=base_directory,
        encoding="utf-8",
        stderr=STDOUT,
    )

    return output.strip().splitlines()


def hg_remove(fragment_filenames: list[str]) -> None:
    if fragment_filenames:
        call(["hg", "remove"] + fragment_filenames)


def hg_add(directory: str, filename: str) -> None:
    call(["hg", "add", "--quiet", os.path.join(directory, filename)])


def hg_remote_branches(base_directory: str) -> list[str]:
    branches = [branch.strip() for branch in check_output(
        ["hg", "branches", "-T", "{branch}\n"],
        cwd=base_directory,
        encoding="utf-8",
        stderr=STDOUT,
    ).strip().splitlines()]
    paths = [path.strip() for path in check_output(
        ["hg", "paths", "-T", "{name}\n"],
        cwd=base_directory,
        encoding="utf-8",
        stderr=STDOUT,
    ).strip().splitlines()]

    return [f"remote({branch}, {path})" for path in paths for branch in branches]


def hg_list_changed_files_compared_to_branch(
    base_directory: str, compare_with: str
) -> list[str]:
    output = check_output(
        [
            "hg",
            "status",
            "--no-status",
            "--rev",
            f"last(ancestors(.) and {compare_with}):.",
        ],
        cwd=base_directory,
        encoding="utf-8",
        stderr=STDOUT
    )

    return output.strip().splitlines()


remove_files = git_remove if REPO_TYPE == GIT else hg_remove
stage_newsfile = git_add if REPO_TYPE == GIT else hg_add
get_remote_branches = git_remote_branches if REPO_TYPE == GIT else hg_remote_branches
list_changed_files_compared_to_branch = (
    git_list_changed_files_compared_to_branch
    if REPO_TYPE == GIT
    else hg_list_changed_files_compared_to_branch
)
