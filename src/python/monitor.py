from kafka import KafkaConsumer
from utils import *
import configparser
import sys
import time 

## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')


consumerProperties = { "bootstrap_servers":[config["kafka"]["brokers"]],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}


consumer = KafkaConsumer(**consumerProperties)
consumer.subscribe("stats")

GLOBAL_MIN  = 10000
GLOBAL_MAX  = -10000
GLOBAL_MEAN = 0
counter     = 0
for message in consumer:
     key, value = msg_deserializer(message)
     counter += 1
     _are = value["ARE"]
     GLOBAL_MIN  = min(_are, GLOBAL_MIN)
     GLOBAL_MAX  = max(_are, GLOBAL_MAX) 
     GLOBAL_MEAN = ((counter-1)*GLOBAL_MEAN + _are)/(counter)

     if counter%10 == 0 :
         print("MEAN :", int(GLOBAL_MEAN), " - MAX :", int(GLOBAL_MAX), " - MIN :", int(GLOBAL_MIN))


