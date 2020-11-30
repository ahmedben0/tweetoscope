## python version of the cascade consumer
import json
from json import loads
from kafka import KafkaConsumer
from utils import *
import configparser

## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')


consumerProperties = { "bootstrap_servers":[config["kafka"]["brokers"]],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}

consumer = KafkaConsumer(**consumerProperties)
consumer.subscribe(config["topic"]["out_series"])


for message in consumer:
    key, value = msg_deserializer(message)
    print(key, value)
    print()
