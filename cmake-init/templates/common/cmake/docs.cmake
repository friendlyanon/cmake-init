# ---- CI specific checks ----

# All of this is done so project() variables are available in script mode, so
# documentation can be generated without having to configure the project, which
# could take more time than necessary, but the downside is that you may not use
# variables defined after the project() call in the root lists file
if(DEFINED CMAKE_SCRIPT_MODE_FILE)
  if(NOT DEFINED PROJECT_BINARY_DIR)
    set(PROJECT_BINARY_DIR "${CMAKE_SOURCE_DIR}/build")
  else()
    get_filename_component(PROJECT_BINARY_DIR "${PROJECT_BINARY_DIR}" ABSOLUTE)
  endif()
  set(PROJECT_SOURCE_DIR "${CMAKE_SOURCE_DIR}")

  macro(_project name)
    set(args VERSION DESCRIPTION LANGUAGES HOMEPAGE_URL)
    cmake_parse_arguments(PROJECT "" "${args}" "" ${ARGN})
    set(PROJECT_NAME "${name}" PARENT_SCOPE)
    foreach(var IN LISTS args)
      set("PROJECT_${var}" "${PROJECT_${var}}" PARENT_SCOPE)
    endforeach()
    return()
  endmacro()

  file(READ CMakeLists.txt lists_content)
  string(REPLACE "\nproject(" "\n_project(" lists_content "${lists_content}")
  file(WRITE "${PROJECT_BINARY_DIR}/docs/lists.txt" "${lists_content}")

  function(project_proxy)
    include("${PROJECT_BINARY_DIR}/docs/lists.txt")
  endfunction()
  project_proxy()
endif()

# ---- Dependencies ----

set(
    mcss_url
    https://github.com/friendlyanon/m.css/releases/download/release-1/mcss.zip
)
set(mcss_root "${PROJECT_BINARY_DIR}/mcss")
if(NOT EXISTS "${mcss_root}")
  file(MAKE_DIRECTORY "${mcss_root}")
  message(STATUS "Downloading m.css")
  file(
      DOWNLOAD "${mcss_url}" "${mcss_root}/mcss.zip"
      EXPECTED_HASH MD5=00cd2757ebafb9bcba7f5d399b3bec7f
      STATUS status
  )
  if(NOT status MATCHES "^0;")
    message(FATAL_ERROR "file(DOWNLOAD) returned with ${status}")
  endif()
  execute_process(
      COMMAND "${CMAKE_COMMAND}" -E tar xf "${mcss_root}/mcss.zip"
      WORKING_DIRECTORY "${mcss_root}"
      RESULT_VARIABLE result
  )
  if(NOT result EQUAL "0")
    message(FATAL_ERROR "Trying to extract m.css returned with ${result}")
  endif()
  file(REMOVE "${mcss_root}/mcss.zip")
endif()

find_package(Python3 3.6 REQUIRED)

# ---- Declare documentation target ----

set(
    DOXYGEN_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/docs"
    CACHE PATH "Path for the generated Doxygen documentation"
)

set(working_dir "${PROJECT_BINARY_DIR}/docs")

foreach(file IN ITEMS Doxyfile conf.py)
  configure_file("docs/${file}.in" "${working_dir}/${file}" @ONLY)
endforeach()

set(mcss_script "${mcss_root}/documentation/doxygen.py")
set(config "${working_dir}/conf.py")

if(DEFINED CMAKE_SCRIPT_MODE_FILE)
  execute_process(
      COMMAND "${Python3_EXECUTABLE}" "${mcss_script}" "${config}"
      WORKING_DIRECTORY "${working_dir}"
      RESULT_VARIABLE result
  )
  if(NOT result EQUAL "0")
    message(FATAL_ERROR "m.css returned with ${result}")
  endif()
else()
  add_custom_target(
      docs
      COMMAND "${Python3_EXECUTABLE}" "${mcss_script}" "${config}"
      COMMENT "Building documentation using Doxygen and m.css"
      WORKING_DIRECTORY "${working_dir}"
      VERBATIM
  )
endif()
