## This function estimates the parameters (p, beta) 
## of the generating  process for the cascade.
## We use the MAP estimator.

from utils import *


## init logger
logger = logger.get_logger('Estimator', broker_list='localhost:9092', debug=True)

## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')


## Create consumer for cascade_series topic
consumerProperties = { "bootstrap_servers":[config["kafka"]["brokers"]],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}
consumer = KafkaConsumer(**consumerProperties)
consumer.subscribe(config["topic"]["out_series"])


## Create producer to send messages to cascade_properties 
## with the estimated params for the Hawkes process
producerProperties = {"bootstrap_servers":[config["kafka"]["brokers"]]}
producer = KafkaProducer(**producerProperties)


## Read cascades from cascade_series and estimate params 
## for the Hawkes process
for message in consumer:
   key, value = msg_deserializer(message)
   cascade = np.array(value['tweets'])
  
   #estimate parameters p, beta
   estimated_params = compute_MAP(cascade)[1].tolist()

   #compute G1
   G1 = compute_G1(estimated_params, cascade)
   estimated_params.append(G1)

   #produce message to cascade properties
   n_obs = len(cascade)
   n_supp = estimated_size(n_obs, estimated_params)
   valeurs =  {'type': 'parameters', 'cid': value['cid'], 'msg' : value['msg'], 'n_obs': n_obs, 'n_supp' : int(n_supp), 'params': estimated_params}
   producer.send(config["topic"]["out_properties"], value=msg_serializer(valeurs), key=msg_serializer(value['T_obs']))
   logger.info(valeurs)
