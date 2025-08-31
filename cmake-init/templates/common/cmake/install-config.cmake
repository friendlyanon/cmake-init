{% if pm %}set({= name =}_FOUND YES)

{% end %}foreach(comp IN LISTS {= name =}_FIND_COMPONENTS)
  if(DEFINED "{= name =}_FIND_REQUIRED_${comp}" AND "${{= name =}_FIND_REQUIRED_${comp}}")
    set({= name =}_FOUND NO)
    set({= name =}_NOT_FOUND_MESSAGE "This package has no components")
    return()
  endif()
endforeach()

{% if pm %}include(CMakeFindDependencyMacro)
find_dependency({% if c %}json-c{% else %}fmt{% end %})

if({= name =}_FOUND)
  {% end %}include("${CMAKE_CURRENT_LIST_DIR}/{= name =}Targets.cmake"){% if pm %}
endif(){% end %}
