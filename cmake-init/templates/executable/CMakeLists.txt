cmake_minimum_required(VERSION 3.14)

include(cmake/prelude.cmake)

project(
    {= name =}
    VERSION {= version =}
    DESCRIPTION "{= description =}"
    HOMEPAGE_URL "{= homepage =}"
    LANGUAGES CXX
)

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Declare library ----

add_library(
    {= name =}_lib OBJECT
    source/lib.cpp
)

target_include_directories(
    {= name =}_lib ${warning_guard}
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/source>"
)

target_compile_features({= name =}_lib PUBLIC cxx_std_{= std =}){% if pm %}

find_package(fmt REQUIRED)
target_link_libraries({= name =}_lib PRIVATE fmt::fmt){% end %}

# ---- Declare executable ----

add_executable({= name =}_exe source/main.cpp)
add_executable({= name =}::exe ALIAS {= name =}_exe)

set_target_properties(
    {= name =}_exe PROPERTIES
    OUTPUT_NAME {= name =}
    EXPORT_NAME exe
)

target_compile_features({= name =}_exe PRIVATE cxx_std_{= std =})

target_link_libraries({= name =}_exe PRIVATE {= name =}_lib)

# ---- Install rules ----

if(NOT CMAKE_SKIP_INSTALL_RULES)
  include(cmake/install-rules.cmake)
endif()

# ---- Developer mode ----

if(NOT {= name =}_DEVELOPER_MODE)
  return()
elseif(NOT PROJECT_IS_TOP_LEVEL)
  message(
      AUTHOR_WARNING
      "Developer mode is intended for developers of {= name =}"
  )
endif()

include(cmake/dev-mode.cmake)
