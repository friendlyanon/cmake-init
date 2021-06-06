# This function builds a PATH=paths string that can be used to set the
# ENVIRONMENT property on tests. This is useful to forward PATH for test 
# discovery functions like gtest_discover_tests from the GoogleTest module.
# You may use it like so:
#
#     windows_set_path_build_path(path dependency::shared)
#     gtest_discover_tests(test_exe PROPERTIES ENVIRONMENT "${path}")
#
# Note that this function does some escaping of semicolons, to properly pass
# the ENVIRONMENT property to the script that executes the tests. This is
# controlled by the ESCAPE_COUNT argument, which is by default set to 7. You
# might have to change this depending on how the value is passed around, but
# the default value works if used like in the above example snippet.
function(windows_set_path_build_path OUT_VAR)
  cmake_parse_arguments(PARSE_ARGV 1 "" "" ESCAPE_COUNT "")
  set(escape_count 7)
  if(DEFINED _ESCAPE_COUNT)
    set(escape_count "${_ESCAPE_COUNT}")
  endif()

  set(backslashes "")
  foreach(unused RANGE 1 "${escape_count}")
    string(APPEND backslashes "\\")
  endforeach()

  set(path "")
  if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    set(glue "")
    foreach(target IN LISTS _UNPARSED_ARGUMENTS)
      get_target_property(type "${target}" TYPE)
      if(type STREQUAL "SHARED_LIBRARY")
        set(path "${path}${glue}$<TARGET_FILE_DIR:${target}>")
        set(glue "${backslashes};")
      endif()
    endforeach()
  endif()

  if(NOT path STREQUAL "")
    string(PREPEND path "PATH=")
  endif()
  set("${OUT_VAR}" "${path}" PARENT_SCOPE)
endfunction()

# This function will add shared libraries to the PATH when running the test, so
# they can be found. Windows does not support RPATH or similar. See:
# https://docs.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order
# Usage: windows_set_path(<test> <target>...)
function(windows_set_path TEST)
  windows_set_path_build_path(PATH ESCAPE_COUNT 1 ${ARGN})
  if(NOT PATH STREQUAL "")
    set_property(TEST "${TEST}" PROPERTY ENVIRONMENT "${PATH}")
  endif()
endfunction()
