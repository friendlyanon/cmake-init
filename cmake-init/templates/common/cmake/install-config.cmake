{% if pm %}include(CMakeFindDependencyMacro)
find_dependency({% if c %}json-c{% else %}fmt{% end %})

{% end %}include("${CMAKE_CURRENT_LIST_DIR}/{= name =}Targets.cmake")
