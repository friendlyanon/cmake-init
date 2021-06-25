if(
    NOT DEFINED CMAKE_SCRIPT_MODE_FILE
    AND CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR
)
  message(
      FATAL_ERROR
      "In-source builds are not supported. "
      "Make a new directory (e.g., 'build/'), and run CMake from there. "
      "You may need to delete 'CMakeCache.txt' and 'CMakeFiles/' first."
  )
endif()
