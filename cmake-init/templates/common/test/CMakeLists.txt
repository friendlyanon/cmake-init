cmake_minimum_required(VERSION 3.14)

project({= name =}Tests LANGUAGES C{% if cpp %}XX{% end %})

include(../cmake/project-is-top-level.cmake)
include(../cmake/folders.cmake)
include(../cmake/windows-set-path.cmake)

if(PROJECT_IS_TOP_LEVEL)
  find_package({= name =} REQUIRED)
  enable_testing()
endif()

add_executable({= name =}_test source/{= name =}_test.c{% if cpp %}pp{% end %})
target_link_libraries({= name =}_test PRIVATE {= name =}::{= name =})
target_compile_features({= name =}_test PRIVATE c{% if cpp %}xx{% end %}_std_{= std =}){% if c_header %}
set_property(
    SOURCE source/{= name =}_test.c PROPERTY
    COMPILE_DEFINITIONS {= uc_name =}_IMPLEMENTATION
){% end %}

add_test(NAME {= name =}_test COMMAND {= name =}_test){% if lib %}
windows_set_path({= name =}_test {= name =}::{= name =}){% end %}

add_folders(Test)
