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
"""Parse a list of tags in the Tox configuration.

Inspired by https://github.com/tox-dev/tox-tags
"""

import packaging.version
import pkg_resources


try:
    HAVE_MOD_TOX_3 = (
        packaging.version.Version("3")
        <= packaging.version.Version(pkg_resources.get_distribution("tox").version)
        < packaging.version.Version("4")
    )
except pkg_resources.DistributionNotFound:
    HAVE_MOD_TOX_3 = False


if HAVE_MOD_TOX_3:
    import tox
    import tox.config

    @tox.hookimpl
    def tox_addoption(parser: tox.config.Parser) -> None:
        """Parse a testenv's "tags" attribute as a list of lines."""
        parser.add_testenv_attribute(
            "tags", "line-list", "A list of tags describing this test environment", default=[]
        )
