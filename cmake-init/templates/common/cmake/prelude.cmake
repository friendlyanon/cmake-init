# ---- In-source guard ----

if(CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR)
  message(
      FATAL_ERROR
      "In-source builds are not supported. "
      "Make a new directory (e.g., 'build/'), and run CMake from there. "
      "You may need to delete 'CMakeCache.txt' and 'CMakeFiles/' first."
  )
endif()

# ---- Dummy function for docs generation ----

# This function is empty here, so it can be overridden in docs.cmake and in CI
# only the docs target is made available
macro(docs_early_return)
endmacro()
