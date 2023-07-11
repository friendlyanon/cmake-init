# Hacking

Here is some wisdom to help you build and test this project as a developer and
potential contributor.

If you plan to contribute, please read the [CONTRIBUTING](CONTRIBUTING.md)
guide.

## Developer mode

Build system targets that are only useful for developers of this project are
hidden if the `{= name =}_DEVELOPER_MODE` option is disabled. Enabling this
option makes tests and other developer targets and options available. Not
enabling this option means that you are a consumer of this project and thus you
have no need for these targets and options.

Developer mode is always set to on in CI workflows.

### Presets

This project makes use of [presets][1] to simplify the process of configuring
the project. As a developer, you are recommended to always have the [latest
CMake version][2] installed to make use of the latest Quality-of-Life
additions.

You have a few options to pass `{= name =}_DEVELOPER_MODE` to the configure
command, but this project prefers to use presets.

As a developer, you should create a `CMakeUserPresets.json` file at the root of
the project:

```json
{
  "version": 2,
  "cmakeMinimumRequired": {
    "major": 3,
    "minor": 14,
    "patch": 0
  },
  "configurePresets": [
    {
      "name": "dev",
      "binaryDir": "${sourceDir}/build/dev",
      "inherits": ["dev-mode"{% if pm %}, "{= pm_name =}"{% end %}, "ci-<os>"],
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    }
  ],
  "buildPresets": [
    {
      "name": "dev",
      "configurePreset": "dev",
      "configuration": "Debug"
    }
  ],
  "testPresets": [
    {
      "name": "dev",
      "configurePreset": "dev",
      "configuration": "Debug",
      "output": {
        "outputOnFailure": true
      }
    }
  ]
}
```

You should replace `<os>` in your newly created presets file with the name of
the operating system you have, which may be `win64`, `linux` or `darwin`. You
can see what these correspond to in the
[`CMakePresets.json`](CMakePresets.json) file.

`CMakeUserPresets.json` is also the perfect place in which you can put all
sorts of things that you would otherwise want to pass to the configure command
in the terminal.

> **Note**
> Some editors are pretty greedy with how they open projects with presets.
> Some just randomly pick a preset and start configuring without your consent,
> which can be confusing. Make sure that your editor configures when you
> actually want it to, for example in CLion you have to make sure only the
> `dev-dev preset` has `Enable profile` ticked in
> `File > Settings... > Build, Execution, Deployment > CMake` and in Visual
> Studio you have to set the option `Never run configure step automatically`
> in `Tools > Options > CMake` **prior to opening the project**, after which
> you can manually configure using `Project > Configure Cache`.{% if pm %}

### Dependency manager

The above preset will make use of the [{= pm_name =}][{= pm_name =}] dependency manager. After
installing it, {% if vcpkg %}make sure the `VCPKG_ROOT` environment variable is pointing at
the directory where the vcpkg executable is. On Windows, you might also want
to inherit from the `vcpkg-win64-static` preset, which will make vcpkg install
the dependencies as static libraries. This is only necessary if you don't want
to setup `PATH` to run tests.{% else %}make sure you have a [Conan profile][profile] setup, then
download the dependencies and generate the necessary CMake files by running
this command in the project root:

```sh
conan install . -s build_type=Debug -b missing
```

Note that if your conan profile does not specify the same compiler, standard
level, build type and runtime library as CMake, then that could potentially
cause issues. See the link above for profiles documentation.{% end %}

[{= pm_name =}]: {% if vcpkg %}https://github.com/microsoft/vcpkg{% else %}https://conan.io/
[profile]: https://docs.conan.io/2/reference/config_files/profiles.html{% end %}{% end %}

### Configure, build and test

If you followed the above instructions, then you can configure, build and test
the project respectively with the following commands from the project root on
any operating system with any build system:

```sh
cmake --preset=dev
cmake --build --preset=dev
ctest --preset=dev
```

If you are using a compatible editor (e.g. VSCode) or IDE (e.g. CLion, VS), you
will also be able to select the above created user presets for automatic
integration.

Please note that both the build and test commands accept a `-j` flag to specify
the number of jobs to use, which should ideally be specified to the number of
threads your CPU has. You may also want to add that to your preset using the
`jobs` property, see the [presets documentation][1] for more details.

### Developer mode targets

These are targets you may invoke using the build command from above, with an
additional `-t <target>` flag:

#### `coverage`

Available if `ENABLE_COVERAGE` is enabled. This target processes the output of
the previously run tests when built with coverage configuration. The commands
this target runs can be found in the `COVERAGE_TRACE_COMMAND` and
`COVERAGE_HTML_COMMAND` cache variables. The trace command produces an info
file by default, which can be submitted to services with CI integration. The
HTML command uses the trace command's output to generate an HTML document to
`<binary-dir>/coverage_html` by default.

#### `docs`

Available if `BUILD_MCSS_DOCS` is enabled. Builds to documentation using
Doxygen and m.css. The output will go to `<binary-dir>/docs` by default
(customizable using `DOXYGEN_OUTPUT_DIRECTORY`).

#### `format-check` and `format-fix`

These targets run the clang-format tool on the codebase to check errors and to
fix them respectively. Customization available using the `FORMAT_PATTERNS` and
`FORMAT_COMMAND` cache variables.{% if exe %}

#### `run-exe`

Runs the executable target `{= name =}_exe`.{% end %}{% if examples %}

#### `run-examples`

Runs all the examples created by the `add_example` command.{% end %}

#### `spell-check` and `spell-fix`

These targets run the codespell tool on the codebase to check errors and to fix
them respectively. Customization available using the `SPELL_COMMAND` cache
variable.
{% if lib and not pm %}
## Running tests on Windows with `BUILD_SHARED_LIBS=ON`

If you are building a shared library on Windows, you must add the path to the
DLL file to `PATH` when you want to run tests. One way you could do that is by
using PowerShell and writing a script for it, e.g. `env.ps1` at the project
root:

```powershell
$oldPrompt = (Get-Command prompt).ScriptBlock

function prompt() { "(Debug) $(& $oldPrompt)" }

$VsInstallPath = & "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -Property InstallationPath
$Env:Path += ";$VsInstallPath\Common7\IDE;$Pwd\build\dev\Debug"
```

Then you can source this script by running `. env.ps1`. This particular
example will only work for Debug builds.

### Passing `PATH` to editors

Make sure you launch your editor of choice from the console with the above
script sourced. Look for `(Debug)` in the prompt to confirm, then run e.g.
`code .` for VScode or `devenv .` for Visual Studio.
{% end %}
[1]: https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html
[2]: https://cmake.org/download/
