TO COMPILE THE .cpp FILES:
	you should be in the src directory and then run : (for example)
	
src$	g++ -o cpp/tweet-generator -O3 -Wall -std=c++17 `pkg-config --libs --cflags gaml cppkafka rdkafka` -lpthread cpp/tweet-generator.cpp


THE FILES NEEDED AS CONFIG FILES FOR THE EXECUTABLES ARE IN THE DIRECTORY : configs

TO RUN THE EXECUTABLES - from the directory src :
src$    ./cpp/tweet-generator ./configs/params.config
