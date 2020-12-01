## This is the predictor part. 
## The predictor uses the params issued by the estimator and 
## the model sent by the learner to predict the final size of the cascade.
## For each time window we fetch the last model in the corresponding partition of the topic "models"
## The predictor send samples to the learner to improve training.
## The predictor outputs a list of cascades with a an important predicted size in the topic "alert".
## The predictor outputs the ARE as a statistic of the performance in the topic "Stat"

from utils import *
import configparser


## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')


## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')

## init logger
logger = logger.get_logger('Predictor', broker_list=config["kafka"]["brokers"], debug=True)


##create topic models with a partition for each time window
admin_client = KafkaAdminClient(
    bootstrap_servers=config["kafka"]["brokers"]
)
#we start by deleting any existing topic
admin_client.delete_topics(['models'])
time.sleep(5)

topic_list = []
topic_list.append(NewTopic(name="models", num_partitions=len(obs), replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)


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

# class model for prediction
class model_consumer:
    def __init__(self, T_obs, topic='models'):
        """
        T_obs -- int, observation time window
        topic -- str, name of the topic from which e extract models
        partition_number -- int, the corresponding partition number for the observation window
        partiton -- kafka partition
        consumer -- kafka consumer assigned the current partition
        model -- sklearn random forest model, latest produced on the partition
        """
        self.T_obs = T_obs
        self.topic = topic
        self.partition_number = obs.index(T_obs)
        self.partition = TopicPartition(self.topic, self.partition_number)
        self.consumer = None
        self.model = None

    def init_consumer(self, consumer_properties):
        ## initialisation of the consumer (properties + assign partition)
        consumer_model = KafkaConsumer(**consumerProperties)
        consumer_model.assign([self.partition])
        self.consumer = consumer_model


    def refresh_model(self):
        ## read alst produced model by the learner in the partition
        self.consumer.seek_to_end() #go to last offset
        position = self.consumer.position(self.partition) #number of the last offset
        if position==0: # if no model yet assign None
            self.model = None
        else:
            self.consumer.seek(self.partition, position-1) #offset fo the last message sent
            for msg in self.consumer:
                value_model = pickle.loads(msg.value)
                self.model = value_model #assign model
                break


## Initialize consumers for each models
models = {}
for time in obs:
    models[time] = model_consumer(time)
    models[time].init_consumer(consumerProperties)




## We create a dict with the cascade id and observation time as key, 
## and the parameters we need as values (params, n_true, n_obs, msg).
##In fact, we have two types of messages in cascade_properties : size, parameters. 
## We collect the values that interest us in each.
cascades = {}

for message in consumer_cascadeProperties:

    #first step collect all the wanted values from each cascade
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


    # check if we have all the values
    wanted_keys = ['n_true', 'n_obs', 'params', 'msg']
    if all(elem in cascades[dict_key].keys()  for elem in wanted_keys):
        key, value = dict_key, cascades[dict_key]

        ## init values
        cid = key[0] #cascade id
        T_obs = key[1] #observation window size
        
        X = value['params'] #p, beta, G1
        n_true = value['n_true']
        n_obs = value['n_obs']

        W = compute_true_omega(n_obs, n_true, X) #the W we want to predict

        #refresh model for the corresponding model consumer
        model_consumer = models[T_obs]
        model_consumer.refresh_model()
        model = model_consumer.model
        


        #we compute here the message of type "sample", i.e a sample to feed the random forest
        #inputs: params, target: omega
        valeurs_sample =  {'type': 'sample', 'cid': cid, 'X' : X, 'W': W}
        producer_sample.send("samples", value=msg_serializer(valeurs_sample), key=msg_serializer(T_obs))
        logger.debug(f'[NEW SAMPLE] {valeurs_sample}')

        #We compute the ARE (messages of type stat)
        if model is None:
            w_obs =1
        else: 
            w_obs = model.predict(np.array(X).reshape(1, -1))[0] #predict the w_obs for the obs window
            
        n_pred = estimated_size(n_obs, X, w_obs=w_obs)
        are = compute_are(n_pred, n_true)
        valeurs_stat =  {'type': 'stat', 'cid': cid, 'T_obs' : T_obs, 'ARE': are}
        producer_stat.send("stats", value=msg_serializer(valeurs_stat), key=None)
        logger.debug(f'[ARE] {valeurs_stat}')
        logger.info(f'[ARE] {valeurs_stat["ARE"]}')


        #we compute the alert message
        valeurs_alert = { 'type': 'alert', 'cid': cid, 'msg' : value['msg'], 'T_obs': T_obs, 'n_tot' : n_pred}
        producer_alert.send("alert", value=msg_serializer(valeurs_alert), key=None)
        logger.debug(f'[ALERT] {valeurs_alert}')
        logger.info(f'[ALERT] {valeurs_alert["n_tot"]}')
        

        

