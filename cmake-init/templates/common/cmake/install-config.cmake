{% if pm %}include(CMakeFindDependencyMacro)
{% if lib %}
if(NOT "@BUILD_SHARED_LIBS@")
  {% end %}find_dependency({% if c %}json-c{% else %}fmt{% end %}){% if lib %}
endif(){% end %}

{% end %}include("${CMAKE_CURRENT_LIST_DIR}/{= name =}Targets.cmake")
