## This function estimates the parameters (p, beta) of the generating process for the cascade.
## We use the MAP estimator.

from utils import *
from json import dumps
import configparser

## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')

#%%
## Create consumer
consumerProperties = { "bootstrap_servers":[config["kafka"]["brokers"]],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}

consumer = KafkaConsumer(**consumerProperties)
consumer.subscribe(config["topic"]["out_series"])


## Create producer
producerProperties = {"bootstrap_servers":[config["kafka"]["brokers"]]}

producer = KafkaProducer(**producerProperties)


## Read cascades from cascade_series
for message in consumer:
    # message = key, value
    key, value = msg_deserializer(message)

    cascade = np.array(value['tweets'])
    estimated_params = compute_MAP(cascade)[1]

    #produce message to cascade properties
    n_supp = estimated_size(estimated_params, cascade)
    valeurs =  {'type': 'parameters', 'cid': value['cid'], 'msg' : value['msg'], 'n_obs': len(cascade), 'n_supp' : n_supp, 'params': estimated_params.tolist()}
    producer.send(config["topic"]["out_properties"], value=msg_serializer(valeurs), key=msg_serializer(value['T_obs']))
    print(valeurs)
