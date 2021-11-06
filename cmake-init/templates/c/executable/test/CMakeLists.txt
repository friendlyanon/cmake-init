# Parent project does not export its library target, so this CML implicitly
# depends on being added from it, i.e. the testing is done only from the build
# tree and is not feasible from an install location

project(%(name)sTests LANGUAGES C)

add_executable(%(name)s_test source/%(name)s_test.c)
target_link_libraries(%(name)s_test PRIVATE %(name)s_lib)
target_compile_features(%(name)s_test PRIVATE c_std_%(std)s)

add_test(NAME %(name)s_test COMMAND %(name)s_test)

add_folders(Test)
