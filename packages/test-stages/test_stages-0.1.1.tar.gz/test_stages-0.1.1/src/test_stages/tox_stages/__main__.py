# Copyright (c) Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
"""The main tox-stages command-line executable."""

# This is a command-line tool, output is part of its job.
# flake8: noqa: T201

from __future__ import annotations

import dataclasses
import pathlib
import subprocess
import sys

from typing import Final

import tox_trivtags

from .. import cmd

if tox_trivtags.HAVE_MOD_TOX_3:
    from tox_trivtags import parse as ttt_parse


@dataclasses.dataclass(frozen=True)
class Config(cmd.Config):
    """Also store the path to the Tox executable if found."""

    tox_program: list[str | pathlib.Path] | None = None


@cmd.click_available()
def _cmd_available(cfg: cmd.Config) -> bool:
    """Check whether we can parse the Tox configuration in any of the supported ways.

    Currently the only supported way is `tox --showconfig`.
    """
    assert isinstance(cfg, Config)
    return cfg.tox_program is not None


@cmd.click_run()
def _cmd_run(cfg: cmd.Config, stages: list[list[cmd.TestEnv]]) -> None:
    """Run the Tox environments in groups."""
    toxdir = cfg.filename.parent

    def run_group(group: list[cmd.TestEnv]) -> None:
        """Run the stages in a single group."""
        if not isinstance(cfg, Config) or cfg.tox_program is None:
            #  _tox_get_envs() really should have taken care of that
            sys.exit(f"Internal error: tox-stages run_group: Config? {cfg!r}")

        names: Final = ",".join(env.name for env in group)
        print(f"\n=== Running Tox environments: {names}\n")
        res: Final = subprocess.run(
            cfg.tox_program + ["-p", "all", "-e", names],
            check=False,
            cwd=toxdir,
            env=cfg.utf8_env,
            shell=False,
        )
        if res.returncode != 0:
            sys.exit(f"Tox failed for the {names} environments")

    for group in stages:
        run_group(group)

    print("\n=== All Tox environment groups passed!")


def _tox_get_envs(cfg: cmd.Config) -> list[cmd.TestEnv]:
    """Get all the Tox environments from the config file."""
    assert isinstance(cfg, Config)
    if cfg.tox_program is None:
        sys.exit("No tox program found or specified")
    tcfg: Final = ttt_parse.parse_showconfig(
        filename=cfg.filename, env=cfg.utf8_env, tox_invoke=cfg.tox_program
    )
    return [cmd.TestEnv(name, env.tags) for name, env in tcfg.items()]


def _find_tox_program() -> list[str | pathlib.Path] | None:
    """Figure out how to invoke Tox.

    For the present, only a Tox installation in the current Python interpreter's
    package directories is supported, since we need to be sure that we can rely on
    the `tox-trivtags` package being installed.

    Also, we only support Tox 3.x for the present.
    """
    if not tox_trivtags.HAVE_MOD_TOX_3:
        return None

    return [sys.executable, "-m", "tox"]


@cmd.click_main(
    prog="tox-stages",
    prog_help="Run Tox environments in groups, stop on failure.",
    filename="tox.ini",
    filename_help="the path to the Tox config file to parse",
    get_all_envs=_tox_get_envs,
)
def main(cfg: cmd.Config) -> cmd.Config:
    """Return our `Config` object with the path to Tox if found."""
    return Config(**dataclasses.asdict(cfg), tox_program=_find_tox_program())


main.add_command(_cmd_available)
main.add_command(_cmd_run)
