## CMakeLists should be edited, not working rn !

cmake_minimum_required( VERSION 2.8 )
project (tweetoscope)
add_subdirectory(src/cpp)

find_package(PkgConfig)
#pkg_check_modules(PTHREAD   REQUIRED pthread)
pkg_check_modules(GMAL      REQUIRED gaml)
pkg_check_modules(CPPKAFKA  REQUIRED cppkafka)
pkg_check_modules(RDKAFKA   REQUIRED rdkafka)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_BUILD_TYPE Release)
