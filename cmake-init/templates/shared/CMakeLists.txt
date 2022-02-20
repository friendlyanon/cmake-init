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
    {= name =}_{= name =}
    source/{= name =}.cpp
)
add_library({= name =}::{= name =} ALIAS {= name =}_{= name =})

include(GenerateExportHeader)
generate_export_header(
    {= name =}_{= name =}
    BASE_NAME {= name =}
    EXPORT_FILE_NAME export/{= name =}/{= name =}_export.hpp
    CUSTOM_CONTENT_FROM_VARIABLE pragma_suppress_c4251
)

if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions({= name =}_{= name =} PUBLIC {= uc_name =}_STATIC_DEFINE)
endif()

set_target_properties(
    {= name =}_{= name =} PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES
    VERSION "${PROJECT_VERSION}"
    SOVERSION "${PROJECT_VERSION_MAJOR}"
    EXPORT_NAME {= name =}
    OUTPUT_NAME {= name =}
)

target_include_directories(
    {= name =}_{= name =} ${warning_guard}
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
)

target_include_directories(
    {= name =}_{= name =} SYSTEM
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/export>"
)

target_compile_features({= name =}_{= name =} PUBLIC cxx_std_{= std =})

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
