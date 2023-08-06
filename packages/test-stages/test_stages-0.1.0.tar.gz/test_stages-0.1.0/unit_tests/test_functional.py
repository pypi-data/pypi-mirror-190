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
"""Load the Tox configuration, look for our tags thing."""

# This is a test suite.
# flake8: noqa: T201

from __future__ import annotations

import contextlib
import pathlib
import sys
import tempfile

from collections.abc import Callable, Iterator
from contextlib import AbstractContextManager
from typing import Final

import pytest
import utf8_locale

import tox_trivtags.parse as ttt_parse

if sys.version_info >= (3, 11):
    import contextlib as contextlib_chdir  # pylint: disable=reimported
else:
    import contextlib_chdir

_EXPECTED: Final[dict[str, list[str]]] = {
    "black": ["check"],
    "black-reformat": ["format"],
    "unit-tests-no-tox": ["tests"],
    "unit-tests-tox-3": ["tests"],
    "unit-tests-tox-4": ["tests"],
    ".package": [],
    "t-single": ["something"],
    "t-several": ["all", "the", "things"],
    "t-special": ["So,", "how many", "$tags", 'is "too many",', "'eh\"?"],
}


@contextlib.contextmanager
def _cfg_filename_cwd() -> Iterator[pathlib.Path]:
    """No arguments, parse the tox.ini file in the current directory."""
    yield pathlib.Path("tox.ini")


@contextlib.contextmanager
def _cfg_filename_tempdir() -> Iterator[pathlib.Path]:
    """Create a temporary directory, enter it, pass `-c` with the original cwd."""
    cwd: Final = pathlib.Path("").absolute()
    with tempfile.TemporaryDirectory() as tempd:
        print(f"Temporary directory: {tempd}; current directory: {cwd}")
        with contextlib_chdir.chdir(tempd):
            yield cwd / "tox.ini"


def _do_test_run_showconfig(filename: pathlib.Path) -> None:
    """Parse the `tox --showconfig` output."""
    u8env: Final = utf8_locale.UTF8Detect().detect().env
    print(f"Using {u8env['LC_ALL']} as a UTF-8-capable locale")

    envs: Final = ttt_parse.parse_showconfig(filename, env=u8env)
    print(f"Got some Tox config sections: {' '.join(sorted(envs))}")
    for envname, expected in _EXPECTED.items():
        print(f"- envname {envname!r} expected {expected!r}")
        assert envs[envname].tags == expected


@pytest.mark.parametrize("cfg_filename", [_cfg_filename_cwd, _cfg_filename_tempdir])
def test_run_showconfig(cfg_filename: Callable[[], AbstractContextManager[pathlib.Path]]) -> None:
    """Run `tox --showconfig` expecting tox.ini to be in the specified directory."""
    print()
    with cfg_filename() as filename:
        _do_test_run_showconfig(filename)


def _do_test_call_tox_config(filename: pathlib.Path) -> None:
    """Invoke tox.config.Config() to parse the Tox configuration."""
    envs: Final = ttt_parse.parse_config(filename)
    print(f"Got some Tox environments: {' '.join(sorted(envs))}")
    for envname, expected in _EXPECTED.items():
        print(f"- envname {envname!r} expected {expected!r}")
        assert envs[envname].tags == expected


@pytest.mark.parametrize("cfg_filename", [_cfg_filename_cwd, _cfg_filename_tempdir])
def test_call_tox_config(cfg_filename: Callable[[], AbstractContextManager[pathlib.Path]]) -> None:
    """Parse the tox.ini file in the specified directory."""
    print()
    with cfg_filename() as filename:
        _do_test_call_tox_config(filename)
