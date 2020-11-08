file(GLOB 
  lib_sources
  tweet-col*.cpp)


add_executable(tweet ${lib_sources} ${CMAKE_BINARY_DIR})