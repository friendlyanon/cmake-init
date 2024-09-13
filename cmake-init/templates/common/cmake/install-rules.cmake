{% if not exe %}if(PROJECT_IS_TOP_LEVEL)
  set(
      CMAKE_INSTALL_INCLUDEDIR "include/{= name =}-${PROJECT_VERSION}"
      CACHE STRING ""
  )
  set_property(CACHE CMAKE_INSTALL_INCLUDEDIR PROPERTY TYPE PATH)
endif(){% if header %}

# Project is configured with no languages, so tell GNUInstallDirs the lib dir
set(CMAKE_INSTALL_LIBDIR lib CACHE PATH ""){% end %}

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

# find_package(<package>) call for consumers to find this project{% if pm %}
# should match the name of variable set in the install-config.cmake script{% end %}
set(package {= name =})

install(
    DIRECTORY{% if lib %}
   {% end %} include/{% if lib %}
    "${PROJECT_BINARY_DIR}/export/"{% end %}
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
    COMPONENT {= name =}_Development
)

{% end %}install(
    TARGETS {= name =}_{% if exe %}exe{% else %}{= name =}
    EXPORT {= name =}Targets{% end %}{% if exe %}
    RUNTIME COMPONENT {= name =}_Runtime{% end %}{% if lib %}
    RUNTIME #
    COMPONENT {= name =}_Runtime
    LIBRARY #
    COMPONENT {= name =}_Runtime
    NAMELINK_COMPONENT {= name =}_Development
    ARCHIVE #
    COMPONENT {= name =}_Development
    INCLUDES #
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"{% end %}{% if header %}
    INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"{% end %}
){% if not exe %}

write_basic_package_version_file(
    "${package}ConfigVersion.cmake"
    COMPATIBILITY SameMajorVersion{% if header %}
    ARCH_INDEPENDENT{% end %}
)

# Allow package maintainers to freely override the path for the configs
set(
    {= name =}_INSTALL_CMAKEDIR "{% if lib %}${CMAKE_INSTALL_LIBDIR}/cmake{% else %}${CMAKE_INSTALL_DATADIR}{% end %}/${package}"
    CACHE STRING "CMake package config location relative to the install prefix"
)
set_property(CACHE {= name =}_INSTALL_CMAKEDIR PROPERTY TYPE PATH)
mark_as_advanced({= name =}_INSTALL_CMAKEDIR)

install(
    FILES cmake/install-config.cmake
    DESTINATION "${{= name =}_INSTALL_CMAKEDIR}"
    RENAME "${package}Config.cmake"
    COMPONENT {= name =}_Development
)

install(
    FILES "${PROJECT_BINARY_DIR}/${package}ConfigVersion.cmake"
    DESTINATION "${{= name =}_INSTALL_CMAKEDIR}"
    COMPONENT {= name =}_Development
)

install(
    EXPORT {= name =}Targets
    NAMESPACE {= name =}::
    DESTINATION "${{= name =}_INSTALL_CMAKEDIR}"
    COMPONENT {= name =}_Development
){% end %}

if(PROJECT_IS_TOP_LEVEL)
  include(CPack)
endif()
