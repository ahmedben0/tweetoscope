## This is the learner part.
## The ;earner is a random forest, for each observation window
## inputs : params (p, beta, G1), target: n_tot(size of the cascade)

from utils import *
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

## Create consumer
consumerProperties = { "bootstrap_servers":['localhost:9092'],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}

consumer_samples = KafkaConsumer(**consumerProperties)
consumer_samples.subscribe("samples")



##Create Producer
producerProperties = {"bootstrap_servers":['localhost:9092']}

producer_models = KafkaProducer(**producerProperties)



X_samples = pd.DataFrame(columns=['T_obs', 'p', 'beta', 'G1', 'W'])

features_columns = ['p', 'beta', 'G1']
target_columns = ['W']


## create dataset from samples
for message in consumer_samples:
    key, value = msg_deserializer(message)

    print(value)

    X = [key]+value['X']+[value['W']]
    sample = pd.DataFrame([X], columns=X_samples.columns)
    X_samples = X_samples.append(sample, ignore_index=True)


##Train models
for t_obs in X_samples.T_obs.unique():

    X_Tobs = X_samples[X_samples['T_obs']==t_obs] #we extract the samples corresponding to t_obs observation window size
    features = X_Tobs[features_columns]
    target = X_Tobs[target_columns]
    model = RandomForestRegressor(max_depth=max_depth, random_state=random_state)
    model.fit(features, target)

    producer_models.send("models", value=msg_serializer(model), key=msg_serializer(t_obs))
