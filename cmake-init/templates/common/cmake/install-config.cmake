{% if pm %}set({= name =}_FOUND YES)

include(CMakeFindDependencyMacro)
find_dependency({% if c %}json-c{% else %}fmt{% end %})

if({= name =}_FOUND)
  {% end %}include("${CMAKE_CURRENT_LIST_DIR}/{= name =}Targets.cmake"){% if pm %}
endif(){% end %}
