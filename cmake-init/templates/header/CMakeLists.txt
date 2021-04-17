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

add_library(%(name)s_%(name)s INTERFACE)
add_library(%(name)s::%(name)s ALIAS %(name)s_%(name)s)

set_property(
    TARGET %(name)s_%(name)s PROPERTY
    EXPORT_NAME %(name)s
)

target_include_directories(
    %(name)s_%(name)s
    ${%(name)s_warning_guard}
    INTERFACE
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
)

target_compile_features(%(name)s_%(name)s INTERFACE cxx_std_%(std)s)

# ---- Install rules ----

include(cmake/install-rules.cmake)

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
endif(){if examples}

option(BUILD_EXAMPLES "Build examples tree." ON)
if(BUILD_EXAMPLES)
  add_subdirectory(example)
endif(){end}
