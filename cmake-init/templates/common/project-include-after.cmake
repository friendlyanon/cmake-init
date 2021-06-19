# This file is run at the end of every project() call

# Top level setup to set folder property for targets to be grouped in IDEs that
# support folders
if(PROJECT_NAME STREQUAL "%(name)s")
  set(FOLDER_%(name)s Project)
  set(FOLDER_%(name)sTests Test){if examples}
  set(FOLDER_%(name)sExamples Example){end}

  function(project_set_folder_property)
    set(var "FOLDER_${PROJECT_NAME}")
    if(NOT DEFINED "${var}")
      message(FATAL_ERROR "Variable '${var}' does not exist")
    endif()
    get_property(targets DIRECTORY PROPERTY BUILDSYSTEM_TARGETS)
    foreach(target IN LISTS targets)
      get_property(folder TARGET "${target}" PROPERTY FOLDER)
      if(DEFINED folder)
        continue()
      endif()
      set(folder UtilityTargets)
      get_property(type TARGET "${target}" PROPERTY TYPE)
      if(NOT type STREQUAL "UTILITY")
        set(folder "${${var}}Targets")
      endif()
      set_property(TARGET "${target}" PROPERTY FOLDER "${folder}")
    endforeach()
  endfunction()

  set_property(GLOBAL PROPERTY USE_FOLDERS YES)
endif()

cmake_language(DEFER CALL project_set_folder_property)
