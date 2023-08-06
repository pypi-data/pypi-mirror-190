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
"""Command-line tool helpers for the various test-stages implementations."""

from __future__ import annotations

import dataclasses
import functools
import pathlib
import sys

from collections.abc import Callable
from typing import Any, Final, NamedTuple, TypeVar

import click
import parse_stages as parse
import utf8_locale

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


TestEnv = parse.TaggedFrozen


class Stage(NamedTuple):
    """A stage specification and its boolean expression."""

    spec: str
    expr: parse.BoolExpr


@dataclasses.dataclass(frozen=True)
class Config:
    """Runtime configuration for the test runner tool."""

    filename: pathlib.Path
    get_all_envs: Callable[[Config], list[TestEnv]]
    stages: list[Stage] = dataclasses.field(default_factory=list)
    utf8_env: dict[str, str] = dataclasses.field(
        default_factory=lambda: utf8_locale.UTF8Detect().detect().env
    )


@dataclasses.dataclass
class ConfigHolder:
    """Hold a Config object."""

    cfg: Config | None = None


# pylint: disable-next=invalid-name
_T = TypeVar("_T")


def _split_by(current: list[_T], func: Callable[[_T], bool]) -> tuple[list[_T], list[_T]]:
    """Split an ordered list of items in two by the given predicate."""
    res: Final[tuple[list[_T], list[_T]]] = ([], [])
    for stage in current:
        if func(stage):
            res[1].append(stage)
        else:
            res[0].append(stage)
    return res


def select_stages(cfg: Config, all_stages: list[TestEnv]) -> list[list[TestEnv]]:
    """Group the stages as specified."""

    def process_stage(
        acc: tuple[list[list[TestEnv]], list[TestEnv]], stage: Stage
    ) -> tuple[list[list[TestEnv]], list[TestEnv]]:
        """Stash the environments matched by a stage specification."""
        res, current = acc
        if not current:
            sys.exit(f"No test environments left for {stage.spec}")
        left, matched = _split_by(current, stage.expr.evaluate)
        if not matched:
            sys.exit(f"No test environments matched by {stage.spec}")
        res.append(matched)
        return res, left

    res_init: Final[list[list[TestEnv]]] = []
    return functools.reduce(process_stage, cfg.stages, (res_init, list(all_stages)))[0]


def extract_cfg(ctx: click.Context) -> Config:
    """Extract the Config object from the ConfigHolder."""
    cfg_hold: Final = ctx.find_object(ConfigHolder)
    # mypy needs these assertions
    assert cfg_hold is not None  # noqa: S101
    cfg: Final = cfg_hold.cfg
    assert cfg is not None  # noqa: S101
    return cfg


def _find_and_load_pyproject(startdir: pathlib.Path) -> dict[str, Any]:
    """Look for a pyproject.toml file, load it if found."""

    def _find_and_load(path: pathlib.Path) -> dict[str, Any] | None:
        """Check for a pyproject.toml file in the specified directory."""
        proj_file: Final = path / "pyproject.toml"
        if not proj_file.is_file():
            return None

        return tomllib.loads(proj_file.read_text(encoding="UTF-8"))

    # Maybe we should look in the parent directories, too... later.
    for path in (startdir,):
        found = _find_and_load(path)
        if found is not None:
            return found

    # No pyproject.toml file found, nothing to parse
    return {}


def click_available() -> Callable[[Callable[[Config], bool]], click.Command]:
    """Wrap an available() function, checking whether the test runner can be invoked."""

    def inner(handler: Callable[[Config], bool]) -> click.Command:
        """Wrap the available check function."""

        @click.command(name="available")
        @click.pass_context
        def real_available(ctx: click.Context) -> None:
            """Check whether the test runner is available."""
            sys.exit(0 if handler(extract_cfg(ctx)) else 1)

        return real_available

    return inner


def click_run() -> Callable[[Callable[[Config, list[list[TestEnv]]], None]], click.Command]:
    """Wrap a run() function, preparing the configuration."""

    def inner(handler: Callable[[Config, list[list[TestEnv]]], None]) -> click.Command:
        """Wrap the run function."""

        @click.command(name="run")
        @click.argument("stages_spec", nargs=-1, required=False, type=str)
        @click.pass_context
        def real_run(ctx: click.Context, stages_spec: list[str]) -> None:
            """Run the test environments in stages."""
            cfg_base: Final = extract_cfg(ctx)
            if not stages_spec:
                pyproj: Final = _find_and_load_pyproject(cfg_base.filename.parent)
                stages_spec = pyproj.get("tool", {}).get("test-stages", {}).get("stages", [])
                if not stages_spec:
                    sys.exit("No stages specified either on the command line or in pyproject.toml")

            cfg: Final = dataclasses.replace(
                cfg_base,
                stages=[Stage(spec, parse.parse_spec(spec)) for spec in stages_spec],
            )
            ctx.obj.cfg = cfg

            handler(cfg, select_stages(cfg, cfg.get_all_envs(cfg)))

        return real_run

    return inner


def click_main(
    prog: str,
    prog_help: str,
    filename: str,
    filename_help: str,
    get_all_envs: Callable[[Config], list[TestEnv]],
) -> Callable[[Callable[[Config], Config]], click.Group]:
    """Wrap a main() function, parsing the top-level options."""

    def inner(main: Callable[[Config], Config]) -> click.Group:
        """Wrap the main function."""

        @click.group(name=prog, help=prog_help)
        @click.option(
            "-f",
            "--filename",
            type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=pathlib.Path),
            default=filename,
            help=filename_help,
        )
        @click.pass_context
        def real_main(ctx: click.Context, filename: pathlib.Path) -> None:
            """Run Tox environments in groups, stop on failure."""
            ctx.ensure_object(ConfigHolder)
            ctx.obj.cfg = main(Config(filename=filename, get_all_envs=get_all_envs))

        return real_main

    return inner
