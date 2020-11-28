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


### Requirements

Most of the libraries used in the projects are in the file docker/requirements.txt. To install them you can lanch the following command L:
```
apt-get update && cat requirements.txt | xargs apt-get install -y
```

Other packages also should be installed, please refer to [Technologies](#technologies) : gaml, cppkafka, spdlog ..

### C++
It is possible to compile the cpp files using CMAKE :

```
$ mkdir build
$ cd build
$ cmake ..
$ make
```
We should also copy the csv data to the folder build/src
