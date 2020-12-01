## it is recommended to use cmake ! ## 

* TO COMPILE THE .cpp FILES:
  * You should be in the src directory and then run :

```
(src)$	g++ -o cpp/tweet-generator.o -O3 -Wall -std=c++17 `pkg-config --libs --cflags gaml spdlog cppkafka rdkafka` -lpthread cpp/tweet-generator.cpp
(src)$	g++ -o cpp/tweet-collector.o -O3 -Wall -std=c++17 `pkg-config --libs --cflags gaml spdlog cppkafka rdkafka` -lpthread cpp/tweet-collector.cpp
```

THE FILES NEEDED AS CONFIG FILES FOR THE EXECUTABLES ARE IN THE DIRECTORY : configs

* TO RUN THE EXECUTABLES: 
  * from the directory src :
```
(src)$ ./cpp/tweet-generator.o ./configs/params.config
(src)$ ./cpp/tweet-collector.o ./configs/collector.ini
```