# Parent project does not export its library target, so this CML implicitly
# depends on being added from it, i.e. the testing is done only from the build
# tree and is not feasible from an install location

project({= name =}Tests LANGUAGES CXX)

add_executable({= name =}_test source/{= name =}_test.cpp)
target_link_libraries({= name =}_test PRIVATE {= name =}_lib)
target_compile_features({= name =}_test PRIVATE cxx_std_{= std =})

add_test(NAME {= name =}_test COMMAND {= name =}_test)

add_folders(Test)
