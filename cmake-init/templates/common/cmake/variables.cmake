# ---- Developer mode ----

# Developer mode enables targets and code paths in the CMake scripts that are
# only relevant for the developer(s) of %(name)s
# Targets necessary to build the project must be provided unconditionally, so
# consumers can trivially build and package the project
if(PROJECT_IS_TOP_LEVEL)
  option(%(name)s_DEVELOPER_MODE "Enable developer mode" OFF){type shared}
  option(BUILD_SHARED_LIBS "Build shared libs." OFF){end}
endif()

{type shared}# ---- Suppress C4251 on Windows ----

# Please see include/%(name)s/%(name)s.h for more details
set(pragma_suppress_c4251 "#define %(uc_name)s_SUPPRESS_C4251")
if(MSVC)
  string(APPEND pragma_suppress_c4251 [[ _Pragma("warning(suppress:4251)")]])
endif()

{end}# ---- Warning guard ----

# target_include_directories with the SYSTEM modifier will request the compiler
# to omit warnings from the provided paths, if the compiler supports that
# This is to provide a user experience similar to find_package when
# add_subdirectory or FetchContent is used to consume this project
set(%(name)s_warning_guard "")
if(NOT PROJECT_IS_TOP_LEVEL)
  option(
      %(name)s_INCLUDES_WITH_SYSTEM
      "Use SYSTEM modifier for %(name)s's includes, disabling warnings"
      ON
  )
  mark_as_advanced(%(name)s_INCLUDES_WITH_SYSTEM)
  if(%(name)s_INCLUDES_WITH_SYSTEM)
    set(%(name)s_warning_guard SYSTEM)
  endif()
endif()
