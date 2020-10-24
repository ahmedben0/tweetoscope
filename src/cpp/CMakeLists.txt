file(GLOB 
  lib_sources
  tweet*.cpp)

file(GLOB 
  lib_headers
  tweet*.hpp)

add_library(tweetoscope
  SHARED
  ${lib_sources})


target_include_directories(tweetoscope PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_options    (tweetoscope PUBLIC -O3 -Wall -std=c++17 `pkg-config --libs --cflags gaml cppkafka rdkafka` -lpthread)
add_executable(tweet ${lib_sources})