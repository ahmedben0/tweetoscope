# Tweetoscope :bird:

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info :book:
This project was developed by Mohammed Fellaji, Elie Mokbel and Ahmed Ben Aissa from Ecole CentraleSupélec. 

Information about the project could be found in the official website :link: : [Tweetoscope](http://sdi.metz.centralesupelec.fr/spip.php?article25)

## Technologies :computer:
This project is created using :
* [gaml](https://github.com/HerveFrezza-Buet/gaml)
* [cppkafka](https://github.com/mfontanini/cppkafka)
* [kafka](https://kafka.apache.org/)
* [spdlog](https://github.com/gabime/spdlog/tree/master)
* [docker](https://www.docker.com/)
* [kubernetes](https://kubernetes.io/)
* and more ...

Check the docker file for more info about the different libraries.

### Remark
if the dockerfiles are changed, one should change the variable name : Docker_image_name !


## Setup :wrench:
To run this project, one should follow these steps

### - Data 
The csv files could be found in : [neww-data.csv](https://pennerath.pages.centralesupelec.fr/tweetoscope/data/news-data.csv) and [news-index.csv](https://pennerath.pages.centralesupelec.fr/tweetoscope/data/news-index.csv) 

Please put the csv files in the folder data/

### - Requirements

Most of the libraries used in the projects are in the file docker/requirements_apt.txt. To install them you can lanch the following command :
```
$ apt-get update && cat requirements_apt.txt | xargs apt-get install -y
```

Other packages also should be installed, please refer to [Technologies](#technologies) : gaml, cppkafka, spdlog ..

### - Kafka 
To use the .sh file to lanch kafka, you should export the path to kafka. As mentionned in the description of the project, [kafka 2.4.1](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.4.1/kafka-2.4.1-src.tgz) is used
```
$ export KAFKA_PATH=/path/to/kafka
```

To run the kafka server from the kafka folder in this project (the 3 files are in the same folder): 
```
$ ./kafka.sh start --zooconfig zookeeper.properties --serverconfig server.properties
```
If you have a problem starting the server, it is possible that you should run this from KAFKA_PATH (in our case, the message in the terminal suggested to run this)
```
$ ./gradlew jar -PscalaVersion=2.12.10
```

To stop the server : 
```
$ ./kafka stop
```

### - C++
It is possible to compile the cpp files using CMAKE :

```
$ mkdir build
$ cd build
$ cmake ..
$ make
```
We should also copy the csv data to the folder build/
