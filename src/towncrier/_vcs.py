# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from subprocess import call, DEVNULL

import os
import click


GIT = "git"
HG = "mercurial"


REPO_TYPE = HG if not call(["hg", "status"], stdout=DEVNULL, stderr=DEVNULL) else GIT



def git_add(*files):
    return list(("git", "add") + files)


def git_remove(*files):
    return list(("git", "rm", "--quiet") + files)


def git_outgoing(target):
    return ["git", "diff", "--name-only", "{target}...".format(target=target)]


def hg_add(*files):
    return list(("hg", "add", "--quiet") + files)


def hg_remove(*files):
    return list(("hg", "remove") + files)


def hg_outgoing(target):
    return ["hg", "status", "--no-status", "--rev", "last(ancestors(.) and {target}):.".format(target=target)]
    

ADD = {GIT: git_add, HG: hg_add}
REMOVE = {GIT: git_remove, HG: hg_remove}
OUTGOING_TARGET = {GIT: "origin/master", HG: "remote(default, default)"}
OUTGOING = {GIT: git_outgoing, HG: hg_outgoing}


def remove_files(fragment_filenames, answer_yes):
    if not fragment_filenames:
        return

    if answer_yes:
        click.echo("Removing the following files:")
    else:
        click.echo("I want to remove the following files:")

    for filename in fragment_filenames:
        click.echo(filename)

    if answer_yes or click.confirm("Is it okay if I remove those files?", default=True):
        call(REMOVE[REPO_TYPE](*fragment_filenames))


def stage_newsfile(directory, filename):

    call(ADD[REPO_TYPE](os.path.join(directory, filename)), stderr=DEVNULL)
