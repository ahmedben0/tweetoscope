TO COMPILE THE .cpp FILES:
	you should be in the cpp directory and then run : (for example)
	
cpp$	g++ -o tweet-generator -O3 -Wall -std=c++17 `pkg-config --libs --cflags gaml cppkafka rdkafka` -lpthread tweet-generator.cpp


THE FILES NEEDED AS CONFIG FILES FOR THE EXECUTABLES ARE IN THE DIRECTORY : configs

TO RUN THE EXECUTABLES :
src$    ./cpp/tweet-generator ./configs/params.config
