## python version of the cascade consumer

import json
from json import loads
from kafka import KafkaConsumer
import ast


def msg_deserializer(message) :
    ## this function a custom to deserialize
    ## the kafka message comming from the cascade topic
    ## message = key, value

    # message is of type ConsumerRecord
    # => message.key & message.value is of type bytes
    # we then decide to use the library -- ast to convert to a dictionnary

    key   = ast.literal_eval(message.key.decode("UTF-8"))
    value = ast.literal_eval(message.value.decode("UTF-8"))
    return (key, value)


consumerProperties = { "bootstrap_servers":['localhost:9092'],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}

consumer = KafkaConsumer(**consumerProperties)
consumer.subscribe("cascade_series")


for message in consumer:
    # message = key, value
    ## value.keys() = dict_keys(['key', 'source_id', 'msg', 'latest_time', 'list_retweets'])
    ## value['list_retweets'] is a list of dictionnaries => dict_keys(['time', 'magnitude', 'info'])
    key, value = msg_deserializer(message)
    print(key, value)
    #break
