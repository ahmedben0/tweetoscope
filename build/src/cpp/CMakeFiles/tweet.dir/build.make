# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.18.4/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.18.4/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/retina/Documents/3_année/cours/tweetoscope

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/retina/Documents/3_année/cours/tweetoscope/build

# Include any dependencies generated for this target.
include src/cpp/CMakeFiles/tweet.dir/depend.make

# Include the progress variables for this target.
include src/cpp/CMakeFiles/tweet.dir/progress.make

# Include the compile flags for this target's objects.
include src/cpp/CMakeFiles/tweet.dir/flags.make

src/cpp/CMakeFiles/tweet.dir/tweet-collector.cpp.o: src/cpp/CMakeFiles/tweet.dir/flags.make
src/cpp/CMakeFiles/tweet.dir/tweet-collector.cpp.o: ../src/cpp/tweet-collector.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/retina/Documents/3_année/cours/tweetoscope/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/cpp/CMakeFiles/tweet.dir/tweet-collector.cpp.o"
	cd /Users/retina/Documents/3_année/cours/tweetoscope/build/src/cpp && /usr/local/bin/g++-10 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/tweet.dir/tweet-collector.cpp.o -c /Users/retina/Documents/3_année/cours/tweetoscope/src/cpp/tweet-collector.cpp

src/cpp/CMakeFiles/tweet.dir/tweet-collector.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tweet.dir/tweet-collector.cpp.i"
	cd /Users/retina/Documents/3_année/cours/tweetoscope/build/src/cpp && /usr/local/bin/g++-10 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/retina/Documents/3_année/cours/tweetoscope/src/cpp/tweet-collector.cpp > CMakeFiles/tweet.dir/tweet-collector.cpp.i

src/cpp/CMakeFiles/tweet.dir/tweet-collector.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tweet.dir/tweet-collector.cpp.s"
	cd /Users/retina/Documents/3_année/cours/tweetoscope/build/src/cpp && /usr/local/bin/g++-10 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/retina/Documents/3_année/cours/tweetoscope/src/cpp/tweet-collector.cpp -o CMakeFiles/tweet.dir/tweet-collector.cpp.s

# Object files for target tweet
tweet_OBJECTS = \
"CMakeFiles/tweet.dir/tweet-collector.cpp.o"

# External object files for target tweet
tweet_EXTERNAL_OBJECTS =

src/cpp/tweet: src/cpp/CMakeFiles/tweet.dir/tweet-collector.cpp.o
src/cpp/tweet: src/cpp/CMakeFiles/tweet.dir/build.make
src/cpp/tweet: src/cpp/CMakeFiles/tweet.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/retina/Documents/3_année/cours/tweetoscope/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable tweet"
	cd /Users/retina/Documents/3_année/cours/tweetoscope/build/src/cpp && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tweet.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/cpp/CMakeFiles/tweet.dir/build: src/cpp/tweet

.PHONY : src/cpp/CMakeFiles/tweet.dir/build

src/cpp/CMakeFiles/tweet.dir/clean:
	cd /Users/retina/Documents/3_année/cours/tweetoscope/build/src/cpp && $(CMAKE_COMMAND) -P CMakeFiles/tweet.dir/cmake_clean.cmake
.PHONY : src/cpp/CMakeFiles/tweet.dir/clean

src/cpp/CMakeFiles/tweet.dir/depend:
	cd /Users/retina/Documents/3_année/cours/tweetoscope/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/retina/Documents/3_année/cours/tweetoscope /Users/retina/Documents/3_année/cours/tweetoscope/src/cpp /Users/retina/Documents/3_année/cours/tweetoscope/build /Users/retina/Documents/3_année/cours/tweetoscope/build/src/cpp /Users/retina/Documents/3_année/cours/tweetoscope/build/src/cpp/CMakeFiles/tweet.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/cpp/CMakeFiles/tweet.dir/depend

