cmake_minimum_required(VERSION 3.14)

include(cmake/prelude.cmake)

project(
    %(name)s
    VERSION %(version)s
    DESCRIPTION "%(description)s"
    HOMEPAGE_URL "%(homepage)s"
    LANGUAGES C
) #

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Declare library ----

add_library(
    %(name)s_%(name)s
    source/%(name)s.c
)
add_library(%(name)s::%(name)s ALIAS %(name)s_%(name)s)

include(GenerateExportHeader)
generate_export_header(
    %(name)s_%(name)s
    BASE_NAME %(name)s
    EXPORT_FILE_NAME export/%(name)s/%(name)s_export.h
)

if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(%(name)s_%(name)s PUBLIC %(uc_name)s_STATIC_DEFINE)
endif()

set_target_properties(
    %(name)s_%(name)s PROPERTIES
    C_VISIBILITY_PRESET hidden
    VERSION "${PROJECT_VERSION}"
    SOVERSION "${PROJECT_VERSION_MAJOR}"
    EXPORT_NAME %(name)s
    OUTPUT_NAME %(name)s
)

target_include_directories(
    %(name)s_%(name)s ${warning_guard}
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
)

target_include_directories(
    %(name)s_%(name)s SYSTEM
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/export>"
)

target_compile_features(%(name)s_%(name)s PUBLIC c_std_%(std)s)

# ---- Install rules ----

if(NOT CMAKE_SKIP_INSTALL_RULES)
  include(cmake/install-rules.cmake)
endif(){if c_examples}

# ---- Examples ----

if(PROJECT_IS_TOP_LEVEL)
  option(BUILD_EXAMPLES "Build examples tree." "${%(name)s_DEVELOPER_MODE}")
  if(BUILD_EXAMPLES)
    add_subdirectory(example)
  endif()
endif(){end}

# ---- Developer mode ----

if(NOT %(name)s_DEVELOPER_MODE)
  return()
elseif(NOT PROJECT_IS_TOP_LEVEL)
  message(
      AUTHOR_WARNING
      "Developer mode is intended for developers of %(name)s"
  )
endif()

include(cmake/dev-mode.cmake)
