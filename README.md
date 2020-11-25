# Tweetoscope :bird:

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info :book:
Information about the project could be found in the official website :link: : [Tweetoscope](http://sdi.metz.centralesupelec.fr/spip.php?article25)

## Technologies :computer:
This project is created using :
* [gaml](https://github.com/HerveFrezza-Buet/gaml)
* [cppkafka](https://github.com/mfontanini/cppkafka)
* [kafka](https://kafka.apache.org/)
* [spdlog](https://github.com/gabime/spdlog/tree/master)
* and more ...

Check the docker file for more info about the different libraries.

### Remark
if the dockerfiles are changed, one should change the variable name : Docker_image_name !

## Setup :wrench:
To run this project, one should follow these steps :

### C++
It is possible to compile the cpp files using CMAKE :

```
$ mkdir build
$ cd build
$ cmake ..
$ make
```
We should also copy the csv data to the folder build/src
