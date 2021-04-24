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

"""\
Opinionated CMake project initializer to generate CMake projects that are
FetchContent ready, separate consumer and developer targets, provide install
rules with proper relocatable CMake packages and use modern CMake (3.14+)
"""

import argparse
import contextlib
import io
import os
import re
import subprocess
import sys
import zipfile

__version__ = "0.5.0"

zip = zipfile.ZipFile(os.path.dirname(__file__), "r")


def not_empty(value):
    return len(value) != 0


def prompt(msg, default, mapper=None, predicate=not_empty, header=None, no_prompt=False):
    if header is not None:
        print(header)
    while True:
        # noinspection PyBroadException
        try:
            print(msg.format(default), end=": ")
            value = ("" if no_prompt else input()) or default
            if mapper is not None:
                value = mapper(value)
            if predicate(value):
                return value
        except Exception:
            pass
        if no_prompt:
            raise ValueError()
        print("Invalid value, try again")


def is_valid_name(name):
    special = ["test", "lib"]  # special case for this script only
    return name not in special \
        and re.match("^[a-zA-Z][0-9a-zA-Z-_]+$", name) is not None \
        and re.match("[-_]{2,}", name) is None


def is_semver(version):
    return re.match(r"^\d+(\.\d+){0,3}", version) is not None


def get_substitutes(cli_args, name):
    no_prompt = cli_args.flags_used
    if no_prompt and not is_valid_name(name):
        print(f"'{name}' is not a valid name", file=sys.stderr)
        exit(1)

    def ask(*args, **kwargs):
        return prompt(*args, **kwargs, no_prompt=no_prompt)

    d = {
        "name": ask(
            "Project name ({})",
            name,
            predicate=is_valid_name,
            header="Use only characters matching the [0-9a-zA-Z-_] pattern"
        ),
        "version": ask(
            "Project version ({})",
            "0.1.0",
            predicate=is_semver,
            header="""\
Use Semantic Versioning, because CMake naturally supports that. Visit
https://semver.org/ for more information."""
        ),
        "description": ask(*(["Short description"] * 2)),
        "homepage": ask("Homepage URL ({})", "https://example.com/"),
        "type_id": ask(
            "Target type ([E]xecutable or [s]tatic/shared or [h]eader-only)",
            cli_args.type_id or "e",
            mapper=lambda v: v[0:1].lower(),
            predicate=lambda v: v in ["s", "h", "e"],
            header="""\
Type of the target this project provides. A static/shared library will be set
up to hide every symbol by default (as it should) and use an export header to
explicitly mark symbols for export/import, but only when built as a shared
library."""
        ),
        "std": ask(
            "C++ standard (11/14/17/20)",
            cli_args.std or "17",
            predicate=lambda v: v in ["11", "14", "17", "20"],
            header="C++ standard to use. Defaults to 17.",
        ),
        "examples": False,
        "os": "windows" if os.name == "nt" else "unix",
        "win_flags": "warnings",
        "win_extra_flags": "",
    }
    d["uc_name"] = d["name"].upper().replace("-", "_")
    if d["type_id"] != "e":
        d["examples"] = "n" == ask(
            "Exclude examples ([Y]es/[n]o)",
            "y",
            mapper=lambda v: v[0:1].lower(),
            predicate=lambda v: v in ["y", "n"],
        )
    else:
        d["win_flags"] = "flags"
        d["win_extra_flags"] = " /EHsc"
    return d


def mkdir(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, d, zip_path):
    if os.path.exists(path):
        return

    def replacer(match):
        query = match.group(1)
        if query == "type":
            mapping = {"exe": "e", "shared": "s", "header": "h"}
            if mapping[match.group(2)] == d["type_id"]:
                return match.group(3)
        elif query == "if" and d[match.group(2)] is True:
            return match.group(3)
        return ""

    regex = re.compile("{(type|if) ([^}]+)}(.+?){end}", re.DOTALL)
    contents = regex.sub(replacer, zip_path.read_text())
    with open(path, "w", newline="\n") as f:
        f.write(contents % d)


def write_dir(path, d, zip_path):
    for entry in zip_path.iterdir():
        name = entry.name.replace("__name__", d["name"])
        next_path = os.path.join(path, name)
        if entry.is_file():
            write_file(next_path, d, entry)
        elif name != "example" or d["examples"]:
            mkdir(next_path)
            write_dir(next_path, d, entry)


def git_init(cwd):
    subprocess.run("git init -b master", shell=True, check=True, cwd=cwd)
    print("""
The project is ready to be used with git. If you are using GitHub, you may
push the project with the following commands from the project directory:

    git add .
    git commit -m "Initial commit"
    git remote add origin https://github.com/<your-account>/<repository>.git
    git push -u origin master
""")


def print_tips(d):
    config = " --config Release" if os.name == "nt" else ""
    test_cfg = " -C Release" if os.name == "nt" else ""
    print("""\
To get you started with the project in developer mode, you may configure,
build, install and test with the following commands from the project directory,
in that order:

    cmake --preset=dev
    cmake --build build{config} -j {cpus}
    cmake --install build{config} --prefix prefix
    cd build && ctest{test_cfg} -j {cpus} --output-on-failure
""".format(config=config, cpus=os.cpu_count(), test_cfg=test_cfg))
    if not d["examples"] and d["type_id"] != "e":
        return
    print("""\
There are some convenience targets that you can run to invoke some built
executables conveniently:
""")
    if d["examples"]:
        print("""\
    run_examples - runs all the examples created by the add_example command""")
    if d["type_id"] == "e":
        print("""\
    run_exe - runs the executable built by the project""")
    print("""
These targets are only available in developer mode, because they are generally
not useful for consumers. You can run these targets with the following command:

    cmake --build build{config} -t <target>
""".format(config=config))


def create(args):
    """Create a CMake project according to the provided information
    """
    path = args.path
    root_exists = os.path.exists(path)
    if root_exists and os.path.isdir(path) and len(os.listdir(path)) != 0:
        print(
            f"Error - directory exists and is not empty:\n{path}",
            file=sys.stderr,
        )
        exit(1)
    if args.flags_used:
        with contextlib.redirect_stdout(io.StringIO()):
            d = get_substitutes(args, os.path.basename(path))
    else:
        d = get_substitutes(args, os.path.basename(path))
    mkdir(path)
    mapping = {"s": "shared/", "e": "executable/", "h": "header/"}
    write_dir(path, d, zipfile.Path(zip, "templates/" + mapping[d["type_id"]]))
    write_dir(path, d, zipfile.Path(zip, "templates/common/"))
    git_init(path)
    print_tips(d)
    print("""\
Now make sure you have at least CMake 3.19 installed for local development, to
make use of all the nice Quality-of-Life improvements in newer releases:
https://cmake.org/download/

For more tips, like integration with package managers, please see the Wiki:
http://github.com/friendlyanon/cmake-init/wiki

You are all set. Have fun programming and create something awesome!""")


def main():
    p = argparse.ArgumentParser(prog="cmake-init", description=__doc__)
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("path", type=os.path.realpath)
    p.set_defaults(type_id="", std="")
    type_g = p.add_mutually_exclusive_group()
    for type, flags in {"s": ["-s"], "e": ["-e", "-y"], "h": ["-ho"]}.items():
        type_g.add_argument(
            *flags,
            dest="type_id",
            action="store_const",
            const=type,
        )
    p.add_argument(
        "--std",
        choices=["11", "14", "17", "20"],
    )
    args = p.parse_args()
    setattr(args, "flags_used", args.type_id != "" or args.std != "")
    create(args)


try:
    # open a dummy fd to keep the zip from being closed
    with zip.open("__main__.py") as dummy_fp:
        main()
except KeyboardInterrupt:
    pass
