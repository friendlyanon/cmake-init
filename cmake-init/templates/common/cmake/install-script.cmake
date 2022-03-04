file(
    RELATIVE_PATH relative_path
    "/${{= name =}_INSTALL_CMAKEDIR}"
    "/${CMAKE_INSTALL_BINDIR}/${{= name =}_NAME}"
)

get_filename_component(prefix "${CMAKE_INSTALL_PREFIX}" ABSOLUTE)
set(config_dir "${prefix}/${{= name =}_INSTALL_CMAKEDIR}")
set(config_file "${config_dir}/{= name =}Config.cmake")

message(STATUS "Installing: ${config_file}")
file(WRITE "${config_file}" "\
get_filename_component(
    _{= name =}_executable
    \"\${CMAKE_CURRENT_LIST_DIR}/${relative_path}\"
    ABSOLUTE
)
set(
    {= uc_name =}_EXECUTABLE \"\${_{= name =}_executable}\"
    CACHE FILEPATH \"Path to the {= name =} executable\"
)
")
