import argparse                   # To parse command line arguments
import json                       # To parse and dump JSON
from kafka import KafkaProducer   # Import Kafka producder

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--broker-list', type=str, required=True, help="the broker list")
args = parser.parse_args()  # Parse arguments

producer = KafkaProducer(
  bootstrap_servers = args.broker_list,                     # List of brokers passed from the command line
  value_serializer=lambda v: json.dumps(v).encode('utf-8'), # How to serialize the value to a binary buffer
  key_serializer=str.encode                                 # How to serialize the key
)

msg = {
    'dst': 'Metz',
    'temp': 2,
    'type': 'rain',
    'comment': 'Nothing special'
}
for _ in range(3):
    producer.send('weather-forecast', key = msg['dst'], value = msg) # Send a new message to topic

producer.flush() # Flush: force purging intermediate buffers before leaving
