import argparse                   # To parse command line arguments
import json                       # To parse and dump JSON
from kafka import KafkaConsumer   # Import Kafka consumer

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--broker-list', type=str, required=True, help="the broker list")
args = parser.parse_args()  # Parse arguments

consumer = KafkaConsumer('weather-forecast',                   # Topic name
  bootstrap_servers = args.broker_list,                        # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

for msg in consumer:                            # Blocking call waiting for a new message
    print (f"msg: ({msg.key}, {msg.value})")    # Write key and payload of the received message
