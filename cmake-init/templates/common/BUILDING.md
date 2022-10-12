# Building with CMake{% if pm %}

## Dependencies

For a list of dependencies, please refer to {% if vcpkg %}[vcpkg.json](vcpkg.json){% else %}[conanfile.py](conanfile.py){% end %}.{% end %}

## Build

This project doesn't require any special command-line flags to build to keep
things simple.

Here are the steps for building in release mode with a single-configuration
generator, like the Unix Makefiles one:

```sh
cmake -S . -B build -D CMAKE_BUILD_TYPE=Release
cmake --build build
```

Here are the steps for building in release mode with a multi-configuration
generator, like the Visual Studio ones:

```sh
cmake -S . -B build
cmake --build build --config Release
```

### Building with MSVC

Note that MSVC by default is not standards compliant and you need to pass some
flags to make it behave properly. See the `flags-windows` preset in the
[CMakePresets.json](CMakePresets.json) file for the flags and with what
variable to provide them to CMake during configuration.

### Building on Apple Silicon

CMake supports building on Apple Silicon properly since 3.20.1. Make sure you
have the [latest version][1] installed.

## Install

This project doesn't require any special command-line flags to install to keep
things simple. As a prerequisite, the project has to be built with the above
commands already.

The below commands require at least CMake 3.15 to run, because that is the
version in which [Install a Project][2] was added.

Here is the command for installing the release mode artifacts with a
single-configuration generator, like the Unix Makefiles one:

```sh
cmake --install build
```

Here is the command for installing the release mode artifacts with a
multi-configuration generator, like the Visual Studio ones:

```sh
cmake --install build --config Release
```
{% if not exe %}
### CMake package

This project exports a CMake package to be used with the [`find_package`][3]
command of CMake:

* Package name: `{= name =}`
* Target name: `{= name =}::{= name =}`

Example usage:

```cmake
find_package({= name =} REQUIRED)
# Declare the imported target as a build requirement using PRIVATE, where
# project_target is a target created in the consuming project
target_link_libraries(
    project_target PRIVATE
    {= name =}::{= name =}
)
```

### Creating a VCPKG port
If you wish to expose your package on vcpkg the following `portfile.cmake`

```cmake
vcpkg_from_github(
  OUT_SOURCE_PATH SOURCE_PATH
  REPO <org_name/repo_name>
  REF <insert git ref here>
  HEAD_REF master
  SHA512 <insert sha here>
)

vcpkg_cmake_configure(
  SOURCE_PATH "${SOURCE_PATH}"
  OPTIONS
  "-DCMAKE_INSTALL_INCLUDEDIR=${CURRENT_PACKAGES_DIR}/include"
)

vcpkg_cmake_build()

vcpkg_cmake_install()

vcpkg_cmake_config_fixup()

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

file(INSTALL "${SOURCE_PATH}/LICENSE" DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}" RENAME copyright)
```

{% end %}
[1]: https://cmake.org/download/
[2]: https://cmake.org/cmake/help/latest/manual/cmake.1.html#install-a-project{% if not exe %}
[3]: https://cmake.org/cmake/help/latest/command/find_package.html{% end %}
