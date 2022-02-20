# cmake-init - The missing CMake project initializer
# Copyright (C) 2021  friendlyanon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Website: https://github.com/friendlyanon/cmake-init

import re

__all__ = ["compile_template"]

block_regex = re.compile(
    r"(.*?)({% .+? %}|{= .+? =})|(.+?)\Z",
    re.MULTILINE | re.DOTALL
)


def compile_template(template_source, globals):
    depth = 0
    python_source = ["def f():\n _result = []"]

    def add_line(line):
        python_source.append(" " * (depth + 1) + line)

    def add_repr(o):
        add_line("_result.append(str(" + repr(o) + "))")

    for match in block_regex.finditer(template_source):
        before, block, tail = match.groups()
        if not block:
            add_repr(tail)
            continue
        if block == "end":
            depth -= 1
            continue
        if before:
            add_repr(before)
        inner = block[3:-3]
        if block[1:2] == "=":
            add_repr(globals[inner])
            continue
        if inner == "end":
            depth -= 1
            continue
        if inner == "else" or inner.startswith("elif "):
            depth -= 1
        add_line(inner + ":")
        depth += 1

    if depth != 0:
        raise SyntaxError("Block not properly terminated")

    add_line("return \"\".join(_result)")
    locals = {}
    exec("\n".join(python_source), globals, locals)
    return locals["f"]
