include(cmake/folders.cmake)

set_property(GLOBAL PROPERTY CTEST_TARGETS_ADDED 1)
include(CTest)
if(BUILD_TESTING)
  add_subdirectory(test)
endif()
{% if exe %}
add_custom_target(
    run-exe
    COMMAND {= name =}_exe
    VERBATIM
)
add_dependencies(run-exe {= name =}_exe)
{% end %}
option(BUILD_MCSS_DOCS "Build documentation using Doxygen and m.css" OFF)
if(BUILD_MCSS_DOCS)
  include(cmake/docs.cmake)
endif()

option(ENABLE_COVERAGE "Enable coverage support separate from CTest's" OFF)
if(ENABLE_COVERAGE)
  include(cmake/coverage.cmake)
endif()

include(cmake/lint-targets.cmake)
include(cmake/spell-targets.cmake)

add_folders(Project)
