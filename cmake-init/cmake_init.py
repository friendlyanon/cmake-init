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
import platform
import re
import subprocess
import sys
import zipfile

__version__ = "0.40.4"

is_windows = os.name == "nt"

compile_template = None


class Language:
    def __init__(self, name, types, options, default):
        self.name = name
        self.types = types
        self.options = options
        self.default = options[default]

    def __str__(self):
        return self.name


c_lang = Language("C", ["e", "s", "h"], ["90", "99", "11", "17", "23"], 1)

cpp_lang = Language("C++", ["e", "h", "s"], ["11", "14", "17", "20"], 2)


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
                print()
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

    type_map = {
        "e": "[E]xecutable",
        "h": "[h]eader-only",
        "s": "[s]tatic/shared",
    }
    lang = c_lang if cli_args.c else cpp_lang
    os_map = {
        "Windows": "win64",
        "Linux": "linux",
        "Darwin": "darwin",
    }

    if not no_prompt:
        print(f"cmake-init is going to generate a {lang} project\n")

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
        "std": ask(
            "{} standard ({})".format(lang, "/".join(lang.options)),
            cli_args.std or lang.default,
            predicate=lambda v: v in lang.options,
            header=f"{lang} standard to use. Defaults to {lang.default}.",
        ),
        "type_id": ask(
            "Target type ({})".format(
                " or ".join([type_map[t] for t in lang.types])
            ),
            cli_args.type_id or "e",
            mapper=lambda v: v[0:1].lower(),
            predicate=lambda v: v in lang.types,
            header="""\
Type of the target this project provides. A static/shared library will be set
up to hide every symbol by default (as it should) and use an export header to
explicitly mark symbols for export/import, but only when built as a shared
library."""
        ),
        "use_clang_tidy": ask(
            "Add clang-tidy to local dev preset ([Y]es/[n]o)",
            cli_args.use_clang_tidy or "y",
            mapper=lambda v: v[0:1].lower(),
            predicate=lambda v: v in ["y", "n"],
            header="This will require you to download clang-tidy locally.",
        ) == "y",
        "use_cppcheck": ask(
            "Add cppcheck to local dev preset ([Y]es/[n]o)",
            cli_args.use_cppcheck or "y",
            mapper=lambda v: v[0:1].lower(),
            predicate=lambda v: v in ["y", "n"],
            header="This will require you to download cppcheck locally.",
        ) == "y",
        "examples": False,
        "c_examples": False,
        "cpp_examples": False,
        "os": os_map.get(platform.system(), "unknown"),
        "c": cli_args.c,
        "cpp": not cli_args.c,
        "c_header": False,
        "include_source": False,
        "has_source": True,
        "cpus": os.cpu_count(),
        "pm_name": "",
        "catch3": False,
        "cpp_std": "",
        "msvc_cpp_std": "",
        "c90": False,
        "c99": False,
        "cmake_321": False,
        "modules": False,
    }
    package_manager = ask(
        "Package manager to use ([N]one/[c]onan/[v]cpkg)",
        cli_args.package_manager or "n",
        mapper=lambda v: v[0:1].lower(),
        predicate=lambda v: v in ["n", "c", "v"],
        header="""\
Choosing Conan requires it to be installed. Choosing vcpkg requires the
VCPKG_ROOT environment variable to be setup to vcpkg's root directory.""",
    )
    d["vcpkg"] = package_manager == "v"
    d["conan"] = package_manager == "c"
    d["pm"] = package_manager != "n"
    if d["pm"]:
        d["pm_name"] = "conan" if d["conan"] else "vcpkg"
    d["uc_name"] = d["name"].upper().replace("-", "_")
    if d["type_id"] != "e":
        key = "c_examples" if cli_args.c else "cpp_examples"
        value = "n" == ask(
            "Exclude examples ([Y]es/[n]o)",
            cli_args.examples or "y",
            mapper=lambda v: v[0:1].lower(),
            predicate=lambda v: v in ["y", "n"],
        )
        d[key] = value
        d["examples"] = value
    if d["type_id"] == "e":
        d["include_source"] = True
    if d["type_id"] == "h":
        d["has_source"] = False
    d["c_header"] = d["c"] and d["type_id"] == "h"
    d["exe"] = d["type_id"] == "e"
    d["lib"] = d["type_id"] == "s"
    d["header"] = d["type_id"] == "h"
    d["catch3"] = d["cpp"] and d["std"] != "11" and d["pm"]
    if d["conan"]:
        if d["c"]:
            d["cpp_std"] = "11"
            d["msvc_cpp_std"] = "14"
        else:
            d["cpp_std"] = d["std"]
            d["msvc_cpp_std"] = d["std"] if d["std"] != "11" else "14"
    if d["c"]:
        if d["std"] == "90":
            d["c90"] = True
        else:
            d["c99"] = True
    else:
        if d["std"] == "20":
            d["modules"] = True
    if d["c"] and int(d["std"]) >= 17:
        d["cmake_321"] = True
    return d


def mkdir(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, d, overwrite, zip_path):
    if overwrite or not os.path.exists(path):
        renderer = compile_template(zip_path.read_text(encoding="UTF-8"), d)
        # noinspection PyBroadException
        try:
            contents = renderer()
        except Exception:
            print(f"Error while rendering {path}", file=sys.stderr)
            raise
        with open(path, "w", encoding="UTF-8", newline="\n") as f:
            f.write(contents)


def should_install_file(name, d):
    if name == "project-is-top-level.cmake":
        return not d["cmake_321"]
    if name == "vcpkg.json":
        return d["vcpkg"]
    if name == "conanfile.py":
        return d["conan"]
    if name == "install-config.cmake":
        return not d["exe"]
    if name == "windows-set-path.cmake":
        return not d["pm"]
    if name == "header_impl.c":
        return d["c_header"] and d["pm"]
    if name == "env.ps1" or name == "env.bat":
        return d["lib"] and not d["pm"]
    return True


def should_install_dir(at, d):
    if at.endswith("/example/"):
        if d["c"]:
            return d["c_examples"] if "/c/" in at else False
        else:
            return d["cpp_examples"]
    if at.endswith("/scripts/"):
        return d["conan"]
    return True


def transform_path(path, d):
    if d["c"] and d["pm"] and path.endswith("_test.c"):
        return f"{path}pp"
    return path


def write_dir(path, d, overwrite, zip_path):
    for entry in zip_path.iterdir():
        name = entry.name.replace("__name__", d["name"])
        next_path = os.path.join(path, name)
        if entry.is_file():
            if should_install_file(name, d):
                write_file(transform_path(next_path, d), d, overwrite, entry)
        elif should_install_dir(entry.at, d):
            mkdir(next_path)
            write_dir(next_path, d, overwrite, entry)


def determine_git_version():
    search_pattern = r"\d+(\.\d+)+"
    git_version_out = \
        subprocess.run("git --version", shell=True, capture_output=True)
    if git_version_out.returncode != 0:
        return None
    git_version_out = str(git_version_out.stdout, sys.stdout.encoding)
    git_version_match = re.search(search_pattern, git_version_out)
    if not git_version_match:
        return None
    git_version_str = git_version_match.group(0)
    git_version = list(map(int, git_version_str.rstrip().split(".")))
    if len(git_version) < 3:
        git_version += [0] * (3 - len(git_version))
    return tuple(git_version)


def git_init(cwd):
    git_version = determine_git_version()
    if git_version is None:
        print("\nGit can't be found! Can't initialize git for the project.\n")
        return
    branch = ""
    if (2, 28, 0) <= git_version:
        branch = " -b master"
    subprocess.run(f"git init{branch}", shell=True, check=True, cwd=cwd)
    print("""
The project is ready to be used with git. If you are using GitHub, you may
push the project with the following commands from the project directory:

    git add .
    git commit -m "Initial commit"
    git remote add origin https://github.com/<your-account>/<repository>.git
    git push -u origin master
""")


def create(args, zip):
    """Create a CMake project according to the provided information
    """
    path = args.path
    if not args.overwrite \
            and os.path.exists(path) \
            and os.path.isdir(path) \
            and len(os.listdir(path)) != 0:
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
    mapping = {"e": "executable/", "h": "header/", "s": "shared/"}
    zip_paths = [("c/" if d["c"] else "") + mapping[d["type_id"]], "common/"]
    if d["c"]:
        zip_paths.insert(1, "c/common/")
    if args.overwrite:
        zip_paths.reverse()
    for zip_path in (f"templates/{p}" for p in zip_paths):
        write_dir(path, d, args.overwrite, zipfile.Path(zip, zip_path))
    git_init(path)
    cmake_version = "3.21" if d["cmake_321"] else "3.20"
    print(f"""\
To get started with developing the project, make sure you read the generated
HACKING.md and BUILDING.md files for how to build the project as a developer or
as a user respectively. There are also some details you may want to fill in in
the README.md, CONTRIBUTING.md and .github/workflows/ci.yml files.

Now make sure you have at least CMake {cmake_version} installed for local development, to
make use of all the nice Quality-of-Life improvements in newer releases:
https://cmake.org/download/

For more tips, like integration with package managers, please see the Wiki:
https://github.com/friendlyanon/cmake-init/wiki

You are all set. Have fun programming and create something awesome!""")


def main(zip, template_compiler):
    global compile_template
    compile_template = template_compiler

    p = argparse.ArgumentParser(
        prog="cmake-init",
        description=__doc__,
        add_help=False,
    )
    p.add_argument(
        "--help",
        action="help",
        help="show this help message and exit",
    )
    p.add_argument("--version", action="version", version=__version__)
    p.set_defaults(overwrite=False, dummy=False, c=False)
    p.add_argument(
        "--c",
        action="store_true",
        help="generate a C project instead of a C++ one",
    )
    p.add_argument(
        "path",
        type=os.path.realpath,
        help="path to generate to, the name is also derived from this",
    )
    create_flags = \
        ["type_id", "std", "use_clang_tidy", "use_cppcheck", "examples"]
    p.set_defaults(**{k: "" for k in create_flags})
    type_g = p.add_mutually_exclusive_group()
    mapping = {
        "e": "generate an executable (default)",
        "h": "generate a header-only library",
        "s": "generate a static/shared library",
    }
    for flag, help in mapping.items():
        type_g.add_argument(
            f"-{flag}",
            dest="type_id",
            action="store_const",
            const=flag,
            help=help,
        )
    defaults = ", ".join(
        [f"{lang} - {lang.default}" for lang in [cpp_lang, c_lang]]
    )
    p.add_argument(
        "--std",
        metavar="NN",
        help=f"set the language standard to use (defaults: {defaults})",
    )
    p.add_argument(
        "--no-clang-tidy",
        action="store_const",
        dest="use_clang_tidy",
        const="n",
        help="omit the clang-tidy preset from the dev preset",
    )
    p.add_argument(
        "--no-cppcheck",
        action="store_const",
        dest="use_cppcheck",
        const="n",
        help="omit the cppcheck preset from the dev preset",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="omit checks for existing files and non-empty project root",
    )
    p.add_argument(
        "--examples",
        action="store_const",
        const="n",
        help="generate examples for a library",
    )
    p.add_argument(
        "-p",
        metavar="pm",
        dest="package_manager",
        help="package manager to use (Options are: conan, vcpkg)",
    )
    args = p.parse_args()
    if args.dummy:
        p.print_help()
        exit(1)
    flags_used = any(getattr(args, k) != "" for k in create_flags)
    setattr(args, "flags_used", flags_used)
    create(args, zip)
