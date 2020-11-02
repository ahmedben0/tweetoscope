## python version of the cascade consumer

import json
from json import loads
from kafka import KafkaConsumer
import ast


def msg_deserializer(message) :
    ## this function a custom to deserialize
    ## the kafka message comming from the cascade topic

    # message is of type ConsumerRecord
    # => message.value is of type bytes
    # we then decide to use the library
    # ast to convert to a dictionnary
    return ast.literal_eval(message.value.decode("UTF-8"))



consumerProperties = { "bootstrap_servers":['localhost:9092'],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}

consumer = KafkaConsumer(**consumerProperties)
consumer.subscribe("cascades")



for message in consumer:
    msg_d = msg_deserializer(message)
    print(msg_d)
    break
