cmake_minimum_required(VERSION 3.14)

include(cmake/prelude.cmake)

project(
    %(name)s
    VERSION %(version)s
    DESCRIPTION "%(description)s"
    HOMEPAGE_URL "%(homepage)s"
    LANGUAGES C
)

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Declare library ----

add_library(
    %(name)s_lib OBJECT
    source/lib.c
)

target_include_directories(
    %(name)s_lib ${warning_guard}
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/source>"
)

target_compile_features(%(name)s_lib PUBLIC c_std_%(std)s)

# ---- Declare executable ----

add_executable(%(name)s_exe source/main.c)
add_executable(%(name)s::exe ALIAS %(name)s_exe)

set_target_properties(
    %(name)s_exe PROPERTIES
    OUTPUT_NAME %(name)s
    EXPORT_NAME exe
)

target_compile_features(%(name)s_exe PRIVATE c_std_%(std)s)

target_link_libraries(%(name)s_exe PRIVATE %(name)s_lib)

# ---- Install rules ----

if(NOT CMAKE_SKIP_INSTALL_RULES)
  include(cmake/install-rules.cmake)
endif()

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
