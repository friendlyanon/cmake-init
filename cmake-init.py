#!/usr/bin/env python3

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

__version__ = "0.3.1"

root_cml_top = """cmake_minimum_required(VERSION 3.14)

include(cmake/in-source-guard.cmake)

project(
    {name}
    VERSION {version}
    DESCRIPTION "{description}"
    HOMEPAGE_URL "{homepage}"
    LANGUAGES CXX
)

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Declare library ----
"""

root_cml_bottom = """
# ---- Install rules ----

include(cmake/install-rules.cmake)

# ---- Developer mode ----

if(NOT {name}_DEVELOPER_MODE)
  return()
elseif(NOT PROJECT_IS_TOP_LEVEL)
  message(
      AUTHOR_WARNING
      "Developer mode is intended for developers of {name}"
  )
endif()

include(CTest)
if(BUILD_TESTING)
  add_subdirectory(test)
endif()
"""

in_source_guard = r"""if(CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR)
  message(FATAL_ERROR "\
In-source builds are not supported. \n\
Make a new directory (e.g., 'build/'), and run CMake from there. \
You may need to delete 'CMakeCache.txt' and 'CMakeFiles/' first.")
endif()
"""

project_is_top_level = """\
# This variable is set by project() in CMake 3.21+
string(
    COMPARE EQUAL
    "${{CMAKE_SOURCE_DIR}}" "${{PROJECT_SOURCE_DIR}}"
    PROJECT_IS_TOP_LEVEL
)
"""

variables = """# ---- Developer mode ----

# Developer mode enables targets and code paths in the CMake scripts that are
# only relevant for the developer(s) of {name}
# Targets necessary to build the project must be provided unconditionally, so
# consumers can trivially build and package the project
if(PROJECT_IS_TOP_LEVEL)
  option({name}_DEVELOPER_MODE "Enable developer mode" OFF)
{shared_libs}
  if("$ENV{{CI}}")
    set({name}_DEVELOPER_MODE ON CACHE INTERNAL "")
  endif()
endif()

# ---- Warning guard ----

# target_include_directories with the SYSTEM modifier will request the compiler
# to omit warnings from the provided paths, if the compiler supports that
# This is to provide a user experience similar to find_package when
# add_subdirectory or FetchContent is used to consume this project
set({name}_warning_guard "")
if(NOT PROJECT_IS_TOP_LEVEL)
  option(
      {name}_INCLUDES_WITH_SYSTEM
      "Use SYSTEM modifier for {name}'s includes, disabling warnings"
      ON
  )
  mark_as_advanced({name}_INCLUDES_WITH_SYSTEM)
  if({name}_INCLUDES_WITH_SYSTEM)
    set({name}_warning_guard SYSTEM)
  endif()
endif()
"""

shared_library = """
add_library(
    {name}_{name}
    include/{name}/{name}.h
    source/{name}.cpp
)
add_library({name}::{name} ALIAS {name}_{name})

include(GenerateExportHeader)
generate_export_header(
    {name}_{name}
    BASE_NAME {name}
    EXPORT_FILE_NAME include/{name}/{name}_export.h
)

if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions({name}_{name} PUBLIC {uc_name}_STATIC_DEFINE)
endif()

set_target_properties(
    {name}_{name} PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES
    VERSION "${{PROJECT_VERSION}}"
    SOVERSION "${{PROJECT_VERSION_MAJOR}}"
    EXPORT_NAME {name}
    OUTPUT_NAME {name}
)

target_include_directories(
    {name}_{name}
    ${{{name}_warning_guard}}
    PUBLIC
    "$<BUILD_INTERFACE:${{PROJECT_SOURCE_DIR}}/include>"
    "$<BUILD_INTERFACE:${{PROJECT_BINARY_DIR}}/include>"
)

target_compile_features({name}_{name} PUBLIC cxx_std_{std})
"""

header_only_library = """
add_library({name}_{name} INTERFACE)
add_library({name}::{name} ALIAS {name}_{name})

set_property(
    TARGET {name}_{name} PROPERTY
    EXPORT_NAME {name}
)

target_include_directories(
    {name}_{name}
    ${{{name}_warning_guard}}
    INTERFACE
    "$<BUILD_INTERFACE:${{PROJECT_SOURCE_DIR}}/include>"
)

target_compile_features({name}_{name} INTERFACE cxx_std_{std})
"""

executable = """
add_executable({name}_{name} source/main.cpp)
add_executable({name}::{name} ALIAS {name}_{name})

set_target_properties(
    {name}_{name} PROPERTIES
    OUTPUT_NAME {name}
    EXPORT_NAME {name}
)

target_compile_features({name}_{name} PRIVATE cxx_std_{std})

target_link_libraries({name}_{name} PRIVATE {name}_lib)
"""

type_id_map = {
    "s": shared_library,
    "h": header_only_library,
    "e": executable,
}

install_rules = """\
if(PROJECT_IS_TOP_LEVEL)
  set(CMAKE_INSTALL_INCLUDEDIR include/{name} CACHE PATH "")
endif()

include(CMakePackageConfigHelpers)
include(GNUInstallDirs){includes}

install(
    TARGETS {name}_{name}
    EXPORT {name}Targets{rules}
)

write_basic_package_version_file(
    {name}ConfigVersion.cmake
    COMPATIBILITY SameMajorVersion{arch_independent}
)

set(
    {name}_INSTALL_CMAKEDIR "${{CMAKE_INSTALL_LIBDIR}}/cmake/{name}"
    CACHE STRING "CMake package config location relative to the install prefix"
)

mark_as_advanced({name}_INSTALL_CMAKEDIR)

install(
    FILES
    "${{PROJECT_SOURCE_DIR}}/cmake/{name}Config.cmake"
    "${{PROJECT_BINARY_DIR}}/{name}ConfigVersion.cmake"
    DESTINATION "${{{name}_INSTALL_CMAKEDIR}}"
    COMPONENT {name}_Development
)

install(
    EXPORT {name}Targets
    NAMESPACE {name}::
    DESTINATION "${{{name}_INSTALL_CMAKEDIR}}"
    COMPONENT {name}_Development
)

if(PROJECT_IS_TOP_LEVEL)
  include(CPack)
endif()
"""

windows_set_path = """\
# This function will add shared libraries to the PATH when running the test, so
# they can be found. Windows does not support RPATH or similar. See:
# https://docs.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order
# Usage: windows_set_path(<test> <target>...)
function(windows_set_path TEST)
  if(NOT CMAKE_HOST_SYSTEM_NAME STREQUAL "Windows")
    return()
  endif()

  set(path "")
  set(glue "")
  foreach(target IN LISTS ARGN)
    get_target_property(type "${target}" TYPE)
    if(type STREQUAL "SHARED_LIBRARY")
      set(path "${path}${glue}$<TARGET_FILE_DIR:${target}>")
      set(glue "\\;") # backslash is important
    endif()
  endforeach()
  if(NOT path STREQUAL "")
    set_property(TEST "${TEST}" PROPERTY ENVIRONMENT "PATH=${path}")
  endif()
endfunction()
"""

test_cml_top = """\
cmake_minimum_required(VERSION 3.14)

project({name}Tests LANGUAGES CXX)

include(../cmake/project-is-top-level.cmake)
%s
if(PROJECT_IS_TOP_LEVEL)
  find_package({name} REQUIRED)
  enable_testing()
endif()

add_executable({name}_test source/{name}_test.cpp)
target_link_libraries({name}_test PRIVATE {name}::{name})
target_compile_features({name}_test PRIVATE cxx_std_{std})

add_test(NAME {name}_test COMMAND {name}_test)
"""

test_exe_cml_top = """\
# Parent project does not export its library target, so this CML implicitly
# depends on being added from it, i.e. the testing is done only from the build
# tree and is not feasible from an install location

add_executable({name}_test source/{name}_test.cpp)
target_link_libraries({name}_test PRIVATE {name}_lib)
target_compile_features({name}_test PRIVATE cxx_std_{std})

add_test(NAME {name}_test COMMAND {name}_test)%s
"""

gitignore = """\
build/
prefix/
CMakeUserPresets.json
"""

ci_yaml = """\
name: Continuous Integration

on:
  push:
    branches:
    - master

  pull_request:
    branches:
    - master

jobs:
  test:
    strategy:
      matrix:
        os: [macos, ubuntu, windows]
%s
    runs-on: ${{ matrix.os }}-latest

    steps:
    - uses: actions/checkout@v1

    - name: Configure
      run: cmake --preset=ci-${{ matrix.os }}%s

    - name: Build
      run: cmake --build build --config Release -j 2

    - name: Install
      run: cmake --install build --config Release --prefix prefix

    - name: Test
      working-directory: build
      run: ctest -C Release -j 2
"""

cmake_presets = """\
{
  "version": 1,
  "cmakeMinimumRequired": {
    "major": 3,
    "minor": 14,
    "patch": 0
  },
  "configurePresets": [
    {
      "name": "ci-build",
      "binaryDir": "${sourceDir}/build",
      "hidden": true
    },
    {
      "name": "ci-unix",
      "generator": "Unix Makefiles",
      "hidden": true,
      "inherits": "ci-build",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    },
    {
      "name": "ci-macos",
      "inherits": "ci-unix"
    },
    {
      "name": "ci-ubuntu",
      "inherits": "ci-unix"
    },
    {
      "name": "ci-windows",
      "inherits": "ci-build",
      "generator": "Visual Studio 16 2019",
      "architecture": "x64"
    }
  ]
}
"""

cmake_user_presets = """\
{
  "version": 1,
  "cmakeMinimumRequired": {
    "major": 3,
    "minor": 14,
    "patch": 0
  },
  "configurePresets": [
    {
      "name": "dev",
      "binaryDir": "${sourceDir}/build",
      "generator": "%s",
      "cacheVariables": {
        "CMAKE_CXX_FLAGS": "%s",
        "%s_DEVELOPER_MODE": "ON"%s
      }
    }
  ]
}
"""

executable_h = """\
#pragma once

#include <string>

struct library {
  library();

  std::string name;
};
"""

executable_cpp = """\
#include <iostream>
#include <string>

#include <lib.h>

int main() {{
  library lib;
  std::string message = "Hello from " + lib.name + "!";
  std::cout << message << '\\n';
  return 0;
}}
"""

executable_lib_cpp = """\
#include <lib.h>

library::library() : name("{name}")
{{}}
"""

header_only_h = """\
#pragma once

#include <string>

inline std::string name() {{
  return "{name}";
}}
"""

shared_h = """\
#pragma once

#include <string>

#include <{name}/{name}_export.h>

class {uc_name}_EXPORT exported_class {{
public:
  exported_class();

  std::string name();

private:
  std::string name_;
}};
"""

shared_cpp = """\
#include <string>

#include <{name}/{name}.h>

exported_class::exported_class() : name_("{name}") {{}}

std::string exported_class::name() {{
  return name_;
}}
"""

test_cpp = "#include <{name}/{name}.h>\n"


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
            cli_args.type or "e",
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
        "exclude_examples": "y",
        "shared_libs": "",
        "includes": "",
        "arch_independent": "",
        "rules": "",
    }
    name = d["name"]
    type = d["type_id"]
    if type == "s":
        d["shared_libs"] = \
            "  option(BUILD_SHARED_LIBS \"Build shared libs.\" OFF)"
        d["includes"] = f"""

install(
    DIRECTORY
    "${{PROJECT_SOURCE_DIR}}/include/"
    "${{PROJECT_BINARY_DIR}}/include/"
    DESTINATION "${{CMAKE_INSTALL_INCLUDEDIR}}"
    COMPONENT {name}_Development
)"""
        d["rules"] = f"""
    RUNTIME #
    COMPONENT {name}_Runtime
    LIBRARY #
    COMPONENT {name}_Runtime
    NAMELINK_COMPONENT {name}_Development
    ARCHIVE #
    COMPONENT {name}_Development
    INCLUDES #
    DESTINATION "${{CMAKE_INSTALL_INCLUDEDIR}}\""""
    elif type == "h":
        d["cmake_version"] = "14"
        d["arch_independent"] = "\n    ARCH_INDEPENDENT"
        d["rules"] = \
            "\n    INCLUDES DESTINATION \"${CMAKE_INSTALL_INCLUDEDIR}\""
        d["includes"] = f"""

install(
    DIRECTORY "${{PROJECT_SOURCE_DIR}}/include/"
    DESTINATION "${{CMAKE_INSTALL_INCLUDEDIR}}"
    COMPONENT {name}_Development
)"""
    elif type == "e":
        d["rules"] = f"\n    RUNTIME COMPONENT {name}_Runtime"
    if type != "e":
        d["exclude_examples"] = ask(
            "Exclude examples ([Y]es/[n]o)",
            "y",
            mapper=lambda v: v.lower(),
            predicate=lambda v: v in ["y", "n"],
        )
    d["uc_name"] = d["name"].upper().replace("-", "_")
    return d


def root_dir(d):
    type = d["type_id"]
    warnings = "-Wall -Wextra -pedantic"
    generator = "Unix Makefiles"
    config = ",\n        \"CMAKE_BUILD_TYPE\": \"Release\""
    if os.name == "nt":
        warnings = "/W4 /permissive-"
        generator = "Visual Studio 16 2019"
        config = ""
    matrix = ""
    shared_option = ""
    if type == "s":
        matrix = """
        type: [shared, static]

        include:
        - { type: shared, shared: YES }
        - { type: static, shared: NO }
"""
        shared_option = \
            "\n        -D BUILD_SHARED_LIBS=${{ matrix.shared }}"
    root_cml = [root_cml_top, type_id_map[type], root_cml_bottom]
    if d["exclude_examples"] == "n":
        root_cml.append("""
option(BUILD_EXAMPLES "Build examples tree." ON)
if(BUILD_EXAMPLES)
  add_subdirectory(example)
endif()
""")
    if type == "e":
        root_cml.insert(1, """
add_library(
    {name}_lib OBJECT
    include/lib.h
    source/lib.cpp
)

target_include_directories(
    {name}_lib
    ${{{name}_warning_guard}}
    PUBLIC
    "$<BUILD_INTERFACE:${{PROJECT_SOURCE_DIR}}/include>"
)

target_compile_features({name}_lib PUBLIC cxx_std_{std})

# ---- Declare executable ----
""")
        root_cml.append("""
add_custom_target(
    run_exe
    COMMAND "$<TARGET_FILE:{name}_{name}>"
    VERBATIM
)
""")
    return {
        ".github": {
            "workflows": {
                "ci.yml": ci_yaml % (matrix, shared_option),
            },
        },
        ".gitignore": gitignore,
        "CMakeLists.txt": [s.format(**d) for s in root_cml],
        "CMakePresets.json": cmake_presets,
        "CMakeUserPresets.json":
            cmake_user_presets % (generator, warnings, d["name"], config),
    }


def cmake_dir(d):
    name = d["name"]
    return {
        f"{name}Config.cmake":
            f"include(${{CMAKE_CURRENT_LIST_DIR}}/{name}Targets.cmake)\n",
        "variables.cmake": variables.format(**d),
        "in-source-guard.cmake": in_source_guard,
        "project-is-top-level.cmake": project_is_top_level.format(**d),
        "install-rules.cmake": install_rules.format(**d),
        "windows-set-path.cmake": windows_set_path,
    }


def test_dir(d):
    test = [test_cpp.format(**d)]
    name = d["name"]
    type = d["type_id"]
    cml = test_cml_top
    set_path = ""
    add_path = ""
    if type == "h":
        test.append("""
int main() {
  auto result = name();
  return result == "%s" ? 0 : 1;
}
""" % (name,))
    elif type == "s":
        set_path = "include(../cmake/windows-set-path.cmake)\n"
        add_path = "windows_set_path({name}_test {name}::{name})\n"
        test.append("""
int main() {
  exported_class e;

  return e.name() == "%s" ? 0 : 1;
}
""" % (name,))
    elif type == "e":
        cml = test_exe_cml_top
        test = """\
#include <lib.h>

int main() {{
  library l;

  return l.name == "{name}" ? 0 : 1;
}}
""".format(**d)
    return {
        "CMakeLists.txt": map(
            lambda s: s.format(**d),
            [cml % (set_path,), add_path],
        ),
        "source": {
            d["name"] + "_test.cpp": test,
        },
    }


def include_dir(d):
    name = d["name"]
    type = d["type_id"]
    if type == "e":
        return {
            "lib.h": executable_h,
        }
    return {
        name: {
            f"{name}.h":
                (header_only_h if type == "h" else shared_h).format(**d),
        }
    }


def source_dir(d):
    if d["type_id"] != "e":
        return {
            d["name"] + ".cpp": shared_cpp.format(**d),
        }
    return {
        "lib.cpp": executable_lib_cpp.format(**d),
        "main.cpp": executable_cpp.format(**d),
    }


def example_dir(d):
    return {
        "empty_example.cpp": "int main() {\n  return 0;\n}\n",
        "CMakeLists.txt": """\
cmake_minimum_required(VERSION 3.14)

project({name}Examples CXX)

include(../cmake/project-is-top-level.cmake)

if(PROJECT_IS_TOP_LEVEL)
  find_package({name} REQUIRED)
endif()

add_custom_target(run_examples)

function(add_example NAME)
  add_executable("${{NAME}}" "${{NAME}}.cpp")
  target_link_libraries("${{NAME}}" PRIVATE {name}::{name})
  target_compile_features("${{NAME}}" PRIVATE cxx_std_{std})
  add_custom_target(
      "run_${{NAME}}"
      COMMAND "$<TARGET_FILE:${{NAME}}>"
      VERBATIM
  )
  add_dependencies(run_examples "run_${{NAME}}")
endfunction()

add_example(empty_example)
""".format(**d),
    }


def join(path, *paths):
    return os.path.join(path, *paths)


def write_dir(path, tree):
    for name, content in tree.items():
        if isinstance(content, tuple):
            keep, f, *args = content
            if not keep:
                continue
            content = f(*args)
        if isinstance(content, dict):
            dir = join(path, name)
            os.mkdir(dir)
            write_dir(dir, content)
            continue
        fragments = [content] if isinstance(content, str) else content
        with open(join(path, name), "w", newline="\n") as f:
            for fragment in fragments:
                f.write(fragment)


def git_init(cwd):
    subprocess.run("git init", shell=True, check=True, cwd=cwd)
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
    if d["exclude_examples"] == "y" and d["type_id"] != "e":
        return
    print("""\
There are some convenience targets that you can run to invoke some built
executables conveniently:
""")
    if d["exclude_examples"] == "n":
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
    project = {
        **root_dir(d),
        "cmake": cmake_dir(d),
        "test": test_dir(d),
        "include": include_dir(d),
        "source": (d["type_id"] != "h", source_dir, d),
        "example": (d["exclude_examples"] == "n", example_dir, d),
    }
    if not root_exists:
        os.mkdir(path)
    write_dir(path, project)
    git_init(path)
    print_tips(d)
    print("""\
Now make sure you have at least CMake 3.19 installed for local development, to
make use of all the nice Quality-of-Life improvements in newer releases:
https://cmake.org/download/

For more tips, like integration with package managers, please see the Wiki:
http://github.com/friendlyanon/cmake-init/wiki

You are all set. Have fun programming and create something awesome!""")


def uncomment():
    # TODO: litter the generated files with copious amounts of comments in a
    #  way that makes them easy to remove with this script, so they don't end
    #  up in VCS, as the comments would be there only to explain rationale and
    #  CMake behavior for the developer
    pass


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--version", action="version", version=__version__)
    subps = p.add_subparsers(dest="subcommand")
    create_p = subps.add_parser("create", description=create.__doc__)
    create_p.add_argument("path", type=os.path.realpath)
    create_p.set_defaults(func=create, type="", std="")
    create_type_g = create_p.add_mutually_exclusive_group()
    for type, flags in {"s": ["-s"], "e": ["-e", "-y"], "h": ["-ho"]}.items():
        create_type_g.add_argument(
            *flags,
            dest="type",
            action="store_const",
            const=type,
        )
    create_p.add_argument(
        "--std",
        choices=["11", "14", "17", "20"],
    )
    args = p.parse_args()
    if args.subcommand is None:
        p.print_help()
    else:
        setattr(args, "flags_used", args.type != "" or args.std != "")
        args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
