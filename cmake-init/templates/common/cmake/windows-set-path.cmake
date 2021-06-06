# This function will add shared libraries to the PATH when running the test, so
# they can be found. Windows does not support RPATH or similar. See:
# https://docs.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order
# Usage: windows_set_path(<test> <target>...)
function(windows_set_path TEST)
  if(NOT CMAKE_HOST_SYSTEM_NAME STREQUAL "Windows")
    return()
  endif()

  set(path "")
  set(glue "")
  foreach(target IN LISTS ARGN)
    get_target_property(type "${target}" TYPE)
    if(type STREQUAL "SHARED_LIBRARY")
      set(path "${path}${glue}$<TARGET_FILE_DIR:${target}>")
      set(glue "\;") # backslash is important
    endif()
  endforeach()
  if(NOT path STREQUAL "")
    set_property(TEST "${TEST}" PROPERTY ENVIRONMENT "PATH=${path}")
  endif()
endfunction()

# Same function as above, except this makes it cleaner to work with lists of
# tests created by test discovery functions like gtest_discover_tests(example)
# creating the example_TESTS list
function(windows_set_path_for_list TESTS)
  foreach(TEST IN LISTS TESTS)
    windows_set_path("${TEST}" ${ARGN})
  endforeach()
endfunction()
