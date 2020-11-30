## This is the predictor part. We use a random forest model

from utils import *
import configparser


## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')


## Create consumers
consumerProperties = { "bootstrap_servers":[config["kafka"]["brokers"]],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}


consumer_cascadeProperties = KafkaConsumer(**consumerProperties)
consumer_cascadeProperties.subscribe("cascade_properties")


consumerProperties = { "bootstrap_servers":[config["kafka"]["brokers"]],
                       "auto_offset_reset":"latest",
                       "group_id":"myOwnPrivatePythonGroup"}
consumer_models = KafkaConsumer(**consumerProperties)
consumer_models.subscribe("models")


## Create producers
producerProperties = {"bootstrap_servers":[config["kafka"]["brokers"]]}

producer_sample = KafkaProducer(**producerProperties)
producer_alert  = KafkaProducer(**producerProperties)
producer_stat   = KafkaProducer(**producerProperties)


#here, we create a dictionanry with the cascade id and observation time as key, and the parameters we need as values (params, n_true, n_obs)
#In fact, we have two types of messages in cascade_properties : size, parameters. We collect the values that interest us in both
cascades = {}

for message in consumer_cascadeProperties:
    key, value = msg_deserializer(message)
    dict_key = (value['cid'], key) #we identify each cascade by its id and the key(observation window)
    if dict_key not in cascades.keys():
        cascades[dict_key] = {}
    if value['type'] == 'size':
        cascades[dict_key]['n_true'] =  value['n_tot']
    if value['type'] == 'parameters':
        cascades[dict_key]['n_obs'] = value['n_obs']
        cascades[dict_key]['params'] = value['params'] #p, beta, G1
        cascades[dict_key]['msg'] = value['msg']


    wanted_keys = ['n_true', 'n_obs', 'params', 'msg']
    if all(elem in cascades[dict_key].keys()  for elem in wanted_keys):
        key, value = dict_key, cascades[dict_key]

        cid = key[0] #cascade id
        T_obs = key[1] #observation window size

        model = None

        X = value['params'] #p, beta, G1
        n_true = value['n_true']
        n_obs = value['n_obs']

        W = compute_true_omega(n_obs, n_true, X) #the W we want to predict

        #we compute here the message of type "sample", i.e a sample to feed the random forest
        #inputs: params, target: omega
        valeurs_sample =  {'type': 'sample', 'cid': cid, 'X' : X, 'W': W}
        producer_sample.send("samples", value=msg_serializer(valeurs_sample), key=msg_serializer(T_obs))
        print(valeurs_sample)

        #We compute the ARE (messages of type stat)
        if model is None:
            w_obs =1
        else: 
            w_obs = model.predict(X) #predict the w_obs for the obs window
        n_pred = estimated_size(n_obs, X, w_obs=w_obs)
        are = compute_are(n_pred, n_true)
        valeurs_stat =  {'type': 'stat', 'cid': cid, 'T_obs' : T_obs, 'ARE': are}
        producer_stat.send("stats", value=msg_serializer(valeurs_stat))    ## key=Nonee : setting the key to None will impact the partitiom of the topic 
        print(valeurs_stat)

        #we compute the alert message
        if n_pred>=100:
            valeurs_alert = { 'type': 'alert', 'cid': cid, 'msg' : value['msg'], 'T_obs': T_obs, 'n_tot' : int(n_pred)}
            producer_alert.send("alert", value=msg_serializer(valeurs_alert)) ## key=Nonee : setting the key to None will impact the partitiom of the topic 
            print(valeurs_alert)
        

