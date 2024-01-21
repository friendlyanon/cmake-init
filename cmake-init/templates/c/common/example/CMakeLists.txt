cmake_minimum_required(VERSION 3.{% if cmake_321 %}21{% else %}14{% end %})

project({= name =}Examples C)
{% if not cmake_321 %}
include(../cmake/project-is-top-level.cmake){% end %}
include(../cmake/folders.cmake)

if(PROJECT_IS_TOP_LEVEL)
  find_package({= name =} REQUIRED)
endif()

add_custom_target(run-examples)

function(add_example NAME)
  add_executable("${NAME}" "${NAME}.c")
  target_link_libraries("${NAME}" PRIVATE {= name =}::{= name =})
  target_compile_features("${NAME}" PRIVATE c_std_{= std =})
  add_custom_target("run_${NAME}" COMMAND "${NAME}" VERBATIM)
  add_dependencies("run_${NAME}" "${NAME}")
  add_dependencies(run-examples "run_${NAME}")
endfunction()

add_example(empty_example)

add_folders(Example)
