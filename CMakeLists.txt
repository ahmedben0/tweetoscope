cmake_minimum_required( VERSION 2.8 )
project (tweetoscope)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(PkgConfig)
pkg_check_modules(GAML      REQUIRED gaml)
pkg_check_modules(CPPKAFKA  REQUIRED cppkafka)
pkg_check_modules(RDKAFKA   REQUIRED rdkafka)

find_package(spdlog )
pkg_check_modules(SPDLOG spdlog)
pkg_search_module(SPDLOG spdlog)

link_libraries(${CPPKAFKA_LIBRARIES} pthread)
link_libraries(${RDKAFKA_LIBRARIES} pthread)
link_libraries(${GAML_LIBRARIES} pthread)
link_libraries(${SPDLOG_LIBRARIES} pthread)


find_package(Boost COMPONENTS filesystem REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${CPPKAFKA_INCLUDE_DIRS} ${GAML_INCLUDE_DIRS} ${RDKAFKA_STATIC_INCLUDE_DIRS})

add_compile_options(-O3 -Wall)

add_subdirectory(src/cpp)

file(COPY src/configs DESTINATION ${CMAKE_BINARY_DIR}/src)
file(COPY src/python DESTINATION ${CMAKE_BINARY_DIR}/src)
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/src/logs)
