add_library(ccc-lib CallChainChecker.cpp)
target_include_directories(ccc-lib SYSTEM PUBLIC Boost::headers ${CLANG_INCLUDE_DIRS} ${LLVM_INCLUDE_DIRS})
target_include_directories(ccc-lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

if(CLANG_LINK_CLANG_DYLIB)
    target_link_libraries(ccc-lib PUBLIC LLVM)
    clang_target_link_libraries(ccc-lib PUBLIC)
else()
    llvm_map_components_to_libnames(llvm_libs support core)
    target_link_libraries(ccc-lib PUBLIC ${llvm_libs}
                                         clangASTMatchers
                                         clangTransformer
                                         clangTooling)
endif(CLANG_LINK_CLANG_DYLIB)


add_executable(ccc CallChainCheckerTool.cpp)
target_link_libraries(ccc PUBLIC ccc-lib)
install(TARGETS ccc DESTINATION bin)
