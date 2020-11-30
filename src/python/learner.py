## This is the learner part.
## The learner is a random forest, for each observation window
## inputs : params (p, beta, G1), target: n_tot(size of the cascade)

from utils import *
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import configparser

## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')


consumerProperties = { "bootstrap_servers":[config["kafka"]["brokers"]],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}

consumer_samples = KafkaConsumer(**consumerProperties)
consumer_samples.subscribe("samples")

#create producer
producerProperties = {"bootstrap_servers":[config["kafka"]["brokers"]]}

producer_models = KafkaProducer(**producerProperties)

#create dataset
X_samples = pd.DataFrame(columns=['T_obs', 'p', 'beta', 'G1', 'W'])

features_columns = ['p', 'beta', 'G1']
target_columns   = ['W']

counter = 0 #to determine after how many samples we train models.
## create dataset from samples
test = 0
for message in consumer_samples:
    key, value = msg_deserializer(message)
    print(key)

    X = [key]+value['X']+[value['W']]
    sample = pd.DataFrame([X], columns=X_samples.columns)
    print(sample)
    X_samples = X_samples.append(sample, ignore_index=True)

    counter += 1
    
    if counter==10:
        ##Train models
        for t_obs in X_samples.T_obs.unique():

            X_Tobs = X_samples[X_samples['T_obs']==t_obs] #we extract the samples corresponding to t_obs observation window size
            features = X_Tobs[features_columns]
            target = X_Tobs[target_columns].values.ravel()
            model = RandomForestRegressor(max_depth=max_depth, random_state=random_state)
            model.fit(features, target)
            producer_models.send("models", value=msg_serializer(model, model=True), key=msg_serializer(t_obs), partition=obs.index(t_obs))
            test+=1
            counter=0
