# Tweetoscope :bird: #

## :rotating_light: VERY IMPORTANT ! :rotating_light: ##

Only the links to download the data are given in the readme of the data folder. This decision was taken to avoid uploding data and csv files in general to GitLab.
Further instructions are given below.


## :book: General info ##
This project is the work of Group 7 ( FELLAJI Mohammed, BEN AISSA Ahmed, MOKBEL Elie).

The presentation of the project could be found in the official website :link: : [Tweetoscope](http://sdi.metz.centralesupelec.fr/spip.php?article25)


## :dart: How to run the project ? ##

### :computer: On your machine ###
* Download the data and put it in the data folder : refer to this [readme](./data/readme.txt),
* Run the kafka server :
1.  To use the .sh file to lanch kafka, you should export the path to kafka. As mentionned in the description of the project, [kafka 2.4.1](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.4.1/kafka-2.4.1-src.tgz) is used
```
    $ export KAFKA_PATH=/path/to/kafka
```
2. To run the kafka server from the kafka folder (or just specify the path to the files) in this project (the 3 files are in the same folder): 
```
    $ ./kafka.sh start --zooconfig zookeeper.properties --serverconfig server.properties
```
* Build the C++ project from the root :
```
    $ mkdir build
    $ cd build
    $ cmake ..
    $ make
```
* Run the generator and the collector from ./build/src using the files for the configuration : [params-build.config](./src/configs/params-build.config) and [collector-build.ini](./src/configs/collector-build.ini)
```
(src)$ ./cpp/tweet-generator.o ./configs/params-build.config
(src)$ ./cpp/tweet-collector.o ./configs/collector-build.ini 
```
* As for the C++ files, the python files are also run from ./build/src

###  :cloud: Minikube  ### 

* Start minikube : 
```
    $ minikube start
```

* We recommand to start by deleting the deployemnt pods in case they already exist by running from the root:
```
    $ kubectl delete -f K8s/deployment.yml
    $ kubectl delete -f K8s/zookeeper-and-kafka.yml
```

* For the deployment, you have to run the following lines from the root as well :
```
    $ kubectl apply -f K8s/zookeeper-and-kafka.yml
    $ kubectl apply -f K8s/deployment.yml
```
* Remarks: it is also possible to only run the python script [deployment.py](./deployment.py) for the deployment.


## :wrench: Setup ##
This project is created using :
* [gaml](https://github.com/HerveFrezza-Buet/gaml)
* [cppkafka](https://github.com/mfontanini/cppkafka)
* [kafka](https://kafka.apache.org/)
* [spdlog](https://github.com/gabime/spdlog/tree/master)
* [docker](https://www.docker.com/)
* [kubernetes](https://kubernetes.io/)
* and more ...

Check the docker file for more info about the different libraries.


To run this project, one should follow these steps


## :package: Requirements ##

Most of the libraries used in the project are in the file [./docker/requirements_apt](./docker/requirements_apt.txt). To install them you can lanch the following command :
```
$ apt-get update && cat requirements_apt.txt | xargs apt-get install -y
```

Other packages also should be installed, please refer to the previous section (Setup)

A requirement file for python is also available in [./docker/requirements_python.txt](./docker/requirements_python.txt)
```
$ pip install -r requirements_python.txt
```