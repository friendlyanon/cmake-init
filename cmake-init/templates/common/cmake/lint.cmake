cmake_minimum_required(VERSION 3.14)

macro(default name)
  if(NOT DEFINED "${name}")
    set("${name}" "${ARGN}")
  endif()
endmacro()

default(FORMAT_COMMAND clang-format)
default(PATTERNS source/*.cpp source/*.h include/*.h)
default(FIX NO)

set(flag --output-replacements-xml)
set(args OUTPUT_VARIABLE output)
if(FIX)
  set(flag -i)
  set(args "")
endif()

file(GLOB_RECURSE files RELATIVE "${CMAKE_SOURCE_DIR}" ${PATTERNS})
set(badly_formatted "")
set(output "")

foreach(file IN LISTS files)
  execute_process(
      COMMAND "${FORMAT_COMMAND}" --style=file "${flag}" "${file}"
      WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
      RESULT_VARIABLE result
      ${args}
  )
  if(NOT result EQUAL "0")
    message(FATAL_ERROR "'${file}': formatter returned with ${result}")
  endif()
  if(NOT FIX AND output MATCHES "\n<replacement offset")
    list(APPEND badly_formatted "${file}")
  endif()
  set(output "")
endforeach()

if(NOT badly_formatted STREQUAL "")
  list(JOIN badly_formatted "\n" bad_list)
  message(NOTICE "The following files are badly formatted:\n\n${bad_list}\n")
  message(FATAL_ERROR "Run again with FIX=YES to fix these files.")
endif()
