# ---- Developer mode ----

# Developer mode enables targets and code paths in the CMake scripts that are
# only relevant for the developer(s) of {= name =}
# Targets necessary to build the project must be provided unconditionally, so
# consumers can trivially build and package the project
if(PROJECT_IS_TOP_LEVEL)
  option({= name =}_DEVELOPER_MODE "Enable developer mode" OFF){% if lib %}
  option(BUILD_SHARED_LIBS "Build shared libs." OFF){% end %}
endif()

{% if cpp and lib %}# ---- Suppress C4251 on Windows ----

# Please see include/{= name =}/{= name =}.hpp for more details
set(pragma_suppress_c4251 "
/* This needs to suppress only for MSVC */
#if defined(_MSC_VER) && !defined(__ICL)
#  define {= uc_name =}_SUPPRESS_C4251 _Pragma(\"warning(suppress:4251)\")
#else
#  define {= uc_name =}_SUPPRESS_C4251
#endif
")

{% end %}# ---- Warning guard ----

# target_include_directories with the SYSTEM modifier will request the compiler
# to omit warnings from the provided paths, if the compiler supports that
# This is to provide a user experience similar to find_package when
# add_subdirectory or FetchContent is used to consume this project
set(warning_guard "")
if(NOT PROJECT_IS_TOP_LEVEL)
  option(
      {= name =}_INCLUDES_WITH_SYSTEM
      "Use SYSTEM modifier for {= name =}'s includes, disabling warnings"
      ON
  )
  mark_as_advanced({= name =}_INCLUDES_WITH_SYSTEM)
  if({= name =}_INCLUDES_WITH_SYSTEM)
    set(warning_guard SYSTEM)
  endif()
endif()
