# ---- Dependencies ----

find_package(Python3 3.6 REQUIRED)

include(FetchContent)
FetchContent_Declare(
    m.css
    GIT_REPOSITORY "https://github.com/mosra/m.css.git"
    GIT_TAG 9385194fa3392a7162e7535cc2478814e382ff8a
    UPDATE_DISCONNECTED YES
)
FetchContent_MakeAvailable(m.css)

# ---- Declare documentation target ----

set(
    DOXYGEN_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/docs"
    CACHE PATH "Path for the generated Doxygen documentation"
)

set(working_dir "${PROJECT_BINARY_DIR}/docs")

foreach(file IN ITEMS Doxyfile conf.py)
  configure_file("docs/${file}.in" "${working_dir}/${file}" @ONLY)
endforeach()

set(mcss_script "${m.css_SOURCE_DIR}/documentation/doxygen.py")
set(config "${working_dir}/conf.py")

add_custom_target(
    docs
    COMMAND "${Python3_EXECUTABLE}" "${mcss_script}" "${config}"
    COMMENT "Building documentation using Doxygen and m.css"
    WORKING_DIRECTORY "${working_dir}"
    VERBATIM
)
