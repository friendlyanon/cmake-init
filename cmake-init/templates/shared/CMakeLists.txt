cmake_minimum_required(VERSION 3.14)

include(cmake/in-source-guard.cmake)

project(
    %(name)s
    VERSION %(version)s
    DESCRIPTION "%(description)s"
    HOMEPAGE_URL "%(homepage)s"
    LANGUAGES CXX
)

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Declare library ----

add_library(
    %(name)s_%(name)s
    source/%(name)s.cpp
)
add_library(%(name)s::%(name)s ALIAS %(name)s_%(name)s)

include(GenerateExportHeader)
generate_export_header(
    %(name)s_%(name)s
    BASE_NAME %(name)s
    EXPORT_FILE_NAME include/%(name)s/%(name)s_export.h
    CUSTOM_CONTENT_FROM_VARIABLE pragma_suppress_c4251
)

if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(%(name)s_%(name)s PUBLIC %(uc_name)s_STATIC_DEFINE)
endif()

set_target_properties(
    %(name)s_%(name)s PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES
    VERSION "${PROJECT_VERSION}"
    SOVERSION "${PROJECT_VERSION_MAJOR}"
    EXPORT_NAME %(name)s
    OUTPUT_NAME %(name)s
)

target_include_directories(
    %(name)s_%(name)s ${%(name)s_warning_guard}
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
    "$<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>"
)

target_compile_features(%(name)s_%(name)s PUBLIC cxx_std_%(std)s)

# ---- Install rules ----

include(cmake/install-rules.cmake){if examples}

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

include(CTest)
if(BUILD_TESTING)
  add_subdirectory(test)
endif()

option(BUILD_DOCUMENTATION "Build documentation using Doxygen and m.css" OFF)
if(BUILD_DOCUMENTATION)
  include(cmake/docs.cmake)
endif()

option(ENABLE_COVERAGE "Enable coverage support separate from CTest's" OFF)
if(ENABLE_COVERAGE)
  include(cmake/coverage.cmake)
endif()
