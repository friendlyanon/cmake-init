# Parent project does not export its library target, so this CML implicitly
# depends on being added from it, i.e. the testing is done only from the build
# tree and is not feasible from an install location

project({= name =}Tests LANGUAGES CXX){% if pm %}

find_package(Catch2 REQUIRED)
include(Catch){% end %}

add_executable({= name =}_test source/{= name =}_test.cpp)
target_link_libraries({% if pm %}
    {% end %}{= name =}_test PRIVATE{% if pm %}
   {% end %} {= name =}_lib{% if pm %}
    Catch2::Catch2WithMain
{% end %})
target_compile_features({= name =}_test PRIVATE cxx_std_{= std =})
{% if pm %}
catch_discover_tests({= name =}_test){% else %}
add_test(NAME {= name =}_test COMMAND {= name =}_test){% end %}

add_folders(Test)
