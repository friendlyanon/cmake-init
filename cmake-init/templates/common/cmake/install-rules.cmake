if(PROJECT_IS_TOP_LEVEL)
  set(CMAKE_INSTALL_INCLUDEDIR include/%(name)s CACHE PATH "")
endif()

include(CMakePackageConfigHelpers)
include(GNUInstallDirs){type shared}

# Allow vcpkg portfiles to not bother with headers in debug folder
option(%(name)s_INSTALL_HEADERS "Install headers" ON)
mark_as_advanced(%(name)s_INSTALL_HEADERS)

if(%(name)s_INSTALL_HEADERS)
  install(
      DIRECTORY
      "${PROJECT_SOURCE_DIR}/include/"
      "${PROJECT_BINARY_DIR}/include/"
      DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
      COMPONENT %(name)s_Development
  )
endif(){end}{type header}

install(
    DIRECTORY "${PROJECT_SOURCE_DIR}/include/"
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
    %(name)sConfigVersion.cmake
    COMPATIBILITY SameMajorVersion{type header}
    ARCH_INDEPENDENT{end}
)

# Allow package maintainers to freely override the path for the configs
set(
    %(name)s_INSTALL_CMAKEDIR "${CMAKE_INSTALL_LIBDIR}/cmake/%(name)s"
    CACHE STRING "CMake package config location relative to the install prefix"
)
mark_as_advanced(%(name)s_INSTALL_CMAKEDIR)

install(
    FILES
    "${PROJECT_SOURCE_DIR}/cmake/%(name)sConfig.cmake"
    "${PROJECT_BINARY_DIR}/%(name)sConfigVersion.cmake"
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
