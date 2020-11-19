# we want to generate to binary files : one for the generator and the other one for the collector

add_executable(tweet-collector.o tweet-collector.cpp ${CMAKE_BINARY_DIR})
add_executable(tweet-generator.o tweet-generator.cpp ${CMAKE_BINARY_DIR})
