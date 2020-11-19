## python version of the cascade consumer

import json
from json import loads
from kafka import KafkaConsumer
from utils import *


consumerProperties = { "bootstrap_servers":['localhost:9092'],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}

consumer = KafkaConsumer(**consumerProperties)
consumer.subscribe("cascade_properties")


for message in consumer:
    key, value = msg_deserializer(message)
    print(key, value)
    print()
