cmake_minimum_required(VERSION 3.14)

include(cmake/prelude.cmake)

project(
    {= name =}
    VERSION {= version =}
    DESCRIPTION "{= description =}"
    HOMEPAGE_URL "{= homepage =}"
    LANGUAGES C
)

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Declare library ----

add_library(
    {= name =}_lib OBJECT
    source/lib.c
)

target_include_directories(
    {= name =}_lib ${warning_guard}
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/source>"
)

target_compile_features({= name =}_lib PUBLIC c_std_{= std =}){% if pm %}

find_package(json-c REQUIRED)
target_link_libraries({= name =}_lib PRIVATE json-c::json-c)

# Unfortunately, hedley provides no CMake package to be found trivially using
# find_package, so it has to be found manually
find_path(HEDLEY_INCLUDE_DIR hedley.h)
if(NOT HEDLEY_INCLUDE_DIR)
  message(FATAL_ERROR "Couldn't find hedley.h (${HEDLEY_INCLUDE_DIR})")
endif()
target_include_directories(
    {= name =}_lib SYSTEM
    PRIVATE "${HEDLEY_INCLUDE_DIR}"
){% end %}

# ---- Declare executable ----

add_executable({= name =}_exe source/main.c)
add_executable({= name =}::exe ALIAS {= name =}_exe)

set_property(TARGET {= name =}_exe PROPERTY OUTPUT_NAME {= name =})

target_compile_features({= name =}_exe PRIVATE c_std_{= std =})

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
