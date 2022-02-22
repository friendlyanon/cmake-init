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
set(
    {= uc_name =}_EXECUTABLE
    \"\${CMAKE_CURRENT_LIST_DIR}/${relative_path}\"
    CACHE FILEPATH \"Path to the {= name =} executable\"
)
")
