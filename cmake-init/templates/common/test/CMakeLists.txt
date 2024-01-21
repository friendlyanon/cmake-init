{% if exe %}# Parent project does not export its library target, so this CML implicitly
# depends on being added from it, i.e. the testing is done only from the build
# tree and is not feasible from an install location{% else %}cmake_minimum_required(VERSION 3.{% if cmake_321 %}21{% else %}14{% end %}){% end %}

project({= name =}Tests LANGUAGES C{% if cpp or pm %}{% if c_header %} C{% end %}XX{% end %}){% if not exe %}
{% if not cmake_321 %}
include(../cmake/project-is-top-level.cmake){% end %}
include(../cmake/folders.cmake)

# ---- Dependencies ----

if(PROJECT_IS_TOP_LEVEL)
  find_package({= name =} REQUIRED)
  enable_testing()
endif(){% end %}{% if pm %}{% if exe %}

# ---- Dependencies ----{% end %}

find_package(Catch2 REQUIRED)
include(Catch){% end %}

# ---- Tests ----

add_executable({% if c_header and pm %}
    {% end %}{= name =}_test{% if c_header and pm %}
   {% end %} source/{= name =}_test.c{% if cpp or pm %}pp{% if c_header %}
    source/header_impl.c
{% end %}{% end %}){% if c_header and not pm %}
set_property(
    SOURCE source/{= name =}_test.c PROPERTY
    COMPILE_DEFINITIONS {= uc_name =}_IMPLEMENTATION
){% end %}
target_link_libraries({% if pm %}
    {% end %}{= name =}_test PRIVATE{% if pm %}
   {% end %} {= name =}{% if exe %}_lib{% else %}::{= name =}{% end %}{% if pm %}
    Catch2::Catch2WithMain
{% end %})
target_compile_features({= name =}_test PRIVATE {% if c and pm %}{% if header %}c_std_{= std =} {% end %}cxx_std_11{% else %}c{% if cpp %}xx{% end %}_std_{= std =}{% end %})
{% if pm %}
catch_discover_tests({= name =}_test){% else %}
add_test(NAME {= name =}_test COMMAND {= name =}_test){% end %}

# ---- End-of-file commands ----

add_folders(Test)
