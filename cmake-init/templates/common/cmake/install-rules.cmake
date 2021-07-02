if(PROJECT_IS_TOP_LEVEL)
  set(CMAKE_INSTALL_INCLUDEDIR include/%(name)s CACHE PATH "")
endif(){type header}

# Project is configured with no languages, so tell GNUInstallDirs the lib dir
set(CMAKE_INSTALL_LIBDIR lib CACHE PATH ""){end}

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

# find_package(<package>) call for consumers to find this project
set(package %(name)s){type shared}

install(
    DIRECTORY
    include/
    "${PROJECT_BINARY_DIR}/export/"
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
    COMPONENT %(name)s_Development
){end}{type header}

install(
    DIRECTORY include/
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
    COMPONENT %(name)s_Development
){end}

install(
    TARGETS %(name)s_%(name)s
    EXPORT %(name)sTargets{type exe}
    RUNTIME COMPONENT %(name)s_Runtime{end}{type shared}
    RUNTIME #
    COMPONENT %(name)s_Runtime
    LIBRARY #
    COMPONENT %(name)s_Runtime
    NAMELINK_COMPONENT %(name)s_Development
    ARCHIVE #
    COMPONENT %(name)s_Development
    INCLUDES #
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"{end}{type header}
    INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"{end}
)

write_basic_package_version_file(
    "${package}ConfigVersion.cmake"
    COMPATIBILITY SameMajorVersion{type header}
    ARCH_INDEPENDENT{end}
)

# Allow package maintainers to freely override the path for the configs
set(
    %(name)s_INSTALL_CMAKEDIR "${CMAKE_INSTALL_DATADIR}/${package}"
    CACHE PATH "CMake package config location relative to the install prefix"
)
mark_as_advanced(%(name)s_INSTALL_CMAKEDIR)

install(
    FILES cmake/install-config.cmake
    DESTINATION "${%(name)s_INSTALL_CMAKEDIR}"
    RENAME "${package}Config.cmake"
    COMPONENT %(name)s_Development
)

install(
    FILES "${PROJECT_BINARY_DIR}/${package}ConfigVersion.cmake"
    DESTINATION "${%(name)s_INSTALL_CMAKEDIR}"
    COMPONENT %(name)s_Development
)

install(
    EXPORT %(name)sTargets
    NAMESPACE %(name)s::
    DESTINATION "${%(name)s_INSTALL_CMAKEDIR}"
    COMPONENT %(name)s_Development
)

if(PROJECT_IS_TOP_LEVEL)
  include(CPack)
endif()
