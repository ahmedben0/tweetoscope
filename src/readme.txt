TO COMPILE THE .cpp FILES:
	you should be in the cpp directory and then run : (for example)
	
cpp$	g++ -o tweet-generator -O3 -Wall -std=c++17 `pkg-config --libs --cflags gaml cppkafka rdkafka` -lpthread tweet-generator.cpp


THE FILES NEEDED AS CONFIG FILES ARE IN THE DIRECTORY configs
