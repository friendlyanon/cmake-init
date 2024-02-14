cmake_minimum_required(VERSION 3.14)

include(cmake/prelude.cmake)

project(
    {= name =}
    VERSION {= version =}
    DESCRIPTION "{= description =}"
    HOMEPAGE_URL "{= homepage =}"
    LANGUAGES NONE
)

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Declare library ----

add_library({= name =}_{= name =} INTERFACE)
add_library({= name =}::{= name =} ALIAS {= name =}_{= name =})

set_property(
    TARGET {= name =}_{= name =} PROPERTY
    EXPORT_NAME {= name =}
)

target_include_directories(
    {= name =}_{= name =} ${warning_guard}
    INTERFACE
    "\$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
)

target_compile_features({= name =}_{= name =} INTERFACE cxx_std_{= std =}){% if pm %}

find_package(fmt REQUIRED)
target_link_libraries({= name =}_{= name =} INTERFACE fmt::fmt){% end %}

# ---- Install rules ----

if(NOT CMAKE_SKIP_INSTALL_RULES)
  include(cmake/install-rules.cmake)
endif(){% if cpp_examples %}

# ---- Examples ----

if(PROJECT_IS_TOP_LEVEL)
  option(BUILD_EXAMPLES "Build examples tree." "${{= name =}_DEVELOPER_MODE}")
  if(BUILD_EXAMPLES)
    add_subdirectory(example)
  endif()
endif(){% end %}

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
