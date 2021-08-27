# ---- Redefine docs_early_return ----

# This function must be a macro, so the return() takes effect in the calling
# scope. This prevents other targets from being available and potentially
# requiring dependencies. This cuts down on the time it takes to generate
# documentation in CI.
macro(docs_early_return)
  return()
endmacro()

# ---- Dependencies ----

set(mcss_SOURCE_DIR "${PROJECT_BINARY_DIR}/mcss")
include(FetchContent)
FetchContent_Declare(
    mcss URL
    https://github.com/friendlyanon/m.css/releases/download/release-1/mcss.zip
    URL_MD5 00cd2757ebafb9bcba7f5d399b3bec7f
    SOURCE_DIR "${mcss_SOURCE_DIR}"
)
if(NOT IS_DIRECTORY "${mcss_SOURCE_DIR}")
  message(STATUS "Downloading m.css")
  FetchContent_Populate(mcss)
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

set(mcss_script "${mcss_SOURCE_DIR}/documentation/doxygen.py")
set(config "${working_dir}/conf.py")

add_custom_target(
    docs
    COMMAND "${Python3_EXECUTABLE}" "${mcss_script}" "${config}"
    COMMENT "Building documentation using Doxygen and m.css"
    WORKING_DIRECTORY "${working_dir}"
    VERBATIM
)
