cmake_minimum_required(VERSION 3.14)

project(%(name)sTests LANGUAGES C{if cpp}XX{end})

include(../cmake/project-is-top-level.cmake)
include(../cmake/folders.cmake)
include(../cmake/windows-set-path.cmake)

if(PROJECT_IS_TOP_LEVEL)
  find_package(%(name)s REQUIRED)
  enable_testing()
endif()

add_executable(%(name)s_test source/%(name)s_test.c{if cpp}pp{end})
target_link_libraries(%(name)s_test PRIVATE %(name)s::%(name)s)
target_compile_features(%(name)s_test PRIVATE c{if cpp}xx{end}_std_%(std)s){if c_header}
set_property(
    SOURCE source/%(name)s_test.c PROPERTY
    COMPILE_DEFINITIONS %(uc_name)s_IMPLEMENTATION
){end}

add_test(NAME %(name)s_test COMMAND %(name)s_test){type shared}
windows_set_path(%(name)s_test %(name)s::%(name)s){end}

add_folders(Test)
