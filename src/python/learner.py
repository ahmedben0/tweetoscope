## This is the learner part.
## The learner is a random forest, for each observation window
## inputs : params (p, beta, G1), target: n_tot(size of the cascade).
## In the topic "models", there's a partition for each time window

from utils import *

## init logger
logger = logger.get_logger('Learner', broker_list='localhost:9092', debug=True)


## Create consumer for reading samples sent by predictor node
consumerProperties = { "bootstrap_servers":['localhost:9092'],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}
consumer_samples = KafkaConsumer(**consumerProperties)
consumer_samples.subscribe("samples")


## Create producer to send trained models to the predictor
producerProperties = {"bootstrap_servers":['localhost:9092']}
producer_models = KafkaProducer(**producerProperties)


## Init dataset with features X=[p, beta, G1] and target Wobs
X_samples = pd.DataFrame(columns=['T_obs', 'n_star', 'beta', 'G1', 'W'])

features_columns = ['n_star', 'beta', 'G1']
target_columns = ['W']


counter = 0 #to determine after how many samples we train models.

for message in consumer_samples:
    key, value = msg_deserializer(message)

    #we add the new sample to the dataset
    X = [key]+value['X']+[value['W']]
    sample = pd.DataFrame([X], columns=X_samples.columns)
    X_samples = X_samples.append(sample, ignore_index=True)

    counter += 1
    
    if counter==50:
        #Train one model by observation window time
        for t_obs in X_samples.T_obs.unique():

            X_Tobs = X_samples[X_samples['T_obs']==t_obs] #we extract the samples corresponding to t_obs observation window size
            features = X_Tobs[features_columns]
            target = X_Tobs[target_columns]
            model = RandomForestRegressor(max_depth=max_depth, random_state=random_state)
            model.fit(features, target)

            logger.info('NEW MODEL:')
            logger.info('Time window: '+str(t_obs))
            logger.info('Number of samples: '+str(len(features)))


            #send trained model to the rpedictor on the corresponding partition for the time window partition
            producer_models.send("models", value=msg_serializer(model, model=True), key=msg_serializer(t_obs), partition=obs.index(t_obs))
            
            counter=0
