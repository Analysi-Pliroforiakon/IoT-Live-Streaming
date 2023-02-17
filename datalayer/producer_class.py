import confluent_kafka
import socket

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Acked message: %s" % (str(msg.value())))

class ProducerClass(confluent_kafka.Producer):
    def __init__(self):
        conf = {
            'bootstrap.servers': "localhost:9092, localhost:9192",
            'client.id': socket.gethostname()
        }
        print('producer config used:', conf)

        super().__init__(conf)

    def produce(self, sensor, curr_datetime, value):
        if sensor in ['TH1', 'TH2']:
            topic = 'temperature'
        elif sensor in ['HVAC1', 'HVAC2', 'MiAC1', 'MiAC2', 'Etot']:
            topic = 'energy'
        elif sensor in ['Mov1']:
            topic = 'motion'
        elif sensor in ['W1', 'Wtot']:
            topic = 'water'
        else:
            topic = 'new_topic'

        msg = f'{sensor} | {curr_datetime} | {value}'
        print(f'\t{sensor}: {msg}')
        super().produce(topic, key=sensor, value=msg, callback=acked)

import json
from datetime import datetime
from confluent_kafka import avro

def avro_acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % msg.value(), str(err))
    else:
        print("Acked message: %s" % msg.value())

def clean_str(string):
    return ' '.join(string.split())

class AvroProducerClass(confluent_kafka.avro.AvroProducer):
    def __init__(self):
        conf = {
            'bootstrap.servers': "localhost:9092, localhost:9192",
            'client.id': socket.gethostname(),
            'schema.registry.url': "http://localhost:8081"
        }
        print('producer config used:', conf)

        self.key_schema = avro.load("avro/kafka_keys.avsc")
        self.value_schema = avro.load("avro/kafka_values.avsc")

        super().__init__(conf, default_key_schema=self.key_schema, default_value_schema=self.value_schema)

    def produce(self, sensor, curr_datetime, value):
        if sensor in ['TH1', 'TH2']:
            topic = 'temperature'
        elif sensor in ['HVAC1', 'HVAC2', 'MiAC1', 'MiAC2', 'Etot']:
            topic = 'energy'
        elif sensor in ['Mov1']:
            topic = 'motion'
        elif sensor in ['W1', 'Wtot']:
            topic = 'water'
        else:
            topic = 'new_topic'

        key_json = clean_str(f'{{\
            "sensorID": "{sensor}"\
        }}')
        
        #dt = datetime.strptime(curr_datetime, '%y-%m-%d %H:%M:%S')
        unix_time = curr_datetime.timestamp()

        value_json = clean_str(f'{{\
            "sensorID": "{sensor}",\
            "timestamp": {unix_time},\
            "value": {float(value)}\
        }}')

        #msg = f'{sensor} | {curr_datetime} | {value}'
        #print(f'\t{key_json}: {value_json}')
        print(json.loads(value_json))
        super().produce(topic=topic, key=json.loads(key_json), value=json.loads(value_json), callback=avro_acked)